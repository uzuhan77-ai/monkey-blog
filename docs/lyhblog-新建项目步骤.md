# lyhblog 新建项目步骤（仿照 POEMON 写自己的博客）

> 只给操作顺序和指令，不直接生成代码；按步做，用 PyCharm 写后端、Cursor 写前端。  
> **技术栈与作者一致**：后端用 **MySQL** + **Django REST framework**（DRF），接口用 DRF 的视图和 `Response` 写。

---

## 一、在 Monkey-blog 下建好两个空项目目录

在 **d:\Monkey-blog** 里新建两个文件夹：

- **lyhblog-backend**（Django 后端，用 PyCharm 打开）
- **lyhblog-frontend**（Vue3 前端，用 Cursor 打开）

名字可改成 `lyhblog-server` / `lyhblog-web` 等，只要前后端各一个、自己能分清即可。

---

## 二、后端（PyCharm / 命令行）

在 **lyhblog-backend** 里按顺序做：

### 1. 建虚拟环境

- 在项目根目录执行：`python -m venv venv`
- 激活：Windows 下 `venv\Scripts\activate`，看到命令行前有 `(venv)` 即可。

### 2. 装 Django 和 DRF

- `pip install django djangorestframework django-cors-headers mysqlclient`
- 装完后执行：`pip freeze > requirements.txt` 生成依赖文件。

### 3. 创建 Django 项目

- 在 **lyhblog-backend** 根目录执行：  
  `django-admin startproject config .`
- 会多出 `config` 文件夹（放 settings、urls）和 `manage.py`，项目根仍是 lyhblog-backend。

### 4. 创建业务 app

- 执行：`python manage.py startapp blog`（或你喜欢的名字，如 `core`）。
- 后面模型、视图、接口都先写在这个 app 里，不要一上来就建很多 app。

### 5. 在 settings 里要做的事

- 在 `INSTALLED_APPS` 里加上：`rest_framework`、`rest_framework.authtoken`、`corsheaders`、你的 `blog`（和 POEMON 作者一样用 DRF）。
- 在 `MIDDLEWARE` 里加上 `corsheaders` 的中间件（查 django-cors-headers 文档，一般是 `CorsMiddleware` 放最上）。
- 配好 `DATABASES` 用 **MySQL**（和作者一致）：`ENGINE: django.db.backends.mysql`，`NAME`、`USER`、`PASSWORD`、`HOST`、`PORT` 填你自己本地的 MySQL。需先在 MySQL 里建好一个库（如 `lyhblog`），NAME 填这个库名。
- 改 `SECRET_KEY`（可先用开发用的一串随机字符），`ALLOWED_HOSTS` 里加 `'*'` 或 `'localhost'` 方便本地调试。
- （可选）配 `REST_FRAMEWORK`：例如 `DEFAULT_AUTHENTICATION_CLASSES` 用 `TokenAuthentication`、`DEFAULT_PERMISSION_CLASSES` 按需设；测试接口阶段可先 `AllowAny`，后面做登录再收紧。

### 6. 总路由

- 在 `config/urls.py` 里用 `include` 把以 `api/` 开头的路径指到你 blog 的 urls（例如 `path('api/', include('blog.urls'))`）。
- 在 blog 里新建 `urls.py`，先写一条测试路由。视图用 **DRF** 写（例如 `@api_view(['GET'])` 或 `APIView`，返回 `Response({"ok": True})`），用 `python manage.py runserver` 跑起来，浏览器访问确认能返回 JSON。

到这里，后端是「空壳 + 能响应的 API 根」，不要求马上有文章、用户，先把项目跑通。

---

## 三、前端（Cursor）

在 **lyhblog-frontend** 里按顺序做：

### 1. 用 Vite 创建 Vue3 项目

- 在 **lyhblog-frontend** 目录下执行：  
  `npm create vite@latest . -- --template vue`
- 选 Vue、JavaScript 即可（不需要 TypeScript 可先不选）。
- 若提示目录非空，就先建好空文件夹再进去执行，或先 `npm create vite@latest lyhblog-frontend -- --template vue` 再把生成的内容挪到你要的目录。

### 2. 安装依赖

- `npm install`
- 再装：`npm install vue-router@4 pinia axios element-plus`（和 POEMON 类似的一套）。

