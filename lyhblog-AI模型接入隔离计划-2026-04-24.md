# lyhblog AI 模型接入隔离计划 - 2026-04-24

## 1. 这次先定目标

你的诉求不是马上改项目，而是先把方案写清楚，并且保证：

1. 不影响博客现有功能。
2. 不影响你现在已经能跑的后台文章管理。
3. 后面如果要接 OpenAI 新模型，只动 AI 写作助手这条链路。
4. 最好以后模型升级时只改 `.env`，不要再改业务代码。

这份文档就是按这个目标写的。

---

## 2. 先看你项目当前状态

我检查的是你自己的项目代码，不是参考项目：

- `D:\Monkey-blog\lyhblog-backend`
- `D:\Monkey-blog\lyhblog-frontend`

当前 AI 功能相关位置如下：

- 后端配置：`lyhblog-backend/config/settings.py`
- 后端 AI 服务：`lyhblog-backend/blog/services/ai_service.py`
- 后端 AI 接口：`lyhblog-backend/blog/views/ai.py`
- 前端 AI 抽屉：`lyhblog-frontend/src/components/admin/AIAssistantDrawer.vue`

当前实际结论：

1. 你的博客主流程和 AI 是分开的。
   登录、注册、文章 CRUD、评论、分类、标签，不会因为 AI 模型切换自动受影响。

2. 当前 AI 写作助手只影响后台管理页里的 AI 按钮。
   也就是说，真正被影响的只有这条路径：
   `后台文章编辑页 -> AI 助手抽屉 -> /blog/ai/... 接口 -> ai_service.py`

3. 你现在后端虽然在 `settings.py` 里留了 `OPENAI_MODEL=gpt-5.4`，但真正调用逻辑并没有走 OpenAI。
   当前实际走的是 `ANTHROPIC_*` 配置。

所以，项目现在不会因为 OpenAI 最新模型发布而自己变化。
只有你主动把 `ai_service.py` 改成支持 OpenAI，它才会切换。

---

## 3. 最稳的改法

最稳的方案不是直接把当前逻辑硬改成 OpenAI。

而是：

1. 保留你现在的 `anthropic` 路线，作为默认值。
2. 新增一个环境变量 `AI_PROVIDER`。
3. `ai_service.py` 内部按 `AI_PROVIDER` 选择走：
   - `anthropic`
   - `openai`
4. 前端一个字都不用改。
5. 后端接口返回结构一个字都不用改。

这样做的好处：

1. 默认还是你现在的行为，不会突然炸。
2. 以后切模型只改 `.env`。
3. 如果 OpenAI API 暂时不稳定，你随时切回 `anthropic`。
4. 未来 OpenAI API 放出 `gpt-5.5` 后，大概率只改：
   `OPENAI_MODEL=gpt-5.5`

---

## 4. 关于“最新模型”在你项目里的实际建议

截至 `2026-04-24`：

1. ChatGPT / Codex 侧最新公开的是 `GPT-5.5`。
2. 但 API 侧现在更稳妥、可直接用于项目接入的，仍然按 `gpt-5.4` 来准备。

所以你项目里不要写死“我要上 GPT-5.5 API”。

更安全的策略是：

1. 代码先支持 OpenAI Provider。
2. `.env` 里先填：
   `OPENAI_MODEL=gpt-5.4`
3. 等 API 真开放 `gpt-5.5` 后，你只改环境变量。

这才叫“不要受其他影响”。

---

## 5. 计划中的最小改动范围

只建议未来改下面 3 个文件：

1. `lyhblog-backend/config/settings.py`
2. `lyhblog-backend/.env.example`
3. `lyhblog-backend/blog/services/ai_service.py`

不建议动这些位置：

1. `lyhblog-frontend/src/components/admin/AIAssistantDrawer.vue`
2. `lyhblog-backend/blog/views/ai.py`
3. 文章、评论、分类、标签相关接口

原因很简单：

你的前后端协议已经通了。
只要 `generate_writing_assistant_result()` 返回的数据结构不变，前端就不需要改。

---

## 6. 未来要改时，settings.py 建议加的代码

位置：
`lyhblog-backend/config/settings.py`

在 AI 配置附近建议改成这样：

