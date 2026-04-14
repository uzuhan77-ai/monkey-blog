# lyhblog 继续开发：环境变量改造与上线准备

## 目标

把当前项目从“只能本地开发跑”改成“可以准备部署到 Ubuntu / 阿里云”的状态。

这一步不直接上线，但它是上线前必须做的收尾工作。

完成后你会得到：

1. 后端数据库配置不再写死在代码里
2. `SECRET_KEY` 不再写死在 `settings.py`
3. 前端接口地址不再写死 `127.0.0.1`
4. 本地开发和生产部署可以用不同环境变量
5. 为后面 Ubuntu 演练部署和阿里云迁移打基础

---

## 为什么现在做这个

你现在已经做到：

1. 前台文章列表
2. 前台详情
3. 分类筛选
4. 标签筛选
5. 关键词搜索
6. 后台文章管理
7. 后台分类管理
8. 后台标签管理
9. 后台评论分页

这个时候继续加小功能，收益已经开始下降。  
现在更应该进入“上线准备阶段”。

---

## 计划

### 计划 1：后端配置改成环境变量

把这些从代码里移出去：

1. `SECRET_KEY`
2. `DEBUG`
3. `ALLOWED_HOSTS`
4. 数据库名
5. 数据库用户名
6. 数据库密码
7. 数据库地址
8. 数据库端口

### 计划 2：前端接口地址改成环境变量

把现在写死的：

```javascript
http://127.0.0.1:8000/api
```

改成：

```javascript
import.meta.env.VITE_API_BASE_URL
```

### 计划 3：补齐依赖

后端需要加：

1. `mysqlclient`
2. `python-dotenv`
3. `gunicorn`

### 计划 4：区分开发环境和生产环境

前端新增：

1. `.env.development`
2. `.env.production`

后端新增：

1. `.env.example`
2. 实际部署时再复制成 `.env`

### 计划 5：本地自测

改完后重新做：

1. 后端 `check`
2. 前端 `build`
3. 登录测试
4. 文章列表/详情测试
5. 后台测试

---

## 要改的文件

1. `lyhblog-backend/requirements.txt`
2. `lyhblog-backend/config/settings.py`
3. `lyhblog-backend/.env.example`
4. `lyhblog-frontend/src/utils/request.js`
5. `lyhblog-frontend/.env.development`
6. `lyhblog-frontend/.env.production`

---

## 一、后端依赖

文件：`lyhblog-backend/requirements.txt`

把它改成下面这版：

```txt
asgiref==3.11.1
Django==6.0.2
django-cors-headers==4.9.0
djangorestframework==3.16.1
mysqlclient==2.2.7
python-dotenv==1.1.0
gunicorn==23.0.0
sqlparse==0.5.5
tzdata==2025.3
```

---

## 二、后端环境变量模板

文件：`lyhblog-backend/.env.example`

新建这个文件，内容如下：

```env
DJANGO_SECRET_KEY=replace-this-with-your-own-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=lyhblog
DB_USER=root
DB_PASSWORD=123
DB_HOST=127.0.0.1
DB_PORT=3306

CORS_ALLOWED_ORIGINS=http://127.0.0.1:5173,http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:5173,http://localhost:5173
```

说明：

1. 这是模板，不是最终真实配置
2. 实际使用时，把它复制成 `.env`
3. `.env` 不建议提交到 Git

---

## 三、后端 settings.py 完整参考代码

文件：`lyhblog-backend/config/settings.py`

把当前内容替换成下面这版：

```python
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


def env_list(name, default=''):
    value = os.getenv(name, default)
    return [item.strip() for item in value.split(',') if item.strip()]


SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-secret-key')
DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() == 'true'
ALLOWED_HOSTS = env_list('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'blog',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'lyhblog'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CSRF_TRUSTED_ORIGINS = env_list(
        'CSRF_TRUSTED_ORIGINS',
        'http://127.0.0.1:5173,http://localhost:5173'
    )
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = env_list('CORS_ALLOWED_ORIGINS')
    CSRF_TRUSTED_ORIGINS = env_list('CSRF_TRUSTED_ORIGINS')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

---

## 四、前端开发环境变量

文件：`lyhblog-frontend/.env.development`

新建这个文件：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

这是你本地开发用的地址。

---

## 五、前端生产环境变量

文件：`lyhblog-frontend/.env.production`

如果先部署到家里 Ubuntu：

```env
VITE_API_BASE_URL=http://你的Ubuntu局域网IP/api
```

如果后面部署到阿里云：

```env
VITE_API_BASE_URL=http://你的云服务器IP/api
```

如果以后有域名和 HTTPS：

```env
VITE_API_BASE_URL=https://你的域名/api
```

---

## 六、前端 request.js 完整参考代码

文件：`lyhblog-frontend/src/utils/request.js`

把现在写死的 `baseURL` 改掉，整个文件改成：

```javascript
import axios from "axios";
import { ElMessage } from "element-plus";
import router from "../router";

const request = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 10000
});

request.interceptors.request.use(
    config => {
        const token = localStorage.getItem("token");
        if (token) {
            config.headers.Authorization = `Token ${token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

request.interceptors.response.use(
    response => {
        return response;
    },
    error => {
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    ElMessage.error("请先登录");
                    localStorage.removeItem("token");
                    localStorage.removeItem("user_info");
                    localStorage.removeItem("is_admin");
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

## 七、改完之后你要做什么

### 1. 后端目录下复制 `.env`

在 `lyhblog-backend` 目录里：

1. 复制 `.env.example`
2. 改名为 `.env`
3. 把里面的数据库信息改成你本机真实值

例如：

```env
DJANGO_SECRET_KEY=你自己的复杂密钥
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=lyhblog
DB_USER=root
DB_PASSWORD=123
DB_HOST=127.0.0.1
DB_PORT=3306

CORS_ALLOWED_ORIGINS=http://127.0.0.1:5173,http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:5173,http://localhost:5173
```

### 2. 前端重新启动

改完前端环境变量后，重新启动开发服务器：

```powershell
cd D:\Monkey-blog\lyhblog-frontend
npm run dev
```

注意：Vite 改 `.env` 后通常要重启才会生效。

---

## 八、自测步骤

### 后端检查

```powershell
cd D:\Monkey-blog\lyhblog-backend
venv\Scripts\python.exe manage.py check
```

### 前端构建

```powershell
cd D:\Monkey-blog\lyhblog-frontend
npm.cmd run build
```

### 页面功能检查

1. 首页文章列表能打开
2. 分类筛选正常
3. 标签筛选正常
4. 搜索正常
5. 登录正常
6. 后台能进
7. 评论管理能进

---

## 九、这一步做完以后，你就能做什么

做完这一步后，你就可以进入：

1. Ubuntu 本机演练部署
2. Nginx + Gunicorn + MySQL 联调
3. 阿里云迁移准备

也就是说，这一步是“上线准备的起点”。

---

## 十、建议的后续顺序

环境变量改造做完后，建议继续按这个顺序：

1. 本地重新联调
2. Ubuntu 演练部署
3. 阿里云部署
4. 域名和 HTTPS
5. README 补齐

---

## 结论

你现在已经不是缺功能，而是缺“从开发项目变成可部署项目”的这一步。

所以这份文档的目标不是让你多写页面，而是让你：

1. 先把配置理干净
2. 再把项目部署起来
3. 最后再正式上线

这才是你当前阶段最值的一步。
