# API Lab 可行性方案

## 1. 项目定位

API Lab 是一个面向学习和求职展示的接口对接练习平台，重点不是做复杂业务，而是系统性补齐后端开发中常见的能力：

- HTTP 接口设计与调用
- JSON 参数校验、格式化、字段提取和结构转换
- 第三方接口对接、超时、错误处理和请求日志
- Webhook 数据接收和排查
- Redis 缓存、限流和临时状态管理
- Playwright 自动化流程验证
- Docker Compose 本地部署

这个项目可以独立存在，也可以被现有博客后台调用。博客继续保持纯净，API Lab 作为工具服务沉淀通用能力。

## 2. 为什么适合现在做

现有 blog 项目已经覆盖文章、分类、标签、评论、后台和 AI 助手雏形，但核心仍是内容管理系统，容易被看成 CRUD 项目。

API Lab 更贴近日常后端工作：

- 对接第三方接口时要处理 method、headers、query、body、status code、timeout、retry、error。
- Webhook 是支付、消息通知、开放平台、企业系统对接里的常见模式。
- JSON 校验和转换是接口开发的基本功。
- Redis、Docker、Playwright 都是主流工具，能自然放进项目里。

这个项目的目标不是炫技，而是把主流工具用在真实问题上。

## 3. 技术栈选择

### 后端

- FastAPI：适合做 API 工具服务，自带 OpenAPI/Swagger 文档。
- Pydantic：练 JSON 入参、出参和字段校验。
- httpx：用于请求第三方接口，练超时、异常、headers、body。
- SQLAlchemy：连接 MySQL，管理请求日志、Webhook 记录等数据。
- pytest：写接口测试和服务函数测试。

### 数据库

使用已有 MySQL。

不先用 SQLite 的原因：

- 你本机已经有 MySQL，直接贴近真实后端环境。
- 可以顺便练表设计、索引、分页查询和连接配置。
- 后续 Docker Compose 也能把 MySQL 放进去，形成完整服务栈。

### Redis

用于三个明确场景：

- 接口限流：同一 IP 或同一 token 每分钟限制请求次数。
- GET 请求缓存：相同 URL + headers 在短时间内复用结果。
- 临时任务状态：保存自动化测试或长请求的状态。

### 前端

- Vue 3
- TypeScript
- Element Plus
- Axios

前端不急着一开始做。第一阶段先用 FastAPI 自带 `/docs` 调试接口。

### 自动化

- Playwright

主要用于自动化测试和流程验证，不用于灰色采集。比如自动登录自己的 blog 后台、新建文章、搜索文章、打开详情页并截图。

### 部署

- Docker Compose

最终目标是一条命令启动：

```text
FastAPI + MySQL + Redis + 前端
```

## 4. 项目边界

### 第一版要做

- 第三方接口请求代理
- 请求/响应日志保存
- JSON 格式化、校验、字段提取
- Webhook 接收和记录
- Redis 限流
- 基础接口测试
- README 和接口文档

### 第一版不做

- 不做 RAG 知识库
- 不做复杂用户权限系统
- 不做分布式爬虫
- 不做 JS 逆向、IP 池、账号池
- 不做 Kubernetes
- 不做复杂低代码平台

先把小而完整的工程做扎实。

## 5. 核心功能设计

### 5.1 接口请求代理

接口：

```text
POST /api/requests/send
GET  /api/requests
GET  /api/requests/{id}
```

请求示例：

```json
{
  "method": "GET",
  "url": "https://api.github.com/repos/vuejs/core",
  "headers": {
    "Accept": "application/json"
  },
  "query": {},
  "body": null,
  "timeout": 10
}
```

返回示例：

```json
{
  "code": 200,
  "data": {
    "id": 1,
    "status_code": 200,
    "duration_ms": 342,
    "response_headers": {},
    "response_body": {},
    "error": null
  },
  "message": "request completed"
}
```

学习重点：

- URL 校验
- method 限制
- headers 处理
- query 和 body 区分
- timeout
- HTTP 错误和网络错误
- JSON 和非 JSON 响应处理
- 请求日志入库