```python
# AI settings
AI_PROVIDER = (os.getenv("AI_PROVIDER", "anthropic") or "anthropic").strip().lower()

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4")
OPENAI_TIMEOUT = float(os.getenv("OPENAI_TIMEOUT", "60"))

ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
ANTHROPIC_AUTH_TOKEN = os.getenv("ANTHROPIC_AUTH_TOKEN", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
ANTHROPIC_TIMEOUT = float(os.getenv("ANTHROPIC_TIMEOUT", "60"))
```

这里的核心不是多了几个变量，而是多了一个：

```python
AI_PROVIDER
```

后面 `ai_service.py` 就靠它决定走哪条路。

---

## 7. 未来要改时，.env.example 建议长这样

位置：
`lyhblog-backend/.env.example`

建议不要在仓库里放真实 token，只放占位符。

```env
DJANGO_SECRET_KEY=replace-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=lyhblog
DB_USER=lyhblog
DB_PASSWORD=123
DB_HOST=127.0.0.1
DB_PORT=3306

AI_PROVIDER=anthropic

OPENAI_BASE_URL=https://api.openai.com
OPENAI_API_KEY=replace-with-your-openai-api-key
OPENAI_MODEL=gpt-5.4
OPENAI_TIMEOUT=60

ANTHROPIC_BASE_URL=https://coding.beehears.com
ANTHROPIC_AUTH_TOKEN=replace-with-your-anthropic-token
ANTHROPIC_MODEL=claude-sonnet-4-6
ANTHROPIC_TIMEOUT=60
```

说明：

1. 你现在如果还想继续用当前中转，就保留：
   `AI_PROVIDER=anthropic`

2. 你后面如果想切 OpenAI，就只改：

```env
AI_PROVIDER=openai
OPENAI_API_KEY=你的真实 key
OPENAI_MODEL=gpt-5.4
```

---

## 8. 未来要改时，ai_service.py 的完整参考代码

位置：
`lyhblog-backend/blog/services/ai_service.py`

下面这份是“以后真要改时”的完整参考实现。
重点是：

1. 对外函数名不变：`generate_writing_assistant_result`
2. 返回结构不变
3. 前端不用动
4. 默认 provider 可以继续走你现有线路

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
    category_names = ", ".join(item["name"] for item in categories) or "无"
    tag_names = ", ".join(item["name"] for item in tags) or "无"

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


def _strip_code_fences(text: str) -> str:
    cleaned = (text or "").strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines:
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned


def _extract_anthropic_text(data: dict[str, Any]) -> str:
    content = data.get("content", [])
    text_parts = []

    for item in content:
        if item.get("type") == "text" and item.get("text"):
            text_parts.append(item["text"])

    return "\n".join(text_parts).strip()


def _extract_openai_text(data: dict[str, Any]) -> str:
    choices = data.get("choices", [])
    if not choices:
        return ""

    message = choices[0].get("message", {})
    content = message.get("content")

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        text_parts = []
        for item in content:
            if item.get("type") == "text" and item.get("text"):
                text_parts.append(item["text"])
        return "\n".join(text_parts).strip()

    return ""


def _parse_output_json(output_text: str) -> dict[str, Any]:
    cleaned = _strip_code_fences(output_text)
    if not cleaned:
        raise AIServiceError("Empty AI response.")

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise AIServiceError("AI response was not valid JSON.") from exc


