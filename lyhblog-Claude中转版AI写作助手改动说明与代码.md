# lyhblog Claude 中转版 AI 写作助手改动说明与代码

更新时间：2026-04-17
适用项目：`D:\Monkey-blog\lyhblog-backend` + `D:\Monkey-blog\lyhblog-frontend`
默认模型：`claude-sonnet-4-6`
说明：这份文档只提供 **Claude / Anthropic 中转版** 的接入方案和代码，不直接改你的项目文件。

## 1. 先说结论

如果你现在不用 OpenAI，而是走你自己的 Claude 中转，那么这一版项目建议这样做：

- 前端代码：基本不变
- 后端代码：不要再用 OpenAI SDK
- 改成：`Django + httpx + /v1/messages`
- 配置项改为：
  - `ANTHROPIC_BASE_URL`
  - `ANTHROPIC_AUTH_TOKEN`
  - `ANTHROPIC_MODEL`
  - `ANTHROPIC_TIMEOUT`

这更符合你现在的中转环境，也更容易控制请求头和模型名。

## 2. 为什么这版不用 OpenAI SDK 或 Anthropic SDK

你现在给的是中转网关，不是我可以直接假设的官方直连环境。

对这种场景，最稳的方式是直接自己发 HTTP 请求，这样你能明确控制：

- `Authorization` 头
- `anthropic-version` 头
- 请求地址拼接
- 模型名
- 超时

所以这版建议：

**后端统一改成 `httpx` 调网关。**

## 3. 安全提醒

你之前贴过真实 token。那把 token 已经暴露了。

建议你现在就：

1. 去中转后台重新生成一把新 token
2. 新 token 只放本地 `.env`
3. 不要再贴聊天里
4. 不要提交到 GitHub

下面文档里只写占位符，不写你的真实 token。

## 4. 这次需要改哪些地方

### 后端需要改

- `lyhblog-backend/requirements.txt`
- `lyhblog-backend/.env.example`
- `lyhblog-backend/config/settings.py`
- `lyhblog-backend/blog/services/ai_service.py`

### 后端继续沿用

- `lyhblog-backend/blog/views/ai.py`
- `lyhblog-backend/blog/urls.py`

### 前端基本不用改

继续沿用你之前那份完整接入文档里的：

- `src/api/ai.js`
- `src/components/admin/AIAssistantDrawer.vue`
- `src/views/admin/ArticleEdit.vue`
- `src/utils/request.js`

也就是说：

**这次核心只替换后端 AI service 和环境变量。**

## 5. 后端具体改法

### 5.1 `requirements.txt`

把 AI 相关依赖改成：

```txt
httpx==0.28.1
```

一个可用示例：

```txt
asgiref==3.11.1
Django==6.0.2
django-cors-headers==4.9.0
djangorestframework==3.16.1
mysqlclient==2.2.7
python-dotenv==1.1.0
sqlparse==0.5.5
tzdata==2025.3
gunicorn==23.0.0
httpx==0.28.1
```

### 5.2 `lyhblog-backend/.env.example`

```env
DJANGO_SECRET_KEY=replace-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=lyhblog
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=3306
ANTHROPIC_BASE_URL=https://your-gateway.example.com
ANTHROPIC_AUTH_TOKEN=your-gateway-token
ANTHROPIC_MODEL=claude-sonnet-4-6
ANTHROPIC_TIMEOUT=60
```

说明：

- 这里 `ANTHROPIC_BASE_URL` 写你的中转根地址
- 这版默认模型按你当前中转支持的别名来写：`claude-sonnet-4-6`
- 这里按你的网关模型别名配置，不强制使用 Anthropic 官方快照名

### 5.3 `config/settings.py`

你现在的 `settings.py` 已经踩过一个坑：`BASE_DIR` 必须先定义，再 `load_dotenv`。

正确顺序：

```python
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
```

然后在底部追加这些配置：

```python
ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
ANTHROPIC_AUTH_TOKEN = os.getenv("ANTHROPIC_AUTH_TOKEN", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
ANTHROPIC_TIMEOUT = float(os.getenv("ANTHROPIC_TIMEOUT", "60"))
```

