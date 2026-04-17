# lyhblog AI 写作助手第一版完整方案与代码

更新时间：2026-04-17
适用项目：`D:\Monkey-blog\lyhblog-backend` + `D:\Monkey-blog\lyhblog-frontend`
说明：这份文档**只提供方案和代码**，不直接改你的项目文件。你可以按文档逐步手动粘贴。

---

## 1. 第一版目标

先做一个能真实接进你现有博客后台、也能写进简历的 AI 功能：

`后台文章编辑页 + AI 写作助手`

第一版完成后，你应该能做到：

- 在后台文章编辑页点击 `AI 助手`
- 输入主题、关键词、读者、风格
- 调用 OpenAI Responses API
- 返回结构化结果：
  - 标题
  - 摘要
  - 分类建议
  - 标签建议
  - 提纲建议
  - Markdown 草稿
- 把这些内容一键回填到文章表单

这已经是一个很完整的“AI + 内容管理系统”项目亮点了。

---

## 2. 第一版为什么这样做

第一版先不上这些：

- `LangChain`
- `LangGraph`
- `CrewAI`
- 多 Agent 协作
- 浏览器自动操作 Agent

原因：

- 你现在最需要的是**做出真实可演示功能**，不是先堆框架
- 这个业务场景很清晰：单次生成、结构化输出、回填表单
- 用 `Django + OpenAI SDK + Responses API` 就够了
- 后面如果做多步骤工作流，再考虑 `LangGraph`

---

## 3. 建议使用的模型

第一版默认：

- `OPENAI_MODEL=gpt-5.4`

原因：

- 成本低
- 能力够第一版写作助手使用
- 更适合你本地联调和简历项目

后面如果你觉得质量不够，再把关键任务切到：

- `gpt-5.4`

---

## 4. 最终效果结构

```text
Vue 后台文章编辑页
    ↓
点击 AI 助手
    ↓
POST /api/ai/writing-assistant/
    ↓
Django DRF 视图
    ↓
AI service 调 OpenAI Responses API
    ↓
返回 JSON 结果
    ↓
Vue 抽屉展示结果
    ↓
一键回填标题 / 摘要 / 标签 / 正文
```

---

## 5. 需要新增或修改的文件

### 后端

新增：

- `lyhblog-backend/blog/services/__init__.py`
- `lyhblog-backend/blog/services/ai_service.py`
- `lyhblog-backend/blog/views/ai.py`
- `lyhblog-backend/.env.example`

修改：

- `lyhblog-backend/requirements.txt`
- `lyhblog-backend/config/settings.py`
- `lyhblog-backend/blog/urls.py`

### 前端

新增：

- `lyhblog-frontend/src/api/ai.js`
- `lyhblog-frontend/src/components/admin/AIAssistantDrawer.vue`
- `lyhblog-frontend/.env.example`

修改：

- `lyhblog-frontend/src/utils/request.js`
- `lyhblog-frontend/src/views/admin/ArticleEdit.vue`

---

## 6. 后端代码

### 6.1 `lyhblog-backend/requirements.txt`

在现有依赖里新增一行：

```txt
openai==2.31.0
```

完整示例：

```txt
asgiref==3.11.1
Django==6.0.2
django-cors-headers==4.9.0
djangorestframework==3.16.1
mysqlclient==2.2.7
openai==2.31.0
python-dotenv==1.1.0
sqlparse==0.5.5
tzdata==2025.3
gunicorn==23.0.0
```

---

### 6.2 `lyhblog-backend/.env.example`

```env
DJANGO_SECRET_KEY=replace-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=lyhblog
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=3306
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-5.4
OPENAI_TIMEOUT=60
```

说明：

- 这是示例文件，可以提交到 GitHub
- 真正运行时你要自己再建 `.env`

---

### 6.3 `lyhblog-backend/config/settings.py`

你当前 `settings.py` 已经有大量原有配置，不建议整文件替换。只补下面这些代码。

#### 1. 顶部 import 区补这几行