def _call_anthropic(system_prompt: str, user_prompt: str) -> dict[str, Any]:
    if not settings.ANTHROPIC_AUTH_TOKEN:
        raise AIConfigError("ANTHROPIC_AUTH_TOKEN is not configured.")

    request_payload = {
        "model": settings.ANTHROPIC_MODEL,
        "max_tokens": 1200,
        "system": system_prompt,
        "messages": [
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
    }

    headers = {
        "Authorization": f"Bearer {settings.ANTHROPIC_AUTH_TOKEN}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }

    endpoint = settings.ANTHROPIC_BASE_URL.rstrip("/") + "/v1/messages"

    try:
        with httpx.Client(timeout=settings.ANTHROPIC_TIMEOUT, trust_env=False) as client:
            response = client.post(endpoint, headers=headers, json=request_payload)
            response.raise_for_status()
            response_data = response.json()
    except httpx.HTTPStatusError as exc:
        raise AIServiceError(f"Anthropic request failed: {exc.response.text}") from exc
    except httpx.HTTPError as exc:
        raise AIServiceError(f"Anthropic network error: {exc}") from exc
    except Exception as exc:
        raise AIServiceError(f"Unexpected Anthropic error: {exc}") from exc

    return _parse_output_json(_extract_anthropic_text(response_data))


def _call_openai(system_prompt: str, user_prompt: str) -> dict[str, Any]:
    if not settings.OPENAI_API_KEY:
        raise AIConfigError("OPENAI_API_KEY is not configured.")

    request_payload = {
        "model": settings.OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    endpoint = settings.OPENAI_BASE_URL.rstrip("/") + "/v1/chat/completions"

    try:
        with httpx.Client(timeout=settings.OPENAI_TIMEOUT, trust_env=False) as client:
            response = client.post(endpoint, headers=headers, json=request_payload)
            response.raise_for_status()
            response_data = response.json()
    except httpx.HTTPStatusError as exc:
        raise AIServiceError(f"OpenAI request failed: {exc.response.text}") from exc
    except httpx.HTTPError as exc:
        raise AIServiceError(f"OpenAI network error: {exc}") from exc
    except Exception as exc:
        raise AIServiceError(f"Unexpected OpenAI error: {exc}") from exc

    return _parse_output_json(_extract_openai_text(response_data))


def generate_writing_assistant_result(payload: dict[str, Any]) -> dict[str, Any]:
    categories = list(Category.objects.values("id", "name").order_by("name"))
    tags = list(Tag.objects.values("id", "name").order_by("name"))

    system_prompt = _build_system_prompt(categories, tags)
    user_prompt = _build_user_prompt(payload)

    provider = getattr(settings, "AI_PROVIDER", "anthropic")
    provider = (provider or "anthropic").strip().lower()

    if provider == "openai":
        parsed = _call_openai(system_prompt, user_prompt)
        current_model = settings.OPENAI_MODEL
    elif provider == "anthropic":
        parsed = _call_anthropic(system_prompt, user_prompt)
        current_model = settings.ANTHROPIC_MODEL
    else:
        raise AIConfigError(f"Unsupported AI_PROVIDER: {provider}")

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
        "model": current_model,
    }
```

---

## 9. 这份代码为什么不会影响你其他模块

原因有 4 个：

1. 只改一个服务层文件：
   `blog/services/ai_service.py`

2. `blog/views/ai.py` 的调用方式不变：
   还是调用 `generate_writing_assistant_result(payload)`

3. 前端接收的数据结构不变：
   还是这些字段：
   `title`
   `summary`
   `category_name`
   `category_id`
   `tag_names`
   `matched_tag_ids`
   `matched_tag_names`
   `outline`
   `draft_markdown`
   `model`

4. 登录、文章 CRUD、评论、首页展示都不依赖这条服务

所以这次方案是“功能隔离式”改法，不是全局改法。

---

## 10. 你下一步应该怎么做

### 方案 A：现在先不动代码，只把这份文档留着

适合你现在的状态。

你下一步先做：

1. 继续把博客 CRUD 和部署跑顺。
2. 不要急着上最新模型。
3. 把 AI 写作助手先当成独立增强功能。

这个阶段最重要的是：
博客主体先稳。

### 方案 B：后面要接 OpenAI 时，再按文档落代码

建议顺序：

1. 先改 `settings.py`
2. 再改 `.env.example`
3. 最后替换 `ai_service.py`
4. 本地 `.env` 先写：

```env
AI_PROVIDER=openai
OPENAI_API_KEY=你的 key
OPENAI_MODEL=gpt-5.4
OPENAI_TIMEOUT=60
```

5. 跑检查：

```bash
cd D:\Monkey-blog\lyhblog-backend
venv\Scripts\python.exe manage.py check
```

6. 再启动后端：

```bash
venv\Scripts\python.exe manage.py runserver
```

7. 最后手测后台文章编辑页里的 AI 助手按钮

---

## 11. 最后给你的明确建议

如果你现在问我：
“我下一步到底做什么最合适？”

答案是：

1. 先不要动项目主代码。
2. 把这份方案文档留着。
3. 你当前项目如果只是想稳定推进，先继续完成博客主体。
4. 真要接 OpenAI，就按这份方案做“隔离式接入”。
5. 模型先用 `gpt-5.4`，不要在项目里抢跑 `gpt-5.5 API`。

这条路最稳，也最不容易把你现有项目带偏。