### 5.4 替换 `blog/services/ai_service.py`

```python
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
        "你必须只返回严格 JSON，不要返回 Markdown 代码块，不要加额外解释。\n\n"
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
        "1. 全部内容用中文；"
        "2. title 要具体；"
        "3. summary 写 2-3 句；"
        "4. tag_names 最多 5 个；"
        "5. outline 返回 4-6 条；"
        "6. draft_markdown 返回一个适合继续编辑的 Markdown 草稿骨架。"
    )


def _build_user_prompt(payload: dict[str, Any]) -> str:
    topic = payload.get("topic", "")
    audience = payload.get("audience", "")
    tone = payload.get("tone", "")
    keywords = payload.get("keywords", [])
    keyword_text = ", ".join(keywords) if keywords else "None"

    return (
        f"主题: {topic or 'None'}\n"
        f"读者: {audience or '通用技术读者'}\n"
        f"风格: {tone or '实战型'}\n"
        f"关键词: {keyword_text}\n"
        f"当前标题: {_trim_text(payload.get('current_title', ''), 200) or 'None'}\n"
        f"当前摘要: {_trim_text(payload.get('current_summary', ''), 600) or 'None'}\n"
        f"当前正文片段: {_trim_text(payload.get('current_content', ''), 2000) or 'None'}"
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
        with httpx.Client(timeout=settings.ANTHROPIC_TIMEOUT) as client:
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
```

## 6. `views/ai.py` 可以继续沿用

你上一篇完整方案里的 `AIWritingAssistantView` 基本可以继续用。

只要它还是这样调用：

```python
from ..services.ai_service import AIConfigError, AIServiceError, generate_writing_assistant_result
```

那前端接口就不用改。

## 7. `urls.py` 也继续沿用

仍然保留：

```python
path('ai/writing-assistant/', AIWritingAssistantView.as_view()),
```

## 8. 前端部分怎么处理

前端这版基本不用重新写。

继续沿用你之前那份完整文档里的：

- `src/api/ai.js`
- `src/components/admin/AIAssistantDrawer.vue`
- `src/views/admin/ArticleEdit.vue`
- `src/utils/request.js`

因为前端只关心：

```text
POST /api/ai/writing-assistant/
```

后端底层到底走 OpenAI 还是 Claude 中转，前端无感。

## 9. 你本地 `.env` 应该怎么写

### Django 后端 `.env`

```env
ANTHROPIC_BASE_URL=https://api.beehears.com
ANTHROPIC_AUTH_TOKEN=换成你新的token
ANTHROPIC_MODEL=claude-sonnet-4-6
ANTHROPIC_TIMEOUT=60
```

### 你本机 Claude Code 环境变量

```powershell
$env:ANTHROPIC_BASE_URL="https://api.beehears.com"
$env:ANTHROPIC_AUTH_TOKEN="your-new-token"
$env:CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
```

## 10. 你现在该怎么做

按顺序来：

1. 先轮换你之前暴露过的 token
2. 后端 `.env` 改成 `ANTHROPIC_*` 这套
3. `settings.py` 改成读取 `ANTHROPIC_BASE_URL / AUTH_TOKEN / MODEL / TIMEOUT`
4. `ai_service.py` 改成这份文档里的 `httpx` 版本
5. 前端继续沿用之前写好的 AI 抽屉和按钮逻辑

## 11. 最后判断

对你当前阶段，我的建议是：

- 可以先走 Claude 中转
- 后端别继续按 OpenAI SDK 方案硬套
- 改成 `httpx + Anthropic Messages API 风格` 最稳
- 前端不用重写
- 先把功能跑通，再谈后面是否换官方 API

## 12. 参考资料

- Claude Code settings: https://docs.anthropic.com/en/docs/claude-code/settings
- Claude Code LLM gateway: https://docs.anthropic.com/en/docs/claude-code/llm-gateway
- Anthropic models overview: https://docs.anthropic.com/en/docs/models-overview
