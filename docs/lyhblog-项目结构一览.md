# lyhblog 项目结构一览（发给 Gemini 看）

> 前后端分离个人博客，仿 POEMON；后端 Django + DRF，前端 Vue3 + Vite。

---

## 一、整体

- **仓库根目录**：`d:\Monkey-blog`
- **前端**：`lyhblog-frontend`（Vue3 + Vite + Vue Router + Pinia + Element Plus + axios）
- **后端**：`lyhblog-backend`（Django 6 + Django REST framework + MySQL）
- **文档**：`docs/` 下若干 .md（新建项目步骤、时间预估、对话记录与计划、POEMON 解读等）

---

## 二、前端结构（lyhblog-frontend）

```
lyhblog-frontend/
├── src/
│   ├── main.js              # 入口：createApp、Pinia、ElementPlus、router
│   ├── App.vue              # 根组件，<router-view />
│   ├── style.css
│   ├── router/
│   │   └── index.js         # Vue Router 4，createWebHistory
│   ├── api/
│   │   └── article.js       # 文章列表/详情/登录请求（axios）
│   ├── utils/
│   │   └── constant.js      # baseURL: http://127.0.0.1:8000/api
│   ├── views/
│   │   ├── Home.vue         # 首页，文章列表，跳详情 /article?id=xxx
│   │   ├── ArticleDetail.vue # 文章详情，query.id，getArticleById
│   │   └── login.vue        # 登录页，ApiLogin，存 token，redirect
│   ├── components/
│   │   └── HelloWorld.vue
│   └── assets/
```

**路由**：`/` 首页，`/article` 详情（query.id），`/login` 登录。  
**接口**：baseURL + `/article/listArticle/`（POST）、`/article/getArticleById/`（GET）、`/appone/login/`（POST）。

---

## 三、后端结构（lyhblog-backend）

```
lyhblog-backend/
├── manage.py
├── config/                  # 项目配置
│   ├── settings.py         # 数据库 MySQL、DRF、CORS、INSTALLED_APPS
│   ├── urls.py              # 根路由：admin/、api/ → blog.urls
│   ├── wsgi.py, asgi.py
├── blog/                    # 业务 app
│   ├── models.py            # Article（title, summary, content, create_time）
│   ├── serializers.py       # ArticleSerializer
│   ├── urls.py              # api 下路由：test/、article/listArticle/、article/getArticleById/、appone/login/
│   ├── views/               # 视图按模块拆分
│   │   ├── __init__.py      # 导出 ArticleListView, ArticleDetailView, LoginView, TestView
│   │   ├── article.py       # ArticleListView（POST，分页 current/size/total）、ArticleDetailView（GET，query id）
│   │   └── auth.py          # TestView（GET）、LoginView（POST，authenticate + Token）
│   ├── admin.py
│   └── migrations/
```

**API 约定**：列表 POST 收 `current`/`size`，返回 `code`、`data`、`total`；详情 GET 收 query `id`，返回 `code`、`data`；登录 POST 收 `account`/`password`，返回 `code`、`token`。

---

## 四、已实现功能

| 功能 | 前端 | 后端 |
|------|------|------|
| 文章列表 | Home.vue，POST listArticle，分页参数 | ArticleListView，分页，返回 total |
| 文章详情 | ArticleDetail.vue，GET getArticleById，query.id | ArticleDetailView，GET id |
| 登录 | login.vue，POST appone/login，存 token，redirect | LoginView，authenticate + DRF Token |

---

## 五、技术栈小结

- **前端**：Vue 3、Vite、Vue Router 4、Pinia、Element Plus、axios。  
- **后端**：Django 6、DRF、MySQL、rest_framework.authtoken、django-cors-headers。  
- **对接**：前端 `constant.baseURL` 指向 `http://127.0.0.1:8000/api`，后端 `path('api/', include('blog.urls'))`。

---

*此文档仅作结构一览，便于发给 Gemini 或他人快速了解项目。*