```python
import os
from pathlib import Path

from dotenv import load_dotenv
```

#### 2. `BASE_DIR` 下方补这行

```python
load_dotenv(BASE_DIR / ".env")
```

#### 3. 文件底部追加 AI 配置

```python
# AI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4")
OPENAI_TIMEOUT = float(os.getenv("OPENAI_TIMEOUT", "60"))
```

说明：

- 这里只是先把 AI 配置读取打通
- 你后面仍然应该把数据库、`SECRET_KEY`、`DEBUG` 也一起环境变量化

---

### 6.4 新建 `lyhblog-backend/blog/services/__init__.py`

```python
"""Service layer helpers for the blog app."""
```

---

### 6.5 新建 `lyhblog-backend/blog/services/ai_service.py`

```python
import json
from typing import Any

from django.conf import settings
from openai import APIError, APITimeoutError, OpenAI

from ..models import Category, Tag


WRITING_ASSISTANT_SCHEMA = {
    "type": "json_schema",
    "name": "writing_assistant_result",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "summary": {"type": "string"},
            "category_name": {"type": "string"},
            "tag_names": {
                "type": "array",
                "items": {"type": "string"},
            },
            "outline": {
                "type": "array",
                "items": {"type": "string"},
            },
            "draft_markdown": {"type": "string"},
        },
        "required": [
            "title",
            "summary",
            "category_name",
            "tag_names",
            "outline",
            "draft_markdown",
        ],
        "additionalProperties": False,
    },
}


class AIConfigError(Exception):
    """Raised when AI config is missing."""


class AIServiceError(Exception):
    """Raised when AI request fails."""


def _normalize_name(value: str) -> str:
    return (value or "").strip().casefold()


def _trim_text(value: str, limit: int = 4000) -> str:
    return (value or "").strip()[:limit]


def _get_client() -> OpenAI:
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        raise AIConfigError("OPENAI_API_KEY is not configured.")
    return OpenAI(api_key=api_key, timeout=settings.OPENAI_TIMEOUT)


def _build_system_prompt(categories: list[dict[str, Any]], tags: list[dict[str, Any]]) -> str:
    category_names = ", ".join(item["name"] for item in categories) or "None"
    tag_names = ", ".join(item["name"] for item in tags) or "None"

    return (
        "You are an AI writing assistant for a Chinese technical blog admin panel. "
        "Generate practical article metadata and a markdown draft skeleton for a Django + Vue blog. "
        "Keep the style concise, useful, and publishable. "
        "Prefer the existing categories and tags when they are relevant.\n\n"
        f"Existing categories: {category_names}\n"
        f"Existing tags: {tag_names}\n\n"
        "Rules:\n"
        "1. Write the result in Chinese.\n"
        "2. Title should be specific and not too exaggerated.\n"
        "3. Summary should be 2-3 sentences.\n"
        "4. Choose one category_name. If nothing fits, return an empty string.\n"
        "5. Return up to 5 tag_names.\n"
        "6. Return 4-6 outline items.\n"
        "7. draft_markdown should be a short markdown draft skeleton using headings and bullet points.\n"
        "8. Follow the provided JSON schema exactly."
    )


def _build_user_prompt(payload: dict[str, Any]) -> str:
    topic = payload.get("topic", "")
    audience = payload.get("audience", "")
    tone = payload.get("tone", "")
    keywords = payload.get("keywords", [])
    keyword_text = ", ".join(keywords) if keywords else "None"

    return (
        f"Topic: {topic or 'None'}\n"
        f"Audience: {audience or 'General blog readers'}\n"
        f"Tone: {tone or '实战型'}\n"
        f"Keywords: {keyword_text}\n"
        f"Current title: {_trim_text(payload.get('current_title', ''), 200) or 'None'}\n"
        f"Current summary: {_trim_text(payload.get('current_summary', ''), 600) or 'None'}\n"
        f"Current content excerpt: {_trim_text(payload.get('current_content', ''), 2000) or 'None'}"
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


def generate_writing_assistant_result(payload: dict[str, Any]) -> dict[str, Any]:
    client = _get_client()
    categories = list(Category.objects.values("id", "name").order_by("name"))
    tags = list(Tag.objects.values("id", "name").order_by("name"))

    try:
        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            input=[
                {"role": "system", "content": _build_system_prompt(categories, tags)},
                {"role": "user", "content": _build_user_prompt(payload)},
            ],
            text={"format": WRITING_ASSISTANT_SCHEMA},
        )
    except (APITimeoutError, APIError) as exc:
        raise AIServiceError(f"OpenAI request failed: {exc}") from exc
    except Exception as exc:
        raise AIServiceError(f"Unexpected AI error: {exc}") from exc

    if not response.output_text:
        raise AIServiceError("Empty AI response.")

    try:
        parsed = json.loads(response.output_text)
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
        "model": settings.OPENAI_MODEL,
    }
```

