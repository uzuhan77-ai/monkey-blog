# lyhblog 阿里云上线与 ECS 登录排障

更新时间：2026-04-20

适用项目目录：

- `D:\Monkey-blog\lyhblog-backend`
- `D:\Monkey-blog\lyhblog-frontend`

目标：

1. 先解决阿里云 ECS 用户名、密码、SSH 登录问题
2. 再把 lyhblog 用 `Nginx + Gunicorn + MySQL` 跑起来
3. 最后绑定域名并开 HTTPS

---

## 一、你刚才那个 ECS 报错是什么意思

你截图里的核心报错是：

```text
chpasswd: line 1: user 'lyh' does not exist
Password reset failed.
```

这说明：

- 阿里云云助手正在尝试给用户 `lyh` 改密码
- 但你的服务器里根本没有 `lyh` 这个 Linux 用户
- 所以不是云助手坏了，而是用户名填错了

另外这句：

```text
Key pair ... has been removed
```

不是主要问题。
真正导致失败的是：

```text
user 'lyh' does not exist
```

---

## 二、先用云助手确认服务器里到底有哪些用户

在阿里云 ECS 云助手里执行：

```bash
awk -F: '$3 >= 0 && $7 !~ /(nologin|false)/ {print $1, $7}' /etc/passwd
```

你通常会看到这些之一：

- `root`
- `ubuntu`
- `ecs-user`

记住真实存在的用户名。

---

## 三、如果你只是想把密码改成功

假设查出来系统用户是 `ubuntu`，那就执行：

```bash
echo 'ubuntu:你的新密码' | chpasswd
```

如果查出来是 `root`：

```bash
echo 'root:你的新密码' | chpasswd
```

如果查出来是 `ecs-user`：

```bash
echo 'ecs-user:你的新密码' | chpasswd
```

---

## 四、如果你就是想用 lyh 这个用户名登录

那就先创建这个用户，再给它设密码：

```bash
id lyh >/dev/null 2>&1 || useradd -m -s /bin/bash lyh
echo 'lyh:你的新密码' | chpasswd
usermod -aG sudo lyh 2>/dev/null || true
usermod -aG wheel lyh 2>/dev/null || true
```

说明：

- Ubuntu 常见管理员组是 `sudo`
- 其他系统有时用 `wheel`
- 上面两个都写上，是为了兼容

---

## 五、如果密码改好了但 SSH 还是不让密码登录

继续在云助手里执行：

```bash
sed -ri 's/^#?PasswordAuthentication\s+.*/PasswordAuthentication yes/' /etc/ssh/sshd_config
systemctl restart sshd || systemctl restart ssh
```

如果你还想允许 `root` 直接密码登录，再检查：

```bash
grep -E '^#?PermitRootLogin' /etc/ssh/sshd_config
```

必要时改成：

```bash
sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
systemctl restart sshd || systemctl restart ssh
```

说明：

- 正式环境不建议长期开放 `root + 密码`
- 如果只是先救急登录，可以暂时开
- 登录稳定后，建议改回密钥登录

---

## 六、阿里云控制台先准备什么

### 1. 安全组

至少放行：

- `22`
- `80`
- `443`

不要把 `8000` 暴露到公网。

### 2. 域名解析

在域名解析里加：

- `@` -> 服务器公网 IP
- `www` -> 服务器公网 IP

### 3. 服务器系统

建议用：

- Ubuntu 22.04

这样和你现在整理的部署方式最接近。

---

## 七、上线前你本地代码要先确认的地方

你当前项目已经接近能上线，但不是完全生产态。

重点看这几个文件：

- `lyhblog-backend/config/settings.py`
- `lyhblog-backend/.env.example`
- `lyhblog-frontend/.env.production`
- `lyhblog-frontend/src/utils/request.js`

### 1. 后端 settings.py 当前的风险

你现在文件里还有这些情况：

- `DEBUG = True`
- `ALLOWED_HOSTS = ['*']`
- `CORS_ALLOW_ALL_ORIGINS = True`

这几个值在服务器正式环境里不应该继续写死。

建议改成走环境变量，至少做到：

```python
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key-change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = [item.strip() for item in os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if item.strip()]
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
```

生产环境下：

- `DEBUG=False`
- `ALLOWED_HOSTS=你的域名,www.你的域名,服务器IP`
- `STATIC_ROOT` 必须有，不然后面 `collectstatic` 没地方放

### 2. 前端生产环境变量

你现在的 `lyhblog-frontend/.env.production` 保持这样就对：

```env
VITE_API_BASE_URL=/api
```

不要改成：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

生产环境里前端应该始终通过 Nginx 反代走 `/api`。

### 3. 后端 .env.example 里不要放真实 token

你当前模板文件里有真实 `ANTHROPIC_AUTH_TOKEN`。
这个必须删掉并换成占位符。

建议模板改成：

```env
DJANGO_SECRET_KEY=replace-me
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=example.com,www.example.com,你的服务器IP

CORS_ALLOWED_ORIGINS=https://example.com,https://www.example.com
CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com

DB_NAME=lyhblog
DB_USER=lyhblog
DB_PASSWORD=replace-db-password
DB_HOST=127.0.0.1
DB_PORT=3306

ANTHROPIC_BASE_URL=https://your-gateway
ANTHROPIC_AUTH_TOKEN=replace-token
ANTHROPIC_MODEL=claude-sonnet-4-6
ANTHROPIC_TIMEOUT=60
```

如果那把 key 已经用过，建议直接作废重发。

---

## 八、服务器环境安装

