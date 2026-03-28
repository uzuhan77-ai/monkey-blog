# POEMON 原版代码阅读指南

> 如何对照学习原版代码，找到你需要的参考

---

## 📂 目录结构速查

```
POEMON-BLOG-v2.0/
├── My-Blog-Vue3/          # 前端（你要参考的）
│   └── src/
│       ├── router/        # 路由配置
│       ├── utils/         # 工具函数（重点看这里）
│       ├── api/           # 接口封装
│       ├── views/         # 页面组件
│       └── store/         # Pinia 状态管理
│
└── My-Blog-Serve/         # 后端（你要参考的）
    ├── user/
    │   ├── urls/          # API 路由
    │   └── views/         # 视图函数
    └── appone/
        └── models/        # 数据模型
```

---

## 🎯 按功能查找代码

### 1. axios 封装（Day 1 需要）

**位置：** `My-Blog-Vue3/src/utils/request.js`

**看什么：**
- 第 1-10 行：axios 实例创建
- 第 12-20 行：请求拦截器（如何带 token）
- 第 22-40 行：响应拦截器（如何处理错误）

**对应你的文件：** `lyhblog-frontend/src/utils/request.js`（要创建）

---

### 2. 路由守卫（Day 2 需要）

**位置：** `My-Blog-Vue3/src/router/index.js`

**看什么：**
- 第 1-50 行：路由配置（前台路由）
- 第 60-100 行：后台路由（注意 `meta: { requiresAuth: true }`）
- 第 150-170 行：`router.beforeEach` 守卫逻辑

**对应你的文件：** `lyhblog-frontend/src/router/index.js`（要修改）

---

### 3. Pinia 状态管理（Day 2 需要）

**位置：** `My-Blog-Vue3/src/store/index.js`

**看什么：**
- state：存储 token、用户信息
- actions：登录、登出方法
- getters：判断是否登录

**对应你的文件：** `lyhblog-frontend/src/stores/user.js`（要创建）

---

### 4. 评论系统（Day 3-5 需要）

#### 后端接口

**位置：** `My-Blog-Serve/user/views/comment/`

**文件列表：**
- `list.py` - 评论列表
- `add.py` - 发表评论
- `delete.py` - 删除评论

**看什么：**
- 如何获取参数（`request.data.get()`）
- 如何查询数据库（`Comment.objects.filter()`）
- 如何返回 JSON（`Response()`）

**对应你的文件：** `lyhblog-backend/blog/views/comment.py`

#### 前端组件

**位置：** `My-Blog-Vue3/src/views/common/comment.vue`

**看什么：**
- 第 1-50 行：评论列表展示
- 第 60-100 行：发表评论表单
- 第 120-150 行：API 调用逻辑

**对应你的文件：** `lyhblog-frontend/src/components/CommentSection.vue`（要创建）

---


### 5. 后台管理布局（Day 8-9 需要）

**位置：** `My-Blog-Vue3/src/views/admin/`

**关键文件：**
- `index.vue` - 后台主布局（侧边栏 + 顶栏）

**看什么：**
- 侧边栏菜单结构
- 顶部用户信息展示
- 退出登录逻辑

**对应你的文件：** `lyhblog-frontend/src/views/admin/Layout.vue`（要创建）

---

### 6. 文章管理（Day 10-12 需要）

#### 后端接口

**位置：** `My-Blog-Serve/user/views/article/`

**文件列表：**
- `list.py` - 文章列表
- `get.py` - 文章详情
- `saveart.py` - 新增/编辑文章
- `delete.py` - 删除文章

**看什么：**
- 如何处理分页
- 如何处理多对多关系（标签）
- 权限控制（`permission_classes`）

#### 前端页面

**位置：** `My-Blog-Vue3/src/views/admin/`

**文件列表：**
- `postList.vue` - 文章列表
- `postEdit.vue` - 新增/编辑文章

**看什么：**
- 表格展示
- 表单验证
- 富文本编辑器使用

**对应你的文件：** 
- `lyhblog-frontend/src/views/admin/ArticleList.vue`
- `lyhblog-frontend/src/views/admin/ArticleEdit.vue`

---

## 🔍 快速查找技巧

### 技巧 1：从路由找页面

1. 打开 `My-Blog-Vue3/src/router/index.js`
2. 搜索你要找的功能（如 `comment`）
3. 看 `component` 字段，找到对应的 `.vue` 文件

### 技巧 2：从 API 找后端

1. 打开 `My-Blog-Vue3/src/api/` 下的文件
2. 看接口 URL（如 `/api/comment/list/`）
3. 去后端 `My-Blog-Serve/user/urls/index.py` 搜索这个 URL
4. 找到对应的 View

### 技巧 3：看数据模型

**位置：** `My-Blog-Serve/appone/models/`

**文件列表：**
- `article.py` - 文章模型
- `comment.py` - 评论模型
- `sort.py` - 分类模型
- `label.py` - 标签模型

**看什么：**
- 字段定义
- 关系定义（ForeignKey、ManyToManyField）

---


## 📖 学习路径建议

### 第 1 周学习重点

**Day 1：axios 封装**
```
阅读：My-Blog-Vue3/src/utils/request.js（全文）
重点：拦截器的使用
```

**Day 2：路由守卫**
```
阅读：My-Blog-Vue3/src/router/index.js（第150-170行）
重点：beforeEach 的判断逻辑
```

**Day 3-5：评论系统**
```
后端：My-Blog-Serve/user/views/comment/（所有文件）
前端：My-Blog-Vue3/src/views/common/comment.vue
重点：前后端如何交互
```

### 第 2 周学习重点

**Day 8-9：后台布局**
```
阅读：My-Blog-Vue3/src/views/admin/index.vue
重点：el-container 布局
```

**Day 10-12：文章管理**
```
后端：My-Blog-Serve/user/views/article/saveart.py
前端：My-Blog-Vue3/src/views/admin/postEdit.vue
重点：表单提交和数据回显
```

---

## ⚠️ 注意事项

### 1. 不要完全照抄

原版代码有些地方比较复杂，你可以：
- 理解思路
- 简化实现
- 用自己的方式写

### 2. 版本差异

原版使用：
- Django 4.1.5（你用的是 6.x，API 基本兼容）
- Vue 3 + Vite 5（你的版本一致）

### 3. 功能取舍

原版有很多功能（音乐、相册、树洞等），你不需要全做：
- ✅ 必做：文章、评论、后台管理
- ⚠️ 可选：富文本、图片上传
- ❌ 暂不做：音乐、相册、访客统计

---

## 🛠️ 实用命令

### 快速查找文件
```bash
# 查找包含 "comment" 的文件
find D:\Monkey-blog\POEMON-BLOG-v2.0 -name "*comment*"

# 搜索代码中的关键字
grep -r "CommentListView" D:\Monkey-blog\POEMON-BLOG-v2.0
```

### 对比文件
用 VS Code 打开两个文件，右键选择"比较所选项"

---

## 💡 遇到问题怎么办

1. **先看原版代码**：找到对应功能的实现
2. **理解逻辑**：不要直接复制，理解为什么这样写
3. **简化实现**：用最简单的方式实现同样的功能
4. **测试验证**：确保功能正常工作

---

**现在你可以开始对照学习了！建议边看边写，不要只看不动手。**

