# lyhblog 部署文档：Ubuntu 演练到阿里云上线

## 目标

先把项目部署到家里 Ubuntu 电脑，用 `Nginx + Gunicorn + MySQL` 跑通；确认稳定后，再迁移到阿里云。

## 为什么先 Ubuntu 再阿里云

这样做更稳，原因有 4 个：

1. 出问题更容易排查
2. 你对 Ubuntu 更熟，不必再加 Rocky Linux 变量
3. 跑通一次后，迁移到阿里云基本就是复制流程
4. 你现在缺的是部署经验，不是换发行版经验

现阶段不建议为了“更像生产环境”先切 Rocky Linux。  
如果没有强制要求，阿里云也继续选 Ubuntu 就够了。

## 什么时候适合正式上线

满足下面这些条件时最合适：

1. 家里 Ubuntu 已经部署成功
2. 前端 `npm run build` 通过
3. 后端 `python manage.py check` 通过
4. 登录、文章、详情、评论、后台管理都手测通过
5. Ubuntu 本机至少稳定跑半天到一天
6. 你能留出 2 到 3 小时观察迁移到云端后的运行情况

建议节奏：

- 第一步：先做家里 Ubuntu 演练部署
- 第二步：演练成功后 1 到 2 天内迁移到阿里云
- 第三步：正式公开上线放在迁移成功后的 1 到 2 天内

## 总体计划

### 计划 1：代码改造成可部署版本

1. 后端改为环境变量配置
2. 前端接口地址改为环境变量
3. 补齐部署依赖
4. 本地联调确认没问题

### 计划 2：Ubuntu 演练部署

1. 安装 Python / Node / MySQL / Nginx
2. 初始化数据库
3. 部署 Django
4. 部署 Vue
5. 配置 Gunicorn
6. 配置 Nginx
7. 本机和局域网测试

### 计划 3：迁移到阿里云

1. 购买 Ubuntu 云服务器
2. 安装同样环境
3. 上传同样代码
4. 导入数据库
5. 修改线上环境变量
6. 配置 Nginx 和 Gunicorn
7. 开放安全组
8. 联调上线

### 计划 4：正式上线前收尾

1. 做一次数据库备份
2. 配域名
3. 配 HTTPS
4. 观察日志
5. 再公开访问

---

## 第一部分：上线前需要改的代码

### 1. 后端依赖

文件：`lyhblog-backend/requirements.txt`

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
```

### 2. 后端环境变量模板

文件：`lyhblog-backend/.env.example`

```env
DJANGO_SECRET_KEY=replace-this-with-your-own-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=lyhblog
DB_USER=lyhblog
DB_PASSWORD=your-db-password
DB_HOST=127.0.0.1
DB_PORT=3306

CORS_ALLOWED_ORIGINS=http://127.0.0.1:5173,http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:5173,http://localhost:5173
```

### 3. 后端 settings.py

文件：`lyhblog-backend/config/settings.py`

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
        'USER': os.getenv('DB_USER', 'lyhblog'),
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

### 4. 前端开发环境变量

文件：`lyhblog-frontend/.env.development`

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

### 5. 前端生产环境变量

文件：`lyhblog-frontend/.env.production`

如果先部署到家里 Ubuntu 且只在局域网访问：

```env
VITE_API_BASE_URL=http://你的Ubuntu局域网IP/api
```

如果迁到阿里云：

```env
VITE_API_BASE_URL=http://你的云服务器IP/api
```

如果以后有域名和 HTTPS：

```env
VITE_API_BASE_URL=https://你的域名/api
```

### 6. 前端 request.js

文件：`lyhblog-frontend/src/utils/request.js`

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
    error => Promise.reject(error)
);

request.interceptors.response.use(
    response => response,
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

## 第二部分：Ubuntu 部署步骤

### 1. 安装环境

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx mysql-server nodejs npm git
```

检查版本：

```bash
python3 --version
node -v
npm -v
mysql --version
nginx -v
```

### 2. 建议目录

```bash
/var/www/lyhblog/
├─ backend/
├─ frontend/
└─ venv/
```

创建目录：

```bash
sudo mkdir -p /var/www/lyhblog
sudo chown -R $USER:$USER /var/www/lyhblog
```

### 3. 上传代码

建议把这两个目录上传到 Ubuntu：

- `lyhblog-backend`
- `lyhblog-frontend`

放到：

```bash
/var/www/lyhblog/backend
/var/www/lyhblog/frontend
```

### 4. 初始化 MySQL

进入 MySQL：

```bash
sudo mysql
```

执行：

```sql
CREATE DATABASE lyhblog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'lyhblog'@'localhost' IDENTIFIED BY '你的数据库密码';
GRANT ALL PRIVILEGES ON lyhblog.* TO 'lyhblog'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 5. 后端 .env

路径：`/var/www/lyhblog/backend/.env`

家里 Ubuntu 演练版可先这样写：

```env
DJANGO_SECRET_KEY=自己生成一个复杂密钥
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,你的Ubuntu局域网IP

DB_NAME=lyhblog
DB_USER=lyhblog
DB_PASSWORD=你的数据库密码
DB_HOST=127.0.0.1
DB_PORT=3306