### 3. 确认能跑

- `npm run dev`，浏览器能打开 Vite 默认页面即可。

### 4. 做「最小路由 + 请求」

- 在 `src` 下建 `router/index.js`，用 Vue Router 4 的 `createRouter`、`createWebHistory`，先配一条根路径 `/` 指向一个首页组件。
- 在 `main.js` 里 `app.use(router)`、`app.use(createPinia())`。
- 建一个 `src/utils/constant.js`，里面对 `baseURL` 赋值为你的后端地址（例如 `http://127.0.0.1:8000/api`）。
- 用 axios 封装一个请求函数（或简单写一个 `axios.get(baseURL + '/你后端那条测试路径')`），在首页里调一次，能在浏览器控制台看到后端返回的 JSON 即可。

这样前端是「Vue3 + Vite + 路由 + 能访问你后端 API」，不要求页面好看，先打通前后端。

---

## 四、建议的推进顺序（只做指令，不写具体代码）

按这个顺序一步步做，每步只做这一件事，做完再下一步：

| 步骤 | 内容 |
|------|------|
| 1 | **目录**：在 d:\Monkey-blog 下建好 lyhblog-backend、lyhblog-frontend。 |
| 2 | **后端空项目**：虚拟环境 → 装包 → startproject → startapp → settings/urls 配好 → 一条测试 API → runserver 能访问。 |
| 3 | **前端空项目**：Vite 创建 Vue3 → 装 vue-router、pinia、axios、element-plus → 配一条路由 → 配 baseURL → 请求后端测试 API → 能收到 JSON。 |
| 4 | **第一个真实功能**：在后端 blog 里做「文章列表」接口（一条 GET，用 DRF 写，可先返回假数据或从 MySQL 读一张简单表），前端做一个「文章列表」页，调这个接口并显示。 |
| 5 | 再往后：文章详情、分类、评论、登录注册等，每块都先在后端加接口，再在前端加页面和请求。 |

---

## 四（续）、步骤 4 详细说明：做「文章列表」功能

### 1. 先确认前后端已连通（如果还没测试）

- **后端**：在 `lyhblog-backend` 目录下运行 `python manage.py runserver`（确保 MySQL 已启动且数据库已创建）
- **前端**：在 `lyhblog-frontend` 目录下运行 `npm run dev`
- 在前端页面点击测试按钮，看能否收到后端返回的 JSON（如 `{'message':'hello', 'code':200}`）

### 2. 后端：创建文章模型和列表接口

**2.1 在 `blog/models.py` 里写 Article 模型**

- 字段至少包含：`title`（标题，CharField）、`content`（内容，TextField）、`created_at`（创建时间，DateTimeField，auto_now_add=True）
- 可选字段：`updated_at`（更新时间）、`author`（作者，ForeignKey 到 User，或先 CharField）、`is_published`（是否发布，BooleanField）

**2.2 执行数据库迁移**

- `python manage.py makemigrations`（生成迁移文件）
- `python manage.py migrate`（应用到 MySQL）

**2.3 在 `blog/views.py` 里写 ArticleListView**

- 用 DRF 的 `APIView` 或 `@api_view(['GET'])`
- 返回文章列表（可先返回假数据，如 `[{'id': 1, 'title': '测试文章', 'content': '...'}]`，或从 MySQL 读：`Article.objects.all()`）
- 返回格式用 `Response({'code': 200, 'data': [...]})`

**2.4 在 `blog/urls.py` 里加路由**

- 例如：`path('articles/', ArticleListView.as_view(), name='article-list')`
- 访问路径会是 `/api/articles/`

### 3. 前端：创建文章列表页面

**3.1 建 `src/router/index.js`（如果还没有）**

- 用 Vue Router 4 的 `createRouter`、`createWebHistory`
- 配一条路由：`path: '/'` 指向文章列表组件（或 `path: '/articles'`）

**3.2 在 `main.js` 里使用路由**

- `import router from './router'`，然后 `app.use(router)`

**3.3 建 `src/views/ArticleList.vue`（或 `ArticleListPage.vue`）**

- 用 `onMounted` 或 `setup` 里调用 axios 请求 `/api/articles/`
- 把返回的数据存到 `ref([])` 里，在模板里用 `v-for` 显示列表
- 可先用简单的 `<div>` 或 `<ul><li>` 显示，后面再加 Element Plus 的 `el-card`、`el-table` 等

