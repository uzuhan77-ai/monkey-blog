import json
from typing import Any

import httpx
from django.conf import settings

from ..models import Category, Tag


class AIConfigError(Exception):
    """Raised when AI config is missing."""


class AIServiceError(Exception):
    """Raised when AI request fails."""


def _normalize_name(value: str) -> str:
    return (value or "").strip().casefold()


def _trim_text(value: str, limit: int = 4000) -> str:
    return (value or "").strip()[:limit]


def _build_system_prompt(categories: list[dict[str, Any]], tags: list[dict[str, Any]]) -> str:
    category_names = ", ".join(item["name"] for item in categories) or "None"
    tag_names = ", ".join(item["name"] for item in tags) or "None"

    return (
        "你是中文技术博客后台的 AI 写作助手。"
        "请围绕 Django + Vue 技术博客场景，生成实用、可发布的文章建议。"
        "优先结合现有分类和标签。"
        "你必须只返回严格 JSON，不要返回 Markdown 代码块，不要添加额外解释。\n\n"
        f"现有分类：{category_names}\n"
        f"现有标签：{tag_names}\n\n"
        "返回 JSON 结构："
        "{"
        '"title": string, '
        '"summary": string, '
        '"category_name": string, '
        '"tag_names": string[], '
        '"outline": string[], '
        '"draft_markdown": string'
        "}\n\n"
        "要求："
        "1. 全部内容使用中文；"
        "2. title 要具体；"
        "3. summary 写 2-3 句；"
        "4. tag_names 最多 5 个；"
        "5. outline 返回 4-6 条；"
        "6. draft_markdown 返回一个适合继续编辑的 Markdown 草稿框架。"
    )


def _build_user_prompt(payload: dict[str, Any]) -> str:
    topic = payload.get("topic", "")
    audience = payload.get("audience", "")
    tone = payload.get("tone", "")
    keywords = payload.get("keywords", [])
    keyword_text = ", ".join(keywords) if keywords else "无"

    return (
        f"主题: {topic or '无'}\n"
        f"读者: {audience or '通用技术读者'}\n"
        f"风格: {tone or '实战型'}\n"
        f"关键词: {keyword_text}\n"
        f"当前标题: {_trim_text(payload.get('current_title', ''), 200) or '无'}\n"
        f"当前摘要: {_trim_text(payload.get('current_summary', ''), 600) or '无'}\n"
        f"当前正文片段: {_trim_text(payload.get('current_content', ''), 2000) or '无'}"
    )


def _match_category(raw_name: str, categories: list[dict[str, Any]]) -> dict[str, Any] | None:
    category_map = {_normalize_name(item["name"]): item for item in categories}
    return category_map.get(_normalize_name(raw_name))


def _match_tags(raw_names: list[str], tags: list[dict[str, Any]]) -> tuple[list[int], list[str], list[str]]:
    tag_map = {_normalize_name(item["name"]): item for item in tags}
    matched_ids: list[int] = []
    matched_names: list[str] = []
    suggested_names: list[str] = []
    seen_normalized: set[str] = set()

    for raw_name in raw_names[:5]:
        cleaned = (raw_name or "").strip()
        normalized = _normalize_name(cleaned)
        if not cleaned or normalized in seen_normalized:
            continue
        seen_normalized.add(normalized)
        suggested_names.append(cleaned)

        match = tag_map.get(normalized)
        if match:
            matched_ids.append(match["id"])
            matched_names.append(match["name"])

    return matched_ids, matched_names, suggested_names


def _extract_text_from_response(data: dict[str, Any]) -> str:
    content = data.get("content", [])
    text_parts = []

    for item in content:
        if item.get("type") == "text" and item.get("text"):
            text_parts.append(item["text"])

    return "\n".join(text_parts).strip()


def generate_writing_assistant_result(payload: dict[str, Any]) -> dict[str, Any]:
    if not settings.ANTHROPIC_AUTH_TOKEN:
        raise AIConfigError("ANTHROPIC_AUTH_TOKEN is not configured.")

    categories = list(Category.objects.values("id", "name").order_by("name"))
    tags = list(Tag.objects.values("id", "name").order_by("name"))

    request_payload = {
        "model": settings.ANTHROPIC_MODEL,
        "max_tokens": 1200,
        "system": _build_system_prompt(categories, tags),
        "messages": [
            {
                "role": "user",
                "content": _build_user_prompt(payload)
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {settings.ANTHROPIC_AUTH_TOKEN}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }

    endpoint = settings.ANTHROPIC_BASE_URL.rstrip("/") + "/v1/messages"

    try:
        with httpx.Client(
                timeout=settings.ANTHROPIC_TIMEOUT,
                trust_env=False,
        ) as client:
            response = client.post(endpoint, headers=headers, json=request_payload)
            response.raise_for_status()
            response_data = response.json()
    except httpx.HTTPStatusError as exc:
        raise AIServiceError(f"Gateway request failed: {exc.response.text}") from exc
    except httpx.HTTPError as exc:
        raise AIServiceError(f"Network error: {exc}") from exc
    except Exception as exc:
        raise AIServiceError(f"Unexpected AI error: {exc}") from exc

    output_text = _extract_text_from_response(response_data)
    if not output_text:
        raise AIServiceError("Empty AI response.")

    try:
        parsed = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise AIServiceError("AI response was not valid JSON.") from exc

    matched_category = _match_category(parsed.get("category_name", ""), categories)
    matched_tag_ids, matched_tag_names, suggested_tag_names = _match_tags(parsed.get("tag_names", []), tags)

    return {
        "title": (parsed.get("title") or "").strip(),
        "summary": (parsed.get("summary") or "").strip(),
        "category_name": matched_category["name"] if matched_category else (parsed.get("category_name") or "").strip(),
        "category_id": matched_category["id"] if matched_category else None,
        "tag_names": suggested_tag_names,
        "matched_tag_ids": matched_tag_ids,
        "matched_tag_names": matched_tag_names,
        "outline": [item.strip() for item in parsed.get("outline", []) if item.strip()][:6],
        "draft_markdown": (parsed.get("draft_markdown") or "").strip(),
        "model": settings.ANTHROPIC_MODEL,
    }
