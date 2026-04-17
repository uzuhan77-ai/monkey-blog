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
        "浣犳槸涓枃鎶€鏈崥瀹㈠悗鍙扮殑 AI 鍐欎綔鍔╂墜銆?
        "璇峰洿缁?Django + Vue 鎶€鏈崥瀹㈠満鏅紝鐢熸垚瀹炵敤銆佸彲鍙戝竷鐨勬枃绔犲缓璁€?
        "浼樺厛缁撳悎鐜版湁鍒嗙被鍜屾爣绛俱€?
        "浣犲繀椤诲彧杩斿洖涓ユ牸 JSON锛屼笉瑕佽繑鍥?Markdown 浠ｇ爜鍧楋紝涓嶈鍔犻澶栬В閲娿€俓n\n"
        f"鐜版湁鍒嗙被锛歿category_names}\n"
        f"鐜版湁鏍囩锛歿tag_names}\n\n"
        "杩斿洖 JSON 缁撴瀯锛?
        "{"
        '"title": string, '
        '"summary": string, '
        '"category_name": string, '
        '"tag_names": string[], '
        '"outline": string[], '
        '"draft_markdown": string'
        "}\n\n"
        "瑕佹眰锛?
        "1. 鍏ㄩ儴鍐呭鐢ㄤ腑鏂囷紱"
        "2. title 瑕佸叿浣擄紱"
        "3. summary 鍐?2-3 鍙ワ紱"
        "4. tag_names 鏈€澶?5 涓紱"
        "5. outline 杩斿洖 4-6 鏉★紱"
        "6. draft_markdown 杩斿洖涓€涓€傚悎缁х画缂栬緫鐨?Markdown 鑽夌楠ㄦ灦銆?
    )


def _build_user_prompt(payload: dict[str, Any]) -> str:
    topic = payload.get("topic", "")
    audience = payload.get("audience", "")
    tone = payload.get("tone", "")
    keywords = payload.get("keywords", [])
    keyword_text = ", ".join(keywords) if keywords else "None"

    return (
        f"涓婚: {topic or 'None'}\n"
        f"璇昏€? {audience or '閫氱敤鎶€鏈鑰?}\n"
        f"椋庢牸: {tone or '瀹炴垬鍨?}\n"
        f"鍏抽敭璇? {keyword_text}\n"
        f"褰撳墠鏍囬: {_trim_text(payload.get('current_title', ''), 200) or 'None'}\n"
        f"褰撳墠鎽樿: {_trim_text(payload.get('current_summary', ''), 600) or 'None'}\n"
        f"褰撳墠姝ｆ枃鐗囨: {_trim_text(payload.get('current_content', ''), 2000) or 'None'}"
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