---

### 6.6 新建 `lyhblog-backend/blog/views/ai.py`

```python
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services.ai_service import AIConfigError, AIServiceError, generate_writing_assistant_result


class AIWritingAssistantView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        topic = (request.data.get("topic") or "").strip()
        current_title = (request.data.get("current_title") or "").strip()
        current_summary = (request.data.get("current_summary") or "").strip()
        current_content = (request.data.get("current_content") or "").strip()

        if not any([topic, current_title, current_summary, current_content]):
            return Response(
                {"code": 400, "message": "请输入主题，或提供现有草稿内容。"},
                status=400,
            )

        keywords = request.data.get("keywords", [])
        if isinstance(keywords, str):
            keywords = [item.strip() for item in keywords.split(",") if item.strip()]
        elif isinstance(keywords, list):
            keywords = [str(item).strip() for item in keywords if str(item).strip()]
        else:
            keywords = []

        try:
            result = generate_writing_assistant_result(
                {
                    "topic": topic,
                    "keywords": keywords,
                    "audience": (request.data.get("audience") or "").strip(),
                    "tone": (request.data.get("tone") or "").strip(),
                    "current_title": current_title,
                    "current_summary": current_summary,
                    "current_content": current_content,
                }
            )
        except AIConfigError as exc:
            return Response({"code": 503, "message": str(exc)}, status=503)
        except AIServiceError as exc:
            return Response({"code": 502, "message": str(exc)}, status=502)

        return Response({"code": 200, "message": "AI 建议生成成功", "data": result})
```

---

### 6.7 修改 `lyhblog-backend/blog/urls.py`

在 import 区新增：

```python
from .views.ai import AIWritingAssistantView
```

在 `urlpatterns` 里新增：

```python
path('ai/writing-assistant/', AIWritingAssistantView.as_view()),
```

放在 `comment` 路由前面或后面都行，只要在列表里即可。

如果你想直接看一个整理后的完整版本，可以参考：

```python
from django.urls import path

from .views import (
    TestView, ArticleListView, ArticleDetailView, ArticleAddView, ArticleDeleteView, ArticleUpdateView,
    LoginView, RegisterView
)
from .views.ai import AIWritingAssistantView
from .views.category import CategoryListView, CategoryAddView, CategoryUpdateView, CategoryDeleteView
from .views.comment import CommentListView, CommentAddView, CommentDeleteView, CommentAllView
from .views.tag import TagListView, TagAddView, TagUpdateView, TagDeleteView

urlpatterns = [
    path('test/', TestView.as_view(), name='test'),

    path('user/login/', LoginView.as_view(), name='login'),
    path('user/register/', RegisterView.as_view(), name='register'),

    path('article/listArticle/', ArticleListView.as_view(), name='article-list'),
    path('article/getArticleById/', ArticleDetailView.as_view(), name='article-detail'),
    path('article/add/', ArticleAddView.as_view(), name='article-add'),
    path('article/delete/', ArticleDeleteView.as_view(), name='article-delete'),
    path('article/update/', ArticleUpdateView.as_view(), name='article-update'),

    path('category/list/', CategoryListView.as_view()),
    path('category/add/', CategoryAddView.as_view()),
    path('category/update/', CategoryUpdateView.as_view()),
    path('category/delete/', CategoryDeleteView.as_view()),

    path('tag/list/', TagListView.as_view()),
    path('tag/add/', TagAddView.as_view()),
    path('tag/update/', TagUpdateView.as_view()),
    path('tag/delete/', TagDeleteView.as_view()),

    path('ai/writing-assistant/', AIWritingAssistantView.as_view()),

    path('comment/list/', CommentListView.as_view()),
    path('comment/add/', CommentAddView.as_view()),
    path('comment/delete/', CommentDeleteView.as_view()),
    path('comment/all/', CommentAllView.as_view()),
]
```