### 5.2 JSON 工具

接口：

```text
POST /api/json/format
POST /api/json/validate
POST /api/json/extract
POST /api/json/diff
```

功能：

- 格式化 JSON
- 判断 JSON 是否合法
- 根据路径提取字段，例如 `data.user.name`
- 对比两个 JSON 的字段差异

学习重点：

- JSON 类型：object、array、string、number、boolean、null
- 字段缺失和类型不一致
- Pydantic 校验错误如何返回给前端
- 统一错误响应结构

### 5.3 Webhook 接收器

接口：

```text
POST /webhook/{token}
GET  /api/webhooks
GET  /api/webhooks/{id}
```

功能：

- 外部系统 POST 数据到 `/webhook/{token}`
- 记录 headers、query、body、来源 IP、接收时间
- 后台页面可以查看收到的 Webhook 数据

学习重点：

- 接收未知 JSON
- 记录原始请求
- token 路由
- headers 和 body 排查
- Webhook 重放和调试

### 5.4 Redis 限流和缓存

限流示例：

```text
同一 IP 每分钟最多调用 /api/requests/send 30 次
```

缓存示例：

```text
相同 GET 请求 60 秒内直接返回缓存结果
```

学习重点：

- Redis key 设计
- TTL
- 计数器
- 缓存命中和失效
- 缓存不适合存什么

### 5.5 Playwright 自动化验证

接口：

```text
POST /api/automation/blog-smoke-test
GET  /api/automation/runs
```

流程：

1. 打开自己的 blog 后台登录页
2. 登录
3. 新建测试文章
4. 搜索测试文章
5. 打开文章详情
6. 截图
7. 返回每一步是否成功

学习重点：

- 浏览器自动化
- 等待页面元素
- 截图
- 自动化报告
- 真实业务流程验证

## 6. 数据库初步设计

### api_request_logs

保存第三方接口请求日志。

字段建议：

- id
- method
- url
- request_headers
- request_query
- request_body
- status_code
- response_headers
- response_body
- duration_ms
- error_message
- created_at

建议索引：

- created_at
- status_code
- method

### webhook_events

保存 Webhook 接收记录。

字段建议：

- id
- token
- source_ip
- request_headers
- request_query
- request_body
- created_at

建议索引：

- token
- created_at

### automation_runs

保存自动化测试记录。

字段建议：

- id
- name
- status
- steps
- screenshot_path
- error_message
- started_at
- finished_at

建议索引：

- status
- started_at

## 7. 目录结构

建议目录：

```text
D:\Monkey-blog\api-lab
├─ backend
│  ├─ app
│  │  ├─ main.py
│  │  ├─ core
│  │  │  ├─ config.py
│  │  │  └─ database.py
│  │  ├─ models
│  │  ├─ schemas
│  │  ├─ api
│  │  ├─ services
│  │  └─ tests
│  ├─ requirements.txt
│  └─ .env.example
├─ frontend
├─ docs
│  └─ API-Lab-可行性方案.md
├─ docker-compose.yml
└─ README.md
```

## 8. 分阶段计划

### 第 1 阶段：后端最小版本

目标：FastAPI 能跑，能通过 `/docs` 调试接口。

任务：

- 创建 FastAPI 项目
- 配置 MySQL 连接
- 创建请求日志表
- 实现 `/health`
- 实现 `/api/requests/send`
- 实现 `/api/requests` 和详情
- 写 3 个 pytest 测试

验收：

- 能请求 GitHub API 或公开测试 API
- 请求和响应能入库
- 出错时能保存错误信息
- `/docs` 中能看到接口说明

### 第 2 阶段：JSON 工具和 Webhook

目标：补齐接口对接中最常见的数据处理能力。

任务：

- JSON validate
- JSON format
- JSON extract
- Webhook 接收
- Webhook 列表和详情

验收：

- 能提交一段非法 JSON 并返回清晰错误
- 能提取嵌套字段
- 能接收任意 Webhook 请求并保存