CORS_ALLOWED_ORIGINS=http://你的Ubuntu局域网IP
CSRF_TRUSTED_ORIGINS=http://你的Ubuntu局域网IP
```

### 6. 部署 Django

```bash
cd /var/www/lyhblog
python3 -m venv venv
source venv/bin/activate

cd /var/www/lyhblog/backend
pip install --upgrade pip
pip install -r requirements.txt
```

执行迁移和检查：

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check
```

创建管理员：

```bash
python manage.py createsuperuser
```

先试跑：

```bash
python manage.py runserver 0.0.0.0:8000
```

浏览器访问：

```text
http://你的Ubuntu局域网IP:8000/admin/
```

确认后按 `Ctrl+C` 停掉。

### 7. 部署 Gunicorn

先手动测试：

```bash
cd /var/www/lyhblog/backend
source /var/www/lyhblog/venv/bin/activate
gunicorn config.wsgi:application --bind 127.0.0.1:8000
```

确认无报错后创建服务：

文件：`/etc/systemd/system/lyhblog.service`

```ini
[Unit]
Description=lyhblog gunicorn service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/lyhblog/backend
EnvironmentFile=/var/www/lyhblog/backend/.env
ExecStart=/var/www/lyhblog/venv/bin/gunicorn config.wsgi:application --workers 3 --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

启用：

```bash
sudo systemctl daemon-reload
sudo systemctl start lyhblog
sudo systemctl enable lyhblog
sudo systemctl status lyhblog
```

看日志：

```bash
journalctl -u lyhblog -f
```

### 8. 部署前端

前端先准备 `.env.production`：

```env
VITE_API_BASE_URL=http://你的Ubuntu局域网IP/api
```

打包：

```bash
cd /var/www/lyhblog/frontend
npm install
npm run build
```

打包输出目录：

```bash
/var/www/lyhblog/frontend/dist
```

### 9. 配置 Nginx

文件：`/etc/nginx/sites-available/lyhblog`

```nginx
server {
    listen 80;
    server_name 你的Ubuntu局域网IP 你的域名;

    root /var/www/lyhblog/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/lyhblog/backend/staticfiles/;
    }
}
```

启用：

```bash
sudo ln -s /etc/nginx/sites-available/lyhblog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl status nginx
```

如果默认站点冲突，可禁用：

```bash
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### 10. 防火墙

如果开启了 `ufw`：

```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw status
```

### 11. Ubuntu 自测清单

访问：

```text
http://你的Ubuntu局域网IP
```

检查：

1. 首页能打开
2. 文章列表能正常加载
3. 分类筛选能用
4. 标签筛选能用
5. 登录能成功
6. 后台能打开
7. 后台文章、分类、标签、评论管理能用
8. 文章详情能打开
9. 评论能发
10. 刷新页面不 404

### 12. 局域网其他设备访问

查看 Ubuntu IP：

```bash
ip addr
```

通常是类似 `192.168.x.x`。  
然后手机或同局域网电脑访问：

```text
http://192.168.x.x
```

如果打不开，优先检查：

1. Nginx 是否运行
2. 防火墙是否放行
3. `ALLOWED_HOSTS` 是否包含该 IP
4. `.env.production` 里的前端接口地址是否正确

---

## 第三部分：迁移到阿里云

迁到阿里云时，流程基本照搬：

1. 买 Ubuntu 云服务器
2. 安装 Python / Node / MySQL / Nginx
3. 上传项目
4. 配 `.env`
5. 初始化数据库
6. 启动 Gunicorn
7. 配 Nginx
8. 配安全组
9. 修改前端 `.env.production`
10. 联调上线

阿里云特别注意：

1. 安全组必须放行 `22/80/443`
2. 如果有域名，要先做域名解析
3. 真正公开上线前再配 HTTPS

阿里云上的 `.env.production` 示例：

```env
VITE_API_BASE_URL=http://你的云服务器IP/api
```

如果使用域名和 HTTPS：

```env
VITE_API_BASE_URL=https://你的域名/api
```

---

## 第四部分：正式上线前建议

不要在家里 Ubuntu 跑通后立刻公开。  
更稳的顺序是：

1. 家里 Ubuntu 演练成功
2. 迁移到阿里云
3. 自己完整手测一遍
4. 让 1 到 2 个熟人帮你访问
5. 看日志是否有 401 / 403 / 404 / 500
6. 观察半天到一天
7. 再正式公开

---

## 第五部分：你现在最适合的顺序

1. 先改 `settings.py`
2. 再改 `request.js`
3. 补 `.env.example`
4. 准备 `.env.production`
5. 在家里 Ubuntu 跑完整部署
6. 成功后迁到阿里云
7. 最后再配域名和 HTTPS

## 结论

你现在最正确的路线不是直接冲阿里云，也不是先折腾 Rocky Linux。  
最合理的是：

1. 先在家里 Ubuntu 部署
2. 用 Nginx 跑通整套流程
3. 再迁移到阿里云
4. 最后做正式上线

这个路线风险最小，也最适合你当前阶段。
