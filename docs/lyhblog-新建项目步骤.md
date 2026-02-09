# lyhblog 新建项目步骤（仿照 POEMON 写自己的博客）

> 只给操作顺序和指令，不直接生成代码；按步做，用 PyCharm 写后端、Cursor 写前端。

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

- 在 `INSTALLED_APPS` 里加上：`rest_framework`、`corsheaders`、你的 `blog`。
- 在 `MIDDLEWARE` 里加上 `corsheaders` 的中间件（查 django-cors-headers 文档，一般是 `CorsMiddleware` 放最上）。
- 先配好 `DATABASES` 用 SQLite（`ENGINE: sqlite3`），等接口和前端联调没问题再改成 MySQL。
- 改 `SECRET_KEY`（可先用开发用的一串随机字符），`ALLOWED_HOSTS` 里加 `'*'` 或 `'localhost'` 方便本地调试。

### 6. 总路由

- 在 `config/urls.py` 里用 `include` 把以 `api/` 开头的路径指到你 blog 的 urls（例如 `path('api/', include('blog.urls'))`）。
- 在 blog 里新建 `urls.py`，先写一条测试路由（比如一个返回 `{"ok": true}` 的视图），用 `python manage.py runserver` 跑起来，浏览器访问确认能返回 JSON。

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
| 4 | **第一个真实功能**：在后端 blog 里做「文章列表」接口（一条 GET，可先返回假数据或从 SQLite 读一张简单表），前端做一个「文章列表」页，调这个接口并显示。 |
| 5 | 再往后：文章详情、分类、评论、登录注册等，每块都先在后端加接口，再在前端加页面和请求。 |

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
