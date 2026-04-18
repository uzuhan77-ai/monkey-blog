# lyhblog WSL 速通上线模拟

这份文档只讲最短可执行路径。
目标是两步：

1. 现在在公司电脑的 WSL Ubuntu 里跑通一遍
2. 晚上买云服务器后，基本照搬

不先折腾 Docker，不先重构全部配置，不先做花活。

---

## 一、你当前项目状态

按你现在代码，已经具备这几个条件：

- 后端依赖里有 `gunicorn`、`mysqlclient`、`python-dotenv`、`httpx`
- 后端支持 `.env` 读取 Claude 中转配置
- 前端可以 `npm run build`
- AI 接口已经通了，主要风险是中转限流，不是项目结构问题

但也要认清当前现实：

- `settings.py` 里数据库、`DEBUG`、`SECRET_KEY` 还是开发态写死
- `ALLOWED_HOSTS=['*']`
- `CORS_ALLOW_ALL_ORIGINS=True`

所以这次上线模拟的目标是：
**先跑通部署链路**，不是一步做到生产级安全加固。

---

## 二、WSL 里你要达到的最终效果

浏览器访问：

- `http://你的WSL地址/` -> 前端页面
- `http://你的WSL地址/api/...` -> Django 接口

服务结构：

- Nginx：对外入口
- 前端：`vite build` 后的静态文件
- 后端：Gunicorn 跑 Django
- 数据库：MySQL

---

## 三、WSL 里先装什么

进入 Ubuntu 后先执行：

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip pkg-config default-libmysqlclient-dev build-essential mysql-server nginx curl git
```

### 安装 Node 22

你前端是 `vite 7.3.1`，别用 Ubuntu 默认旧版 Node。
直接用 NodeSource：

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
node -v
npm -v
```

看到 Node 22 就行。

---

## 四、项目路径先别放错

如果你 Windows 项目在 `D:\Monkey-blog`，WSL 里一般能看到：

```bash
/mnt/d/Monkey-blog
```

### 当前默认方案：直接在 D 盘这份代码上跑

你现在是在公司电脑里做 WSL 演练，最短路径就是直接用：

```bash
cd /mnt/d/Monkey-blog
```

不要先执行：

```bash
cp -r /mnt/d/Monkey-blog ~/Monkey-blog
```

原因很简单：

- `~` 在 WSL 里对应的是 Linux 用户目录
- WSL 的 Linux 用户目录默认存到 WSL 虚拟磁盘
- 这个虚拟磁盘通常落在 Windows 的 `C:` 盘
- 你项目一复制，实际是在继续吃 Windows `C:` 空间

所以你当前这台公司电脑，默认就按这个路径往下走：

```bash
/mnt/d/Monkey-blog
```

### 晚上换到你自己的电脑怎么办

如果晚上你换到自己的电脑继续做：

- 如果你自己电脑的 `C:` 盘空间充足，可以复制到 `~/Monkey-blog`
- 如果你想走最短可执行路径，还是直接用 `/mnt/d/Monkey-blog`

这份文档下面统一按：

```bash
/mnt/d/Monkey-blog
```

来写，避免两套路径来回切。

---

## 五、后端速通部署

### 1. 进后端目录

```bash
cd /mnt/d/Monkey-blog/lyhblog-backend
```

### 2. 建虚拟环境并安装依赖

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. 配 MySQL

先登录 MySQL：

```bash
sudo mysql
```

执行：