---

## 7. 前端代码

### 7.1 新建 `lyhblog-frontend/.env.example`

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

你本地实际跑的时候，再手动建：

- `lyhblog-frontend/.env.development`
- `lyhblog-frontend/.env.production`

例如开发环境：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

---

### 7.2 替换 `lyhblog-frontend/src/utils/request.js`

```javascript
import axios from "axios";
import { ElMessage } from "element-plus";
import router from "../router";

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api",
  timeout: 10000,
});

request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

request.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          ElMessage.error("请先登录");
          localStorage.removeItem("token");
          router.push("/login");
          break;
        case 403:
          ElMessage.error("没有权限");
          break;
        case 404:
          ElMessage.error("请求的资源不存在");
          break;
        case 500:
          ElMessage.error("服务器错误");
          break;
        default:
          ElMessage.error("请求失败");
          break;
      }
    } else {
      ElMessage.error("网络错误");
    }

    return Promise.reject(error);
  }
);

export default request;
```

---

### 7.3 新建 `lyhblog-frontend/src/api/ai.js`

```javascript
import request from "../utils/request";

export function ApiAIWritingAssistant(data) {
  return request.post("/ai/writing-assistant/", data);
}
```

---

### 7.4 新建 `lyhblog-frontend/src/components/admin/AIAssistantDrawer.vue`