**3.4 测试**

- 前端页面能显示文章列表即可（即使只有假数据）

---

## 四（续）、步骤 5 及后续：按模块扩展

每做一个新功能，都按「后端接口 → 前端页面 → 测试」的顺序：

1. **文章详情**：后端 `ArticleDetailView`（GET 单篇文章），前端详情页，路由 `/article/:id`
2. **分类/标签**：后端 `CategoryView`、`TagView`，前端分类页、标签页
3. **评论**：后端 `CommentView`（GET 列表、POST 新增），前端评论组件
4. **登录注册**：后端 `LoginView`、`RegisterView`（用 DRF 的 Token 认证），前端登录页、注册页，Pinia 存 token
5. **后台管理**：后端加 `admin/` 前缀的接口（如 `api/admin/articles/`），前端后台路由加 `meta: { requiresAuth: true }` 做守卫

参考 POEMON 的 `user/urls/index.py` 看 API 路径怎么设计，参考 `My-Blog-Vue3/src/api/` 看前端接口怎么封装。

---

## 五、和 POEMON 的关系

- **参考**：API 路径怎么设计（如 `api/article/`）、前端怎么分包（api、router、views）可以看 POEMON 的 `user/urls/index.py` 和 `My-Blog-Vue3/src`。
- **不复制**：不直接拷贝 POEMON 的代码，按上面步骤自己建、自己写，这样才是「仿照写一个属于你的 blog」。

---

## 六、需要具体代码时

- 做到某一步卡住，可以说「第 X 步的 xxx 怎么写」，再针对那一步给代码或片段。
- 也可以先要「Django settings 要改哪几处、每处填什么」的清单，照着在 PyCharm 里改。

---

*文档放在 d:\\Monkey-blog\\docs\\ 方便在写 lyhblog 时随时打开看。*

## 七、当前进度后的下一步示例：文章详情接口 + 页面

在完成「文章列表」和前后端联通之后，下一步可以先实现 **文章详情** 功能，对标 POEMON 的 `getArticle` 接口。

### 1. 后端：文章详情接口（blog）

1. 在 `blog/models.py` 中确认 `Article` 模型存在，至少包含：
   - `title`：标题（`CharField`）
   - `content`：正文（`TextField`）
   - `created_at`：创建时间（`DateTimeField(auto_now_add=True)`）

2. 在 `blog/views.py` 中新增 `ArticleDetailView(APIView)`：
   - 方法：`get(self, request, pk)`（或 `id`）
   - 从 MySQL 取单条记录：`Article.objects.get(pk=pk)`，注意处理找不到时返回 404。
   - 返回 JSON 结构示例：

     ```jsonc
     {
       "code": 200,
       "data": {
         "id": 1,
         "title": "xxx",
         "content": "正文...",
         "created_at": "2026-02-xx xx:xx:xx"
       },
       "message": "ok"
     }
     ```

3. 在 `blog/urls.py` 中加路由：

   ```python
   path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail')
   ```

   这样访问路径为：`/api/articles/1/`。

### 2. 前端：文章详情页面（lyhblog-frontend）

1. 新建 `src/router/index.js`（若尚未创建）：
   - 使用 `createRouter` + `createWebHistory`。
   - 添加详情路由：

     ```js
     {
       path: '/article/:id',
       name: 'article-detail',
       component: () => import('../views/ArticleDetail.vue')
     }
     ```

2. 在 `main.js` 中启用路由：

   ```js
   import router from './router'
   app.use(router)
   ```

3. 在 `src/views/` 下新建 `ArticleDetail.vue`：
   - 使用 `useRoute()` 读取 `route.params.id`。
   - 使用 axios 请求 `GET constant.baseURL + '/articles/' + id + '/'`。
   - 将返回的 `data` 渲染为标题、时间和正文内容。

4. （可选）如果已经有文章列表页面：
   - 在列表项中添加跳转：

     ```vue
     <router-link :to="`/article/${item.id}`">
       {{ item.title }}
     </router-link>
     ```

   - 点击后跳转到详情页，并根据 ID 加载数据。

> 这一节的目标：从首页/列表进入详情页，能根据文章 ID 从后端读取一篇文章并完整展示出来。

