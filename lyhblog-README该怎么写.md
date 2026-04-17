# lyhblog README 该怎么写

更新时间：2026-04-17
适用目录：`D:\Monkey-blog`
说明：这份文档是给你写仓库 README 用的，不是最终 README 成品，而是一个可以直接套用的结构稿。

## 1. README 的目标

你这个项目的 README 不该再写成“我做了个个人博客”。

更合理的定位是：

`前后端分离内容管理系统 + AI 写作助手`

别人点开仓库首页，要在 10 秒内看懂这几件事：

- 你做的是一个什么系统
- 技术栈是什么
- 有哪些功能
- 怎么启动
- AI 写作助手有什么价值
- 你解决了哪些实际问题

---

## 2. 推荐标题

你可以直接用：

```md
# lyhblog | 前后端分离内容管理系统 + AI 写作助手
```

或者：

```md
# lyhblog
## Django REST Framework + Vue3 内容管理系统与 AI 写作助手
```

---

## 3. README 推荐结构

直接按这个顺序写：

```md
# 项目标题

## 项目简介
## 技术栈
## 核心功能
## AI 写作助手
## 项目截图
## 项目结构
## 本地启动
## 环境变量说明
## 部署说明
## 后续计划
```

---

## 4. 可直接粘贴的 README 初稿

```md
# lyhblog | 前后端分离内容管理系统 + AI 写作助手

## 项目简介

lyhblog 是一个基于 Django REST Framework + Vue3 构建的前后端分离内容管理系统，支持文章发布、分类与标签管理、评论管理、后台权限控制等基础内容管理能力。

在此基础上，项目还接入了 AI 写作助手，支持根据主题自动生成文章标题、摘要、标签建议、提纲与 Markdown 草稿，并可在后台编辑页一键回填到表单中。

这个项目的目标不是做一个单纯的“个人博客页面”，而是做一个可展示、可部署、可写进简历的内容管理系统项目。

## 技术栈

### 后端

- Django 6
- Django REST Framework
- Token Authentication
- MySQL
- python-dotenv
- Gunicorn

### 前端

- Vue 3
- Vite
- Element Plus
- Vue Router
- Pinia
- Axios

### AI 能力

- Claude / Anthropic 兼容中转网关
- 后端统一封装 AI 请求
- 支持结构化写作建议生成

## 核心功能

- 用户注册与登录
- Token 鉴权
- 文章新增、编辑、删除、列表展示
- 分类管理
- 标签管理
- 评论管理
- 前台文章列表与文章详情页
- 后台文章编辑页 AI 写作助手

## AI 写作助手

AI 写作助手集成在后台文章编辑页中，支持：

- 输入主题生成标题
- 自动生成摘要
- 自动推荐标签
- 自动生成文章提纲
- 自动生成 Markdown 草稿
- 一键回填到文章表单

这部分能力通过 Django 后端统一调用 AI 网关完成，前端不直接暴露密钥。

## 项目截图

> 建议你后续补上以下截图：

- 首页
- 文章详情页
- 后台文章管理页
- 新增文章页
- AI 写作助手抽屉
- 登录页

## 项目结构

```text
D:\Monkey-blog
├─ lyhblog-backend
└─ lyhblog-frontend
```

## 本地启动

### 后端

```bash
cd lyhblog-backend
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

### 前端

```bash
cd lyhblog-frontend
npm.cmd install
npm.cmd run dev
```

## 环境变量说明

### 后端 `.env`

```env
ANTHROPIC_BASE_URL=你的网关地址
ANTHROPIC_AUTH_TOKEN=你的token
ANTHROPIC_MODEL=claude-sonnet-4-6
ANTHROPIC_TIMEOUT=60
```

### 前端 `.env.development`

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## 部署说明

项目可通过 Gunicorn + Nginx 进行部署。前端使用 `npm build` 构建后交由 Nginx 托管，后端使用 Gunicorn 提供接口服务。

## 后续计划

- 优化 AI 写作助手的错误处理和稳定性
- 完善 README 与截图展示
- 完成 Ubuntu / WSL 部署流程
- 增加更贴近简历场景的第二个项目
```

---

## 5. 你写 README 时最容易踩的坑

### 不要写成流水账

别写成：

- 今天学了什么
- 这个功能怎么加的
- 那个报错怎么修的

README 不是学习日志。

### 不要一直强调“个人博客”

你现在这个项目已经不只是“个人博客页面”了。

更好的表达是：

- 前后端分离内容管理系统
- 支持后台管理与 AI 写作辅助

### 不要漏截图

没有截图，仓库说服力会差很多。

### 不要只写技术名词

一定要把“做了什么”写清楚。

---

## 6. 你现在最该补的 README 内容

如果你今天只补 3 个部分，就先补：

1. 项目简介
2. 核心功能
3. AI 写作助手

然后再补：

4. 启动步骤
5. 截图

---

## 7. 一句话建议

你的 README 目标不是“显得学了很多”，而是让别人看完后知道：

**你做了一个可运行、可管理、可接 AI、可部署的内容管理系统。**