```vue
<template>
  <el-drawer
    :model-value="modelValue"
    title="AI 写作助手"
    size="520px"
    @close="handleClose"
  >
    <div class="assistant-drawer">
      <el-form :model="queryForm" label-width="88px">
        <el-form-item label="主题">
          <el-input
            v-model="queryForm.topic"
            placeholder="比如：Django + Vue 博客项目部署实战"
          />
        </el-form-item>

        <el-form-item label="关键词">
          <el-input
            v-model="queryForm.keywordText"
            placeholder="多个关键词用英文逗号分隔"
          />
        </el-form-item>

        <el-form-item label="读者">
          <el-input
            v-model="queryForm.audience"
            placeholder="比如：准备做个人博客项目的初学者"
          />
        </el-form-item>

        <el-form-item label="风格">
          <el-select v-model="queryForm.tone" placeholder="选择风格">
            <el-option label="实战型" value="实战型" />
            <el-option label="教程型" value="教程型" />
            <el-option label="总结型" value="总结型" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleGenerate">
            生成建议
          </el-button>
        </el-form-item>
      </el-form>

      <div v-if="result" class="result-panel">
        <div class="panel-header">
          <span>生成结果</span>
          <el-button type="success" plain @click="applyAll">应用全部</el-button>
        </div>

        <div class="result-block">
          <div class="result-label">
            标题
            <el-button link type="primary" @click="applyPartial({ title: result.title })">
              应用
            </el-button>
          </div>
          <div class="result-text">{{ result.title }}</div>
        </div>

        <div class="result-block">
          <div class="result-label">
            摘要
            <el-button link type="primary" @click="applyPartial({ summary: result.summary })">
              应用
            </el-button>
          </div>
          <div class="result-text">{{ result.summary }}</div>
        </div>

        <div class="result-block">
          <div class="result-label">
            分类建议
            <el-button
              link
              type="primary"
              :disabled="!result.category_id"
              @click="applyPartial({ category_id: result.category_id })"
            >
              应用
            </el-button>
          </div>
          <div class="result-text">
            {{ result.category_name || "未匹配到现有分类" }}
          </div>
        </div>

        <div class="result-block">
          <div class="result-label">
            标签建议
            <el-button
              link
              type="primary"
              :disabled="!result.matched_tag_ids?.length"
              @click="applyPartial({ matched_tag_ids: result.matched_tag_ids })"
            >
              应用已匹配标签
            </el-button>
          </div>

          <div class="tag-list">
            <el-tag
              v-for="tag in result.tag_names"
              :key="tag"
              class="tag-item"
              type="info"
            >
              {{ tag }}
            </el-tag>
          </div>

          <div v-if="unmatchedTagNames.length" class="tip-text">
            以下标签未匹配到现有标签，需要你手动新增：{{ unmatchedTagNames.join("、") }}
          </div>
        </div>

        <div class="result-block">
          <div class="result-label">提纲建议</div>
          <ol class="outline-list">
            <li v-for="item in result.outline" :key="item">{{ item }}</li>
          </ol>
        </div>

        <div class="result-block">
          <div class="result-label">
            Markdown 草稿
            <el-button
              link
              type="primary"
              @click="applyPartial({ content: result.draft_markdown })"
            >
              应用到正文
            </el-button>
          </div>
          <el-input
            :model-value="result.draft_markdown"
            type="textarea"
            :rows="12"
            readonly
          />
        </div>
      </div>
    </div>
  </el-drawer>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { ElMessage } from "element-plus";
import { ApiAIWritingAssistant } from "../../api/ai";

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  articleForm: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["update:modelValue", "apply"]);

const loading = ref(false);
const result = ref(null);
const queryForm = ref({
  topic: "",
  keywordText: "",
  audience: "",
  tone: "实战型",
});

watch(
  () => props.modelValue,
  (visible) => {
    if (visible && !queryForm.value.topic && props.articleForm.title) {
      queryForm.value.topic = props.articleForm.title;
    }
  }
);

const unmatchedTagNames = computed(() => {
  if (!result.value) return [];
  const matchedSet = new Set(result.value.matched_tag_names || []);
  return (result.value.tag_names || []).filter((item) => !matchedSet.has(item));
});

function handleClose() {
  emit("update:modelValue", false);
}

async function handleGenerate() {
  if (!queryForm.value.topic && !props.articleForm.content && !props.articleForm.summary) {
    ElMessage.warning("请先输入主题，或先写一点草稿内容。");
    return;
  }

  loading.value = true;

  try {
    const payload = {
      topic: queryForm.value.topic,
      keywords: queryForm.value.keywordText
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean),
      audience: queryForm.value.audience,
      tone: queryForm.value.tone,
      current_title: props.articleForm.title,
      current_summary: props.articleForm.summary,
      current_content: props.articleForm.content,
    };

    const res = await ApiAIWritingAssistant(payload);
    if (res.data.code === 200) {
      result.value = res.data.data;
      ElMessage.success("AI 建议已生成");
    } else {
      ElMessage.error(res.data.message || "AI 生成失败");
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "AI 生成失败");
  } finally {
    loading.value = false;
  }
}

function applyPartial(payload) {
  emit("apply", payload);
}

function applyAll() {
  if (!result.value) return;

  emit("apply", {
    title: result.value.title,
    summary: result.value.summary,
    category_id: result.value.category_id,
    matched_tag_ids: result.value.matched_tag_ids,
    content: result.value.draft_markdown,
  });
}
</script>

<style scoped>
.assistant-drawer {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.result-panel {
  border-top: 1px solid #ebeef5;
  padding-top: 16px;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  font-weight: 600;
}

.result-block {
  margin-bottom: 18px;
}

.result-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
  font-weight: 600;
}

.result-text {
  color: #303133;
  line-height: 1.7;
  white-space: pre-wrap;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  margin-right: 0;
}

.outline-list {
  padding-left: 18px;
  color: #303133;
  line-height: 1.8;
}

.tip-text {
  margin-top: 8px;
  color: #909399;
  font-size: 13px;
}
</style>
```

