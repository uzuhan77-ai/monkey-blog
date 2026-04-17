# lyhblog 速通上线步骤

更新时间：2026-04-17
适用目录：`D:\Monkey-blog`
目标：先跑通，不追求一步到位的完美部署。

## 1. 当前最现实的上线路线

你的项目现在不适合一上来追求 Docker 全家桶、复杂监控和自动化流水线。

最现实的路线是：

1. 先在 Windows 本地跑通
2. 再在 WSL / Ubuntu 跑通
3. 前端 `npm build`
4. 后端 `Gunicorn`
5. Nginx 反向代理
6. 数据库连接正常
7. AI 中转配置正常

---

## 2. 上线前必须确认的 5 件事

### 1. 后端 `.env` 已准备好

至少有：

```env
ANTHROPIC_BASE_URL=你的网关地址
ANTHROPIC_AUTH_TOKEN=你的token
ANTHROPIC_MODEL=claude-sonnet-4-6
ANTHROPIC_TIMEOUT=60
```

### 2. 前端 `.env.production` 已准备好

```env
VITE_API_BASE_URL=http://你的服务器IP或域名/api
```

### 3. Django 时间和配置正常

```python
TIME_ZONE = 'Asia/Shanghai'
USE_TZ = True
```

### 4. AI 助手浏览器里至少成功跑通过一次

也就是：

- 输入主题
- 返回结果
- 一键回填
- 保存文章

### 5. 本地构建成功

前端：

```bash
npm.cmd run build
```

后端：

```bash
python manage.py check
```

---

## 3. WSL / Ubuntu 速通步骤

### 第一步：装基础环境

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx mysql-server nodejs npm
```

如果 Node 版本太低，就不要用系统默认源，改装高版本 Node。

---

### 第二步：准备项目目录

```bash
mkdir -p ~/projects
cd ~/projects
```

把你的：

- `lyhblog-backend`
- `lyhblog-frontend`

传到这里。

---

### 第三步：启动后端

```bash
cd ~/projects/lyhblog-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

先别急着 Gunicorn，先 `runserver` 跑通。

验证：

```bash
curl http://127.0.0.1:8000/api/test/
```

---

### 第四步：启动前端

```bash
cd ~/projects/lyhblog-frontend
npm install
npm run build
```

构建后会有：

```text
dist/
```

---

## 4. Gunicorn 速通

后端先这样起：

```bash
cd ~/projects/lyhblog-backend
source venv/bin/activate
gunicorn config.wsgi:application --bind 127.0.0.1:8000
```

这一步的目标只有一个：

**先确认 Gunicorn 能起。**

---

## 5. Nginx 最小配置

思路：

- `/` -> 前端静态页面
- `/api/` -> 反向代理到 Gunicorn

一个最小示例：

```nginx
server {
    listen 80;
    server_name _;

    root /home/你的用户名/projects/lyhblog-frontend/dist;
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
}
```

改完：

```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

## 6. 你现在真正的上线验收标准

不是“配了很多东西”，而是下面这些能不能用：

1. 首页能打开
2. 登录页能打开
3. 后台能登录
4. 文章列表能拉到数据
5. 新增文章能成功
6. AI 助手能成功返回一次

只要这 6 条成立，你就已经完成“速通上线”。

---

## 7. 最常见的 4 个坑

### 1. 前端 API 地址没换

如果前端还是请求：

```text
http://127.0.0.1:8000/api
```

那上线后一定错。

所以：

- 本地开发用 `.env.development`
- 部署时改 `.env.production`
- 改完重新 `npm run build`

### 2. `.env` 没带过去

后端 `.env` 不是 `.env.example`。

运行时读的是：

```text
lyhblog-backend/.env
```

### 3. Gunicorn 起了但 Nginx 没代理对

典型现象：

- 首页打开了
- 接口 404 或 502

### 4. AI 网关本身限流

你已经遇到过：

```text
rate_limit_error
```

这个不是代码没通，是网关上游限流。

---

## 8. 最短执行顺序

如果你只想最快跑通，就按这个顺序：

1. 本地构建前端
2. 本地 `manage.py check`
3. Ubuntu 里 `runserver` 跑通
4. Ubuntu 里前端 `build` 成功
5. Gunicorn 起成功
6. Nginx 指向前端 `dist`
7. `/api/` 转发到 Gunicorn
8. 浏览器测试后台 + AI 助手

---

## 9. 一句话建议

你现在上线不要追求“专业运维化”，而是：

**先把前端、后端、数据库、AI 网关这 4 条线在 Linux 环境里跑通。**