### 第 3 阶段：Redis

目标：把 Redis 用在真实场景，而不是只会启动。

任务：

- 配置 Redis
- 对请求代理接口做限流
- 对 GET 请求做短缓存
- 记录缓存是否命中

验收：

- 超过限流次数返回 429
- 相同 GET 请求第二次明显更快
- Redis key 有清晰命名和 TTL

### 第 4 阶段：前端管理页

目标：做一个简单工具界面，不追求花哨。

页面：

- 请求发送页
- 请求历史页
- JSON 工具页
- Webhook 记录页

验收：

- 不用打开 Swagger 也能使用核心功能
- 能查看请求详情和响应 JSON
- 能筛选状态码和时间

### 第 5 阶段：Playwright 自动化

目标：展示自动化流程验证能力。

任务：

- 写一个 blog smoke test 脚本
- 后端接口触发脚本
- 保存运行结果和截图

验收：

- 能自动打开 blog
- 能完成一条核心流程
- 能返回步骤结果和截图路径

### 第 6 阶段：Docker Compose

目标：项目可以一键启动。

服务：

- backend
- frontend
- mysql
- redis

验收：

```text
docker compose up -d
```

后可以访问：

- FastAPI docs
- 前端页面
- MySQL
- Redis

## 9. 和现有 blog 的关系

API Lab 不直接改现有 blog。

后续可以用两种方式复用：

### 方式一：前端直接调用

blog 后台前端调用 API Lab：

```text
Vue blog admin -> API Lab
```

适合 AI 写作助手、JSON 工具、自动化测试按钮。

### 方式二：Django 后端中转

Django 后端调用 API Lab：

```text
Vue blog admin -> Django -> API Lab
```

适合需要权限控制、保存结果到 blog 数据库的功能。

第一版建议先独立做 API Lab，不急着接回 blog。

## 10. 风险和控制

### 风险：功能做散

控制：

- 第一版只做请求代理、JSON 工具、Webhook。
- Redis 和 Playwright 放后面。

### 风险：前端拖慢进度

控制：

- 第一阶段只用 Swagger `/docs` 调接口。
- 后端稳定后再做前端。

### 风险：数据库表设计过度

控制：

- 先只存 JSON 文本字段。
- 等查询需求明确后再拆表。

### 风险：Playwright 环境复杂

控制：

- 先写独立脚本。
- 跑通后再接后端接口。

## 11. 求职价值

这个项目可以体现：

- FastAPI 接口开发
- Pydantic 数据校验
- 第三方接口对接
- MySQL 表设计和分页查询
- Redis 限流和缓存
- Webhook 调试
- Playwright 自动化测试
- Docker Compose 部署
- pytest 测试意识

简历表述：

> 基于 FastAPI 开发 API 对接与 Webhook 调试平台，支持第三方接口请求代理、请求响应日志、JSON 校验与字段提取、Webhook 数据接收、Redis 限流与缓存、Playwright 自动化流程验证，并使用 Docker Compose 完成多服务部署。

## 12. 第一周执行计划

### Day 1

- 创建项目结构
- 初始化 FastAPI
- 写 `/health`
- 配置 `.env`

### Day 2

- 配置 MySQL
- 建 `api_request_logs` 表
- 写数据库连接

### Day 3

- 写请求发送接口
- 支持 GET/POST
- 保存请求和响应

### Day 4

- 完善错误处理
- 处理 timeout、无效 URL、非 JSON 响应

### Day 5

- 写请求历史和详情接口
- 支持分页

### Day 6

- 写 pytest 测试
- 补 README

### Day 7

- 整理接口文档
- 复盘第一阶段问题
- 决定是否进入 JSON 工具模块

## 13. 当前结论

API Lab 可行，且比继续给 blog 堆功能更适合补能力。

推荐启动方式：

1. 先不碰复杂前端。
2. 先用 FastAPI + MySQL 做后端 MVP。
3. 用 `/docs` 练接口和 JSON。
4. 后续再逐步加入 Redis、前端、Playwright、Docker Compose。