---

### 7.5 替换 `lyhblog-frontend/src/views/admin/ArticleEdit.vue`

```vue
<template>
  <div class="article-edit">
    <div class="page-header">
      <h2>{{ isEdit ? "编辑文章" : "新增文章" }}</h2>
      <el-button type="primary" plain @click="aiDrawerVisible = true">
        AI 助手
      </el-button>
    </div>

    <el-form :model="form" label-width="88px">
      <el-form-item label="标题">
        <el-input v-model="form.title" placeholder="请输入文章标题" />
      </el-form-item>

      <el-form-item label="分类">
        <el-select v-model="form.category_id" placeholder="请选择分类" clearable>
          <el-option
            v-for="cat in categories"
            :key="cat.id"
            :label="cat.name"
            :value="cat.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="标签">
        <el-select v-model="form.tags" multiple placeholder="请选择标签" clearable>
          <el-option
            v-for="tag in tags"
            :key="tag.id"
            :label="tag.name"
            :value="tag.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="摘要">
        <el-input
          v-model="form.summary"
          type="textarea"
          :rows="4"
          placeholder="请输入文章摘要"
        />
      </el-form-item>

      <el-form-item label="正文">
        <el-input
          v-model="form.content"
          type="textarea"
          :rows="16"
          placeholder="请输入文章正文"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSubmit">保存</el-button>
        <el-button @click="goBack">取消</el-button>
      </el-form-item>
    </el-form>

    <AIAssistantDrawer
      v-model="aiDrawerVisible"
      :article-form="form"
      @apply="handleApplyAiResult"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import AIAssistantDrawer from "../../components/admin/AIAssistantDrawer.vue";
import {
  ApiArticleAdd,
  ApiArticleDetail,
  ApiArticleUpdate,
  ApiCategoryList,
  ApiTagList,
} from "../../api/article";

const route = useRoute();
const router = useRouter();

const isEdit = computed(() => !!route.params.id);
const aiDrawerVisible = ref(false);

const form = ref({
  title: "",
  category_id: null,
  tags: [],
  summary: "",
  content: "",
});

const categories = ref([]);
const tags = ref([]);

async function loadOptions() {
  try {
    const [categoryRes, tagRes] = await Promise.all([ApiCategoryList(), ApiTagList()]);

    if (categoryRes.data.code === 200) {
      categories.value = categoryRes.data.data;
    }
    if (tagRes.data.code === 200) {
      tags.value = tagRes.data.data;
    }
  } catch (error) {
    ElMessage.error("分类或标签加载失败");
  }
}

async function loadArticleDetail() {
  if (!isEdit.value) return;

  try {
    const res = await ApiArticleDetail(route.params.id);
    if (res.data.code === 200) {
      const article = res.data.data;
      form.value = {
        title: article.title || "",
        category_id: article.category?.id || null,
        tags: article.tags ? article.tags.map((item) => item.id) : [],
        summary: article.summary || "",
        content: article.content || "",
      };
    }
  } catch (error) {
    ElMessage.error("文章详情加载失败");
  }
}

function handleApplyAiResult(payload) {
  if (typeof payload.title === "string") {
    form.value.title = payload.title;
  }
  if (typeof payload.summary === "string") {
    form.value.summary = payload.summary;
  }
  if (payload.category_id !== undefined && payload.category_id !== null) {
    form.value.category_id = payload.category_id;
  }
  if (Array.isArray(payload.matched_tag_ids) && payload.matched_tag_ids.length) {
    form.value.tags = [...new Set(payload.matched_tag_ids)];
  }
  if (typeof payload.content === "string" && payload.content.trim()) {
    form.value.content = payload.content;
  }

  ElMessage.success("AI 建议已应用到表单");
}

async function handleSubmit() {
  if (!form.value.title || !form.value.content) {
    ElMessage.warning("标题和内容不能为空");
    return;
  }

  try {
    if (isEdit.value) {
      const res = await ApiArticleUpdate({
        id: route.params.id,
        ...form.value,
      });
      if (res.data.code === 200) {
        ElMessage.success("文章修改成功");
        router.push("/admin/article");
      }
      return;
    }

    const res = await ApiArticleAdd(form.value);
    if (res.data.code === 200) {
      ElMessage.success("文章新增成功");
      router.push("/admin/article");
    }
  } catch (error) {
    ElMessage.error(isEdit.value ? "文章修改失败" : "文章新增失败");
  }
}

function goBack() {
  router.back();
}

onMounted(async () => {
  await loadOptions();
  await loadArticleDetail();
});
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
</style>
```