登录服务器后执行：

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip pkg-config default-libmysqlclient-dev build-essential nginx mysql-server curl git
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
```

检查版本：

```bash
python3 --version
node -v
npm -v
mysql --version
nginx -v
```

---

## 九、上传项目到服务器

建议目录：

```bash
sudo mkdir -p /srv/lyhblog
sudo chown -R $USER:$USER /srv/lyhblog
```

最终建议结构：

```text
/srv/lyhblog/backend
/srv/lyhblog/frontend
```

你把这两个目录传上去：

- `lyhblog-backend` -> `/srv/lyhblog/backend`
- `lyhblog-frontend` -> `/srv/lyhblog/frontend`

---

## 十、配置 MySQL

先进入 MySQL：

```bash
sudo mysql
```

执行：

```sql
CREATE DATABASE lyhblog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'lyhblog'@'127.0.0.1' IDENTIFIED BY '你的强密码';
GRANT ALL PRIVILEGES ON lyhblog.* TO 'lyhblog'@'127.0.0.1';
FLUSH PRIVILEGES;
EXIT;
```

---

## 十一、配置后端

进入后端目录：

```bash
cd /srv/lyhblog/backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

新建服务器真实使用的 `.env`：

```env
DJANGO_SECRET_KEY=你自己的长随机字符串
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=你的域名,www.你的域名,你的服务器公网IP

CORS_ALLOWED_ORIGINS=https://你的域名,https://www.你的域名
CSRF_TRUSTED_ORIGINS=https://你的域名,https://www.你的域名

DB_NAME=lyhblog
DB_USER=lyhblog
DB_PASSWORD=你的数据库密码
DB_HOST=127.0.0.1
DB_PORT=3306

ANTHROPIC_BASE_URL=你的中转地址
ANTHROPIC_AUTH_TOKEN=你的新token
ANTHROPIC_MODEL=claude-sonnet-4-6
ANTHROPIC_TIMEOUT=60
```

然后执行：

```bash
python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

先手动试跑：

```bash
gunicorn config.wsgi:application --bind 127.0.0.1:8000
```

再另开终端验证：

```bash
curl http://127.0.0.1:8000/api/test/
```

能通再继续。

---

## 十二、配置 systemd

新建服务文件：

```bash
sudo nano /etc/systemd/system/lyhblog.service
```

内容：

```ini
[Unit]
Description=lyhblog gunicorn service
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/srv/lyhblog/backend
Environment="PATH=/srv/lyhblog/backend/.venv/bin"
ExecStart=/srv/lyhblog/backend/.venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3 --timeout 120
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

注意：

- 如果你的服务器用户名不是 `ubuntu`，改成你自己的

启动：

```bash
sudo systemctl daemon-reload
sudo systemctl enable lyhblog
sudo systemctl start lyhblog
sudo systemctl status lyhblog --no-pager
```

---

## 十三、配置前端

进入前端目录：

```bash
cd /srv/lyhblog/frontend
npm install
npm run build
```

构建后应得到：

```text
/srv/lyhblog/frontend/dist
```

---

## 十四、配置 Nginx

新建站点配置：

```bash
sudo nano /etc/nginx/sites-available/lyhblog
```

内容：

```nginx
server {
    listen 80;
    server_name 你的域名 www.你的域名;

    root /srv/lyhblog/frontend/dist;
    index index.html;

    client_max_body_size 20m;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120;
    }

    location /admin/ {
        proxy_pass http://127.0.0.1:8000/admin/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /srv/lyhblog/backend/staticfiles/;
    }
}
```

启用：

```bash
sudo ln -s /etc/nginx/sites-available/lyhblog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 十五、上 HTTPS

等 HTTP 全部跑通后再做：

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d 你的域名 -d www.你的域名
sudo certbot renew --dry-run
```

---

## 十六、上线验收顺序

按下面顺序验：

1. `http://你的域名` 首页能打开
2. `http://你的域名/api/test/` 能返回
3. 后台登录页能打开
4. 后台能登录
5. 文章列表能拉到数据
6. 新增文章成功
7. AI 写作助手成功返回一次
8. `https://你的域名` 正常
9. 刷新前台和后台路由不 404

---

## 十七、你这个项目最容易踩的坑

### 1. 后端还是开发配置

如果不改：

- `DEBUG=True`
- `ALLOWED_HOSTS=['*']`
- `CORS_ALLOW_ALL_ORIGINS=True`

那它只是能跑，不是稳妥上线。

### 2. .env.example 里留了真实 token

这不是模板，是泄漏点。
要删，并且那把 key 最好作废重发。

### 3. 前端 API 地址写死

生产环境一定走：

```env
VITE_API_BASE_URL=/api
```

不要写服务器 IP 直连后端。

### 4. 忘了 collectstatic

如果没执行：

```bash
python manage.py collectstatic --noinput
```

那 Django admin 样式很容易丢。

---

## 十八、最短上线顺序

1. 先用云助手查出真实 Linux 用户名
2. 改好密码或创建 `lyh` 用户
3. 打通 SSH 登录
4. 本地先把 `settings.py` 和 `.env.example` 改好
5. 上传代码到阿里云
6. 配 MySQL
7. 配后端 `.env`
8. `migrate + collectstatic + createsuperuser`
9. Gunicorn 手动试跑
10. 配 systemd
11. 前端 build
12. 配 Nginx
13. 验证域名访问
14. 最后再上 HTTPS

---

## 十九、如果你下一步卡住了，优先把这三样发出来

1. 云助手里执行这条的输出：

```bash
awk -F: '$3 >= 0 && $7 !~ /(nologin|false)/ {print $1, $7}' /etc/passwd
```

2. 这条的输出：

```bash
sudo systemctl status lyhblog --no-pager
```

3. 这条的输出：

```bash
sudo nginx -t
```

有了这三样，基本就能快速判断你卡在哪一层。