```sql
CREATE DATABASE lyhblog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'lyhblog'@'localhost' IDENTIFIED BY '123';
GRANT ALL PRIVILEGES ON lyhblog.* TO 'lyhblog'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. 改后端数据库配置

你当前 `settings.py` 还是写死：

- 库名：`lyhblog`
- 用户：`root`
- 密码：`123`

WSL 里为了最短跑通，二选一：

#### 方案 A：直接把 `settings.py` 改成你刚创建的库用户

改成：

```python
'DATABASES': {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lyhblog',
        'USER': 'lyhblog',
        'PASSWORD': '123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

#### 方案 B：你偷懒，就在 MySQL 里把 root 密码也设成你代码现在写的

不推荐，但能跑。

**我建议你用方案 A。**

### 5. 准备 `.env`

如果你 AI 要继续可用，确保 `lyhblog-backend/.env` 至少有：

```env
ANTHROPIC_BASE_URL=https://api.beehears.com
ANTHROPIC_AUTH_TOKEN=你的新token
ANTHROPIC_MODEL=claude-sonnet-4-6
ANTHROPIC_TIMEOUT=60
```

### 6. 跑迁移和检查

```bash
python manage.py migrate
python manage.py check
```

### 7. 创建管理员

```bash
python manage.py createsuperuser
```

### 8. 先本地试跑 Gunicorn

```bash
gunicorn config.wsgi:application --bind 127.0.0.1:8000
```

这时不要关，开新终端继续做前端。

---

## 六、前端速通部署

### 1. 进前端目录

```bash
cd /mnt/d/Monkey-blog/lyhblog-frontend
```

### 2. 安装依赖

```bash
npm install
```

### 3. 配生产环境变量

如果你前端已经支持 `.env.production`，就写：

```env
VITE_API_BASE_URL=/api
```

如果还没有这个文件，就新建：

```bash
cat > .env.production <<EOF
VITE_API_BASE_URL=/api
EOF
```

### 4. 构建

```bash
npm run build
```

构建成功后，产物在：

```bash
/mnt/d/Monkey-blog/lyhblog-frontend/dist
```

---

## 七、Nginx 反代速通

### 1. 新建站点配置

```bash
sudo nano /etc/nginx/sites-available/lyhblog
```

填入：

```nginx
server {
    listen 80;
    server_name _;

    root /mnt/d/Monkey-blog/lyhblog-frontend/dist;
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

    location /admin/ {
        proxy_pass http://127.0.0.1:8000/admin/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        proxy_pass http://127.0.0.1:8000/static/;
    }
}
```

把里面的：

```text
/mnt/d/Monkey-blog/lyhblog-frontend/dist
```

如果你晚上在自己电脑上选择复制到 `~/Monkey-blog`，这里再改成对应的 `/home/你的Linux用户名/...` 路径。

### 2. 启用配置

```bash
sudo ln -s /etc/nginx/sites-available/lyhblog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 八、正式把 Gunicorn 挂成 systemd 服务

### 1. 新建服务文件

```bash
sudo nano /etc/systemd/system/lyhblog.service
```

填入：

```ini
[Unit]
Description=lyhblog gunicorn service
After=network.target

[Service]
User=你的Linux用户名
Group=www-data
WorkingDirectory=/mnt/d/Monkey-blog/lyhblog-backend
Environment="PATH=/mnt/d/Monkey-blog/lyhblog-backend/.venv/bin"
ExecStart=/mnt/d/Monkey-blog/lyhblog-backend/.venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### 2. 启动

```bash
sudo systemctl daemon-reload
sudo systemctl enable lyhblog
sudo systemctl start lyhblog
sudo systemctl status lyhblog
```

如果状态是 `active (running)`，说明后端服务挂好了。

---

## 九、WSL 里怎么验收

按这个顺序验：

1. 首页能打开
2. 登录页能打开
3. 后台能登录
4. 新增文章能保存
5. 前台能看到文章
6. AI 写作助手能请求成功

### 如果 AI 写作助手失败

优先看两类：

#### 1. 前端超时

你当前 AI 接口已经单独配了长超时，这个大概率没问题。

#### 2. 中转限流

你之前已经遇到过：

```json
{"error":{"message":"Upstream rate limit exceeded, please retry later"}}
```

这个不是部署挂了，是中转上游限流。

---

## 十、晚上换到你自己的电脑，或买云服务器后怎么照搬

如果你晚上先换到自己的电脑继续做：

- 最短路径还是继续用 `/mnt/d/Monkey-blog`
- 只有在你自己电脑 `C:` 盘空间充足、并且你想把项目完整放进 Linux 文件系统时，才改成 `~/Monkey-blog`

如果你晚上直接买 Ubuntu 云服务器，流程也基本一样，只是把 `/mnt/d/Monkey-blog` 换成服务器路径。

你只需要重做这几件事：

1. 安装系统依赖
2. 上传项目代码
3. 建 Python 虚拟环境
4. 装依赖
5. 建 MySQL 数据库
6. 配 `.env`
7. `python manage.py migrate`
8. `npm run build`
9. 配 Gunicorn
10. 配 Nginx
11. 开放 80 端口

### 云服务器额外要做的

#### 1. 安全组开放

至少开放：

- `80`
- `22`

如果你临时调试，也可以短时开放：

- `8000`

但正式不用一直开 `8000`。

#### 2. 改 `ALLOWED_HOSTS`

现在你代码是：

```python
ALLOWED_HOSTS = ['*']
```

为了今晚先上去，这个其实能跑。
后面稳定后再收口到你的域名和服务器 IP。

#### 3. 域名没买也能先用公网 IP 访问

先别被域名卡住。
你今晚就算只有：

```text
http://你的云服务器公网IP
```

也已经算上线成功。

---

## 十一、今晚最短成功标准

你今天别追求一步到位，成功标准就这 4 条：

1. WSL 里前后端都能通过 Nginx 正常访问
2. Gunicorn 不是手工跑，而是 systemd 挂起来
3. 云服务器买完后，能按同样步骤跑起来
4. 你能用公网 IP 打开首页和后台

做到这一步，你这个项目就已经从“本地练手”进入“可部署项目”阶段了。

---

## 十二、我对你现在的直接建议

如果你现在马上开干，顺序不要乱：

1. 先在 WSL 装依赖
2. 先把 MySQL 和 Gunicorn 跑起来
3. 再 build 前端
4. 最后配 Nginx

不要一上来先研究云服务器面板，也不要先研究 HTTPS。
先把 `HTTP + 公网 IP + Nginx + Gunicorn + MySQL` 跑通。

这才是今晚最值的路线。