---

## 8. 本地接入步骤

### 后端

```bash
cd D:\Monkey-blog\lyhblog-backend
venv\Scripts\activate
pip install -r requirements.txt
```

手动创建：

- `lyhblog-backend/.env`

内容参考：

```env
OPENAI_API_KEY=你的key
OPENAI_MODEL=gpt-5.4
OPENAI_TIMEOUT=60
```

然后启动后端：

```bash
python manage.py runserver
```

### 前端

```bash
cd D:\Monkey-blog\lyhblog-frontend
npm.cmd install
```

手动创建：

- `lyhblog-frontend/.env.development`

内容：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

启动前端：

```bash
npm.cmd run dev
```

---

## 9. 联调检查清单

你可以按这个顺序自测：

1. 后台登录成功
2. 进入 `/admin/article/add`
3. 页面右上角能看到 `AI 助手` 按钮
4. 打开抽屉
5. 输入主题和关键词
6. 点击 `生成建议`
7. 成功返回标题、摘要、标签、提纲、草稿
8. 点击 `应用全部`
9. 表单字段自动被填充
10. 点击 `保存`

如果失败，先查这几个点：

- `.env` 是否真的创建了
- `OPENAI_API_KEY` 是否正确
- 后端是否安装了 `openai`
- 前端 `VITE_API_BASE_URL` 是否指向正确地址
- 当前登录用户是否是管理员，因为后端接口用了 `IsAdminUser`

---

## 10. 这版能怎么写进简历

项目名称建议写成：

`前后端分离内容管理系统 + AI 写作助手 | Django REST Framework + Vue3 + OpenAI API`

项目亮点可写成：

- 基于 Django REST Framework 与 Vue3 实现前后端分离内容管理系统，支持文章发布、分类标签管理、评论管理与后台权限控制。
- 接入 OpenAI Responses API，在后台文章编辑页实现 AI 写作助手，支持根据主题自动生成标题、摘要、标签、文章提纲与 Markdown 草稿，并回填编辑表单。
- 在后端统一封装 Prompt、模型调用和结构化输出解析，避免前端暴露 API Key，提升系统安全性与可维护性。
- 结合现有分类和标签数据，对 AI 输出进行业务匹配与回填，形成完整的“生成建议 -> 表单应用 -> 保存文章”闭环。

---

## 11. 下一步怎么迭代

这版做完后，第二阶段你再考虑：

- 草稿润色助手
- 评论审核建议
- 站内知识问答
- AI 自动打标签
- 发布前质量检查

再往后，如果你真做成这种多步骤流程：

```text
检索历史文章 -> 生成提纲 -> 生成正文 -> 风险检查 -> 保存草稿
```

那时候再引入 `LangGraph` 才合适。

---

## 12. 注意事项

这份方案是按你当前仓库结构写的，但我**没有直接改动项目代码**，也**没有在你的仓库里执行实际联调**。所以你粘贴时要注意：

- 你本地文件如果还有编码问题，先别一口气全覆盖
- 建议一次只改一个文件
- 每改完一个文件就启动检查一次
- 如果报错，优先看导入路径和 `.env` 是否创建

如果你下一步要，我可以继续给你补一份：

`lyhblog-AI写作助手接入排错清单.md`

专门写常见报错和排查顺序。


