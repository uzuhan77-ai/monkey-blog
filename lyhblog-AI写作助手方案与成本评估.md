# lyhblog AI 写作助手方案与成本评估

更新时间：2026-04-17
适用项目：`D:\Monkey-blog\lyhblog-backend` + `D:\Monkey-blog\lyhblog-frontend`
默认模型：`gpt-5.4`

## 1. 目标定位

这次不做多 Agent 平台，先做一个能真实接进你现有博客后台、能直接写进简历的 **AI 写作助手**。

第一版目标：

- 在后台新增一个 `AI 助手` 面板
- 输入主题或草稿后，自动生成：
  - 文章标题
  - 摘要
  - 标签建议
  - SEO 描述
  - 文章提纲
- 支持把结果一键填回文章编辑页
- 所有调用都经过你自己的 Django 后端，不在前端暴露 API Key

## 2. 为什么这个方向适合你

你现在的项目已经是一个前后端分离内容管理系统。加上 AI 写作助手以后，项目表达会更完整，能体现：

- Django 后端接口设计
- Vue 后台交互设计
- OpenAI API 接入
- Prompt 设计与结构化输出
- 成本控制与模型切换策略
- AI 功能和业务表单联动

## 3. 第一版不要上的东西

先不要上：

- `LangChain`
- `LangGraph`
- `CrewAI`
- 多 Agent 协作
- 浏览器自动操作 Agent

原因：

- 你现在最需要的是做出一个可解释、可演示、可部署的 AI 功能
- 当前业务是标准的“单次生成 + 结构化结果 + 回填表单”
- `Django + OpenAI Responses API` 就够了

## 4. 推荐技术方案

### 后端

- `Django`
- `djangorestframework`
- `openai` Python SDK
- OpenAI `Responses API`
- 你自己的业务函数封装

### 前端

- `Vue 3`
- `Element Plus`
- 后台文章编辑页新增 `AI 助手` 抽屉

### 模型建议

按 OpenAI 官方文档，当前最新推荐模型是 `gpt-5.4`。

建议你这样用：

- 默认模型：`gpt-5.4`
- 如果后面你觉得成本或延迟偏高，再切到：`gpt-5.4-mini`
- 简单高并发分类任务：`gpt-5.4-nano`

## 5. 可落地的第一版功能

### 5.1 文章创作助手

输入：主题、关键词、目标读者、文章方向

输出：

- 标题 `title`
- 摘要 `summary`
- 标签数组 `tags`
- SEO 描述 `seo_description`
- 提纲数组 `outline`

### 5.2 草稿润色助手

输入：你已经写好的草稿

输出：

- 标题优化建议
- 摘要优化建议
- 推荐标签
- 段落结构建议
- 是否适合发布的简短建议

### 5.3 评论审核建议

输入：评论正文

输出：

- 是否疑似垃圾评论
- 是否含攻击性/低质量内容
- 后台审核建议

## 6. 成本评估

以下价格按我在 2026-04-17 查到的 OpenAI 官方模型页与最新模型指南整理。

### 6.1 模型价格

- `gpt-5.4`：输入 `$2.50 / 1M tokens`，输出 `$15 / 1M tokens`
- `gpt-5.4-mini`：输入 `$0.75 / 1M tokens`，输出 `$4.50 / 1M tokens`
- `gpt-5.4-nano`：输入 `$0.20 / 1M tokens`，输出 `$1.25 / 1M tokens`

### 6.2 File Search / Vector Store 价格

- Vector store 总存储 `1 GB` 以内免费
- 超过 `1 GB` 后：`$0.10 / GB / day`

### 6.3 你的第一版大概会花多少钱

假设一次典型请求：

- 输入：1500 tokens
- 输出：800 tokens

按 `gpt-5.4` 估算：

- 输入成本：`1500 / 1,000,000 × 2.50 ≈ $0.00375`
- 输出成本：`800 / 1,000,000 × 15 ≈ $0.012`
- 单次总成本：约 `$0.01575`

也就是：

- 单次大约 `$0.016`
- 100 次大约 `$1.58`
- 1000 次大约 `$15.75`

按 `gpt-5.4-mini` 估算：

- 输入成本：`1500 / 1,000,000 × 0.75 ≈ $0.001125`
- 输出成本：`800 / 1,000,000 × 4.50 ≈ $0.0036`
- 单次总成本：约 `$0.004725`

也就是：

- 单次不到 `$0.005`
- 100 次大约 `$0.47`
- 1000 次大约 `$4.73`

结论：

- 你如果是“简历项目 + 个人演示”，直接上 `gpt-5.4` 没问题
- 如果后面你开始频繁调用，再降到 `gpt-5.4-mini`
- 第一版根本不需要为了成本先把模型压得太低

## 7. 成本控制建议

- 默认模型用 `gpt-5.4`
- 只返回结构化结果，不要让模型长篇解释
- 限制提纲条数、标签数量、摘要长度
- 后台加调用频率限制
- 记录每次调用的输入长度和返回长度
- 如果后面功能增多，再把部分任务降到 `gpt-5.4-mini`

## 8. 环境变量建议

### 后端 `.env.example`

```env
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-5.4
OPENAI_TIMEOUT=60
```

如果后端还没完成环境变量改造，建议一起补：

```env
DJANGO_SECRET_KEY=replace-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=lyhblog
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 前端 `.env.example`

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## 9. 简历怎么写

项目名称建议写成：

`前后端分离内容管理系统 + AI 写作助手 | Django REST Framework + Vue3 + OpenAI API`

项目亮点示例：

- 基于 Django REST Framework 与 Vue3 实现前后端分离内容管理系统，支持文章发布、分类标签管理、评论管理与后台权限控制。
- 接入 OpenAI Responses API，在后台文章编辑页实现 AI 写作助手，支持根据主题自动生成标题、摘要、标签、文章提纲与 Markdown 草稿，并回填编辑表单。
- 在后端统一封装 Prompt、模型调用和结构化输出解析，避免前端暴露 API Key，提升系统安全性与可维护性。
- 结合模型分级和结构化输出策略，对 AI 生成成本进行控制，并形成“生成建议 -> 表单应用 -> 保存文章”的完整业务闭环。

## 10. 最终建议

如果你现在明确就是想把项目做得更强、更像样，那就：

- 第一版直接上 `gpt-5.4`
- 不上 `LangChain / LangGraph / CrewAI`
- 先把写作助手完整做出来
- 后面如果成本上来，再降到 `gpt-5.4-mini`
- 再往后如果流程复杂了，再考虑 `LangGraph`

## 11. 参考资料

- Models: https://developers.openai.com/api/docs/models
- Latest GPT-5.4: https://developers.openai.com/api/docs/guides/latest-model
- Responses API: https://platform.openai.com/docs/api-reference/responses
- Tools / Function calling: https://platform.openai.com/docs/guides/tools?api-mode=responses
- File Search: https://platform.openai.com/docs/guides/tools-file-search
- Retrieval: https://platform.openai.com/docs/guides/retrieval
