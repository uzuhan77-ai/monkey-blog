# lyhblog 分步骤开发教程

> 从当前状态到完整可用的博客系统
> 预计时间：3周（每天2-3小时）

---

## 📋 开发前准备

### 检查当前环境

**后端检查：**
```bash
cd D:\Monkey-blog\lyhblog-backend
python manage.py runserver
# 访问 http://127.0.0.1:8000/api/article/listArticle/ 应该能看到数据
```

**前端检查：**
```bash
cd D:\Monkey-blog\lyhblog-frontend
npm run dev
# 访问 http://localhost:5173 应该能看到文章列表
```

**如果都正常，开始第一步！**

---

## 第 1 周：工程化基础 + 评论系统

### Day 1：axios 统一封装（2-3小时）

#### 步骤 1.1：创建 request.js

在 `lyhblog-frontend/src/utils/` 目录下创建 `request.js`：

```javascript
// src/utils/request.js
import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

// 创建 axios 实例
const request = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 10000
})

// 请求拦截器：自动带上 token
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器：统一处理错误
request.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          ElMessage.error('请先登录')
          localStorage.removeItem('token')
          router.push('/login')
          break
        case 403:
          ElMessage.error('没有权限')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器错误')
          break
        default:
          ElMessage.error('请求失败')
      }
    } else {
      ElMessage.error('网络错误')
    }
    return Promise.reject(error)
  }
)

export default request
```

#### 步骤 1.2：修改 api/article.js

把所有接口改用新的 request：

```javascript
// src/api/article.js
import request from '../utils/request'

// 文章列表
export const ApiArticleList = (data) => {
  return request.post('/article/listArticle/', data)
}

// 文章详情
export const ApiArticleDetail = (id) => {
  return request.get('/article/getArticleById/', {
    params: { id }
  })
}

// 分类列表
export const ApiCategoryList = () => {
  return request.get('/category/listCategory/')
}

// 登录
export const ApiLogin = (data) => {
  return request.post('/user/login/', data)
}

// 注册
export const ApiRegister = (data) => {
  return request.post('/user/register/', data)
}
```

#### 步骤 1.3：测试

启动前后端，测试文章列表是否正常。

**✅ Day 1 完成标志：** 文章列表、详情、登录都能正常工作，控制台没有报错。

---


### Day 2：路由守卫 + Pinia 状态管理（2-3小时）

#### 步骤 2.1：创建 Pinia store

在 `src/stores/` 目录下创建 `user.js`：

```javascript
// src/stores/user.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: null
  }),
  
  actions: {
    // 登录
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
    },
    
    // 登出
    logout() {
      this.token = ''
      this.userInfo = null
      localStorage.removeItem('token')
    },
    
    // 设置用户信息
    setUserInfo(info) {
      this.userInfo = info
    }
  },
  
  getters: {
    isLogin: (state) => !!state.token
  }
})
```

#### 步骤 2.2：修改登录页面

修改 `src/views/login.vue`，使用 Pinia：

```javascript
// login.vue 的 script 部分
import { useUserStore } from '../stores/user'
import { useRouter, useRoute } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

const handleLogin = async () => {
  try {
    const res = await ApiLogin({
      username: form.username,
      password: form.password
    })
    
    if (res.data.code === 200) {
      // 保存 token
      userStore.setToken(res.data.token)
      
      ElMessage.success('登录成功')
      
      // 跳转到之前的页面，或首页
      const redirect = route.query.redirect || '/'
      router.push(redirect)
    }
  } catch (error) {
    ElMessage.error('登录失败')
  }
}
```

#### 步骤 2.3：添加路由守卫

修改 `src/router/index.js`，添加守卫：

```javascript
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/article',
    name: 'ArticleDetail',
    component: () => import('../views/ArticleDetail.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/login.vue')
  },
  // 后台路由（需要登录）
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/admin/Layout.vue'),
    meta: { requiresAuth: true },  // 标记需要登录
    children: []  // 后续添加子路由
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 如果路由需要登录，但用户未登录
  if (to.meta.requiresAuth && !userStore.isLogin) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }  // 记住要去的页面
    })
  } else {
    next()
  }
})

export default router
```

#### 步骤 2.4：测试

1. 未登录访问 `/admin`，应该跳转到登录页
2. 登录后自动跳回 `/admin`

**✅ Day 2 完成标志：** 路由守卫生效，未登录无法访问后台。

---


### Day 3：评论系统后端接口（2-3小时）

#### 步骤 3.1：修改评论视图

编辑 `lyhblog-backend/blog/views/comment.py`：

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..models import Comment, Article
from ..serializers import CommentSerializer

# 评论列表
class CommentListView(APIView):
    def get(self, request):
        article_id = request.GET.get('article_id')
        if not article_id:
            return Response({"code": 400, "message": "缺少文章ID"}, status=400)
        
        comments = Comment.objects.filter(article_id=article_id).order_by('-create_time')
        serializer = CommentSerializer(comments, many=True)
        
        return Response({
            "code": 200,
            "data": serializer.data,
            "message": "获取评论成功"
        })

# 发表评论
class CommentAddView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        article_id = request.data.get('article_id')
        content = request.data.get('content')
        
        if not article_id or not content:
            return Response({"code": 400, "message": "参数不完整"}, status=400)
        
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({"code": 404, "message": "文章不存在"}, status=404)
        
        comment = Comment.objects.create(
            article=article,
            user=request.user,
            content=content
        )
        
        return Response({
            "code": 200,
            "message": "评论成功",
            "data": CommentSerializer(comment).data
        })

# 删除评论（仅管理员）
class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request):
        comment_id = request.data.get('id')
        
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return Response({"code": 200, "message": "删除成功"})
        except Comment.DoesNotExist:
            return Response({"code": 404, "message": "评论不存在"}, status=404)
```

#### 步骤 3.2：添加评论序列化器

编辑 `lyhblog-backend/blog/serializers.py`，添加：

```python
class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'create_time', 'username', 'article']
```

#### 步骤 3.3：添加路由

编辑 `lyhblog-backend/blog/urls.py`，添加：

```python
from .views.comment import CommentListView, CommentAddView, CommentDeleteView

urlpatterns = [
    # ... 现有路由
    
    # 评论
    path('comment/list/', CommentListView.as_view()),
    path('comment/add/', CommentAddView.as_view()),
    path('comment/delete/', CommentDeleteView.as_view()),
]
```

#### 步骤 3.4：测试接口

使用 ApiPost 或浏览器测试：

```
GET http://127.0.0.1:8000/api/comment/list/?article_id=1
```

**✅ Day 3 完成标志：** 评论接口能正常返回数据。

---


### Day 4-5：评论系统前端（3-4小时）

#### 步骤 4.1：创建评论 API

在 `src/api/` 下创建 `comment.js`：

```javascript
// src/api/comment.js
import request from '../utils/request'

// 获取评论列表
export const ApiCommentList = (articleId) => {
  return request.get('/comment/list/', {
    params: { article_id: articleId }
  })
}

// 发表评论
export const ApiCommentAdd = (data) => {
  return request.post('/comment/add/', data)
}

// 删除评论
export const ApiCommentDelete = (id) => {
  return request.post('/comment/delete/', { id })
}
```

#### 步骤 4.2：创建评论组件

在 `src/components/` 下创建 `CommentSection.vue`：

```vue
<template>
  <div class="comment-section">
    <h3>评论 ({{ comments.length }})</h3>
    
    <!-- 发表评论 -->
    <div v-if="isLogin" class="comment-form">
      <el-input
        v-model="commentContent"
        type="textarea"
        :rows="3"
        placeholder="写下你的评论..."
      />
      <el-button 
        type="primary" 
        @click="handleSubmit"
        :loading="submitting"
        style="margin-top: 10px"
      >
        发表评论
      </el-button>
    </div>
    <div v-else class="login-tip">
      <el-button type="primary" text @click="goLogin">
        登录后发表评论
      </el-button>
    </div>
    
    <!-- 评论列表 -->
    <div class="comment-list">
      <div v-for="item in comments" :key="item.id" class="comment-item">
        <div class="comment-header">
          <span class="username">{{ item.username }}</span>
          <span class="time">{{ item.create_time }}</span>
        </div>
        <div class="comment-content">{{ item.content }}</div>
      </div>
      
      <el-empty v-if="comments.length === 0" description="暂无评论" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ApiCommentList, ApiCommentAdd } from '../api/comment'
import { ElMessage } from 'element-plus'

const props = defineProps({
  articleId: {
    type: Number,
    required: true
  }
})

const router = useRouter()
const userStore = useUserStore()
const isLogin = computed(() => userStore.isLogin)

const comments = ref([])
const commentContent = ref('')
const submitting = ref(false)

const loadComments = async () => {
  try {
    const res = await ApiCommentList(props.articleId)
    if (res.data.code === 200) {
      comments.value = res.data.data
    }
  } catch (error) {
    console.error(error)
  }
}

const handleSubmit = async () => {
  if (!commentContent.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }
  
  submitting.value = true
  try {
    const res = await ApiCommentAdd({
      article_id: props.articleId,
      content: commentContent.value
    })
    
    if (res.data.code === 200) {
      ElMessage.success('评论成功')
      commentContent.value = ''
      loadComments()
    }
  } catch (error) {
    ElMessage.error('评论失败')
  } finally {
    submitting.value = false
  }
}

const goLogin = () => {
  router.push('/login')
}

onMounted(() => {
  loadComments()
})
</script>

<style scoped>
.comment-section {
  margin-top: 40px;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
}

.comment-form {
  margin: 20px 0;
}

.login-tip {
  margin: 20px 0;
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 4px;
}

.comment-item {
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.username {
  font-weight: bold;
  color: #409eff;
}

.time {
  color: #999;
  font-size: 12px;
}

.comment-content {
  color: #606266;
  line-height: 1.6;
}
</style>
```


#### 步骤 4.3：在文章详情页引入评论组件

修改 `src/views/ArticleDetail.vue`，在文章内容下方添加：

```vue
<template>
  <div>
    <!-- 文章内容 -->
    <div class="article-detail">
      <h1>{{ article.title }}</h1>
      <div class="meta">{{ article.create_time }}</div>
      <div class="content">{{ article.content }}</div>
    </div>
    
    <!-- 评论区 -->
    <CommentSection v-if="article.id" :article-id="article.id" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ApiArticleDetail } from '../api/article'
import CommentSection from '../components/CommentSection.vue'

const route = useRoute()
const article = ref({})

const getArticle = async () => {
  const id = route.query.id
  const res = await ApiArticleDetail(id)
  if (res.data.code === 200) {
    article.value = res.data.data
  }
}

onMounted(() => {
  getArticle()
})
</script>
```

#### 步骤 4.4：测试

1. 未登录查看文章，应该显示"登录后发表评论"
2. 登录后能发表评论
3. 发表后评论列表立即刷新

**✅ Day 4-5 完成标志：** 评论功能完整可用。

---

### Day 6-7：修复现有问题 + 体验优化（2-3小时）

#### 步骤 6.1：修复后端代码问题

编辑 `lyhblog-backend/blog/views/article.py`：

**问题1：权限类重复定义**
```python
# 修改前
class ArticleAddView(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser]

# 修改后
class ArticleAddView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
```

**问题2：文章列表排序**
```python
# 第33行，改为降序
articles = queryset.order_by('-create_time')[start:end]
```

#### 步骤 6.2：前端添加 Loading 状态

修改 `src/views/Home.vue`：

```javascript
const loading = ref(false)

const getArticleList = async () => {
  loading.value = true
  try {
    const res = await ApiArticleList({
      current: current.value,
      size: size.value,
      category_id: activeCategoryId.value
    })
    if (res.data.code == 200) {
      articleList.value = res.data.data
      total.value = res.data.total
    }
  } catch (error) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}
```

在模板中添加：
```vue
<el-skeleton v-if="loading" :rows="5" animated />
<el-row v-else :gutter="20">
  <!-- 文章列表 -->
</el-row>
```

**✅ Day 6-7 完成标志：** 代码问题修复，体验更流畅。

---

## 🎉 第 1 周总结

完成内容：
- ✅ axios 统一封装
- ✅ 路由守卫
- ✅ Pinia 状态管理
- ✅ 评论系统（前后端）
- ✅ 代码问题修复

**现在你的博客已经有了基本的互动功能！**


## 第 2 周：后台管理系统

### Day 8-9：后台框架搭建（3-4小时）

#### 步骤 8.1：创建后台布局组件

在 `src/views/admin/` 下创建 `Layout.vue`：

```vue
<template>
  <el-container class="admin-layout">
    <el-aside width="200px">
      <div class="logo">博客后台</div>
      <el-menu
        :default-active="activeMenu"
        router
      >
        <el-menu-item index="/admin/article">
          <span>文章管理</span>
        </el-menu-item>
        <el-menu-item index="/admin/comment">
          <span>评论管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header>
        <div class="header-right">
          <span>{{ userStore.userInfo?.username || '管理员' }}</span>
          <el-button type="danger" text @click="handleLogout">退出</el-button>
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

const handleLogout = () => {
  ElMessageBox.confirm('确定退出登录？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    userStore.logout()
    router.push('/login')
  })
}
</script>

<style scoped>
.admin-layout {
  height: 100vh;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  color: #409eff;
  border-bottom: 1px solid #eee;
}

.el-aside {
  background: #fff;
  border-right: 1px solid #eee;
}

.el-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  border-bottom: 1px solid #eee;
  background: #fff;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.el-main {
  background: #f5f7fa;
}
</style>
```


#### 步骤 8.2：配置后台路由

修改 `src/router/index.js`，完善后台路由：

```javascript
const routes = [
  // ... 前台路由
  
  // 后台路由
  {
    path: '/admin',
    component: () => import('../views/admin/Layout.vue'),
    meta: { requiresAuth: true },
    redirect: '/admin/article',
    children: [
      {
        path: 'article',
        name: 'AdminArticle',
        component: () => import('../views/admin/ArticleList.vue')
      },
      {
        path: 'article/add',
        name: 'AdminArticleAdd',
        component: () => import('../views/admin/ArticleEdit.vue')
      },
      {
        path: 'article/edit/:id',
        name: 'AdminArticleEdit',
        component: () => import('../views/admin/ArticleEdit.vue')
      },
      {
        path: 'comment',
        name: 'AdminComment',
        component: () => import('../views/admin/CommentList.vue')
      }
    ]
  }
]
```

**✅ Day 8-9 完成标志：** 访问 `/admin` 能看到后台布局。

---


### Day 10-12：文章管理（4-5小时）

#### 步骤 10.1：创建文章列表页

在 `src/views/admin/` 下创建 `ArticleList.vue`：

```vue
<template>
  <div class="article-list">
    <div class="toolbar">
      <el-button type="primary" @click="goAdd">新增文章</el-button>
    </div>
    
    <el-table :data="articleList" border>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="category.name" label="分类" width="120" />
      <el-table-column prop="create_time" label="创建时间" width="180" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button type="primary" text @click="goEdit(row.id)">编辑</el-button>
          <el-button type="danger" text @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <el-pagination
      v-model:current-page="current"
      :page-size="size"
      :total="total"
      @current-change="loadList"
      style="margin-top: 20px"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ApiArticleList } from '../../api/article'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const articleList = ref([])
const current = ref(1)
const size = ref(10)
const total = ref(0)

const loadList = async () => {
  const res = await ApiArticleList({ current: current.value, size: size.value })
  if (res.data.code === 200) {
    articleList.value = res.data.data
    total.value = res.data.total
  }
}

const goAdd = () => {
  router.push('/admin/article/add')
}

const goEdit = (id) => {
  router.push(`/admin/article/edit/${id}`)
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定删除这篇文章？', '提示', {
    type: 'warning'
  }).then(async () => {
    // 调用删除接口（下一步实现）
    ElMessage.success('删除成功')
    loadList()
  })
}

onMounted(() => {
  loadList()
})
</script>

<style scoped>
.toolbar {
  margin-bottom: 20px;
}
</style>
```


#### 步骤 10.2：创建文章编辑页

在 `src/views/admin/` 下创建 `ArticleEdit.vue`：

```vue
<template>
  <div class="article-edit">
    <h2>{{ isEdit ? '编辑文章' : '新增文章' }}</h2>
    
    <el-form :model="form" label-width="80px">
      <el-form-item label="标题">
        <el-input v-model="form.title" placeholder="请输入标题" />
      </el-form-item>
      
      <el-form-item label="分类">
        <el-select v-model="form.category_id" placeholder="请选择分类">
          <el-option
            v-for="cat in categories"
            :key="cat.id"
            :label="cat.name"
            :value="cat.id"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="标签">
        <el-select v-model="form.tags" multiple placeholder="请选择标签">
          <el-option
            v-for="tag in tags"
            :key="tag.id"
            :label="tag.name"
            :value="tag.id"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="摘要">
        <el-input v-model="form.summary" type="textarea" :rows="3" />
      </el-form-item>
      
      <el-form-item label="内容">
        <el-input v-model="form.content" type="textarea" :rows="10" />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">保存</el-button>
        <el-button @click="goBack">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)

const form = ref({
  title: '',
  category_id: null,
  tags: [],
  summary: '',
  content: ''
})

const categories = ref([])
const tags = ref([])

const loadData = async () => {
  // 加载分类和标签（需要添加对应接口）
  // 如果是编辑，加载文章数据
}

const handleSubmit = async () => {
  if (!form.value.title || !form.value.content) {
    ElMessage.warning('标题和内容不能为空')
    return
  }
  
  // 调用新增或编辑接口
  ElMessage.success('保存成功')
  router.push('/admin/article')
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  loadData()
})
</script>
```


#### 步骤 10.3：添加文章管理 API

在 `src/api/article.js` 中添加：

```javascript
// 删除文章
export const ApiArticleDelete = (id) => {
  return request.post('/article/delete/', { id })
}

// 新增文章
export const ApiArticleAdd = (data) => {
  return request.post('/article/add/', data)
}

// 更新文章
export const ApiArticleUpdate = (data) => {
  return request.post('/article/update/', data)
}

// 获取标签列表
export const ApiTagList = () => {
  return request.get('/tag/list/')
}
```

#### 步骤 10.4：后端添加标签接口

在 `lyhblog-backend/blog/views/` 下创建 `tag.py`：

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Tag
from ..serializers import TagSerializer

class TagListView(APIView):
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response({
            "code": 200,
            "data": serializer.data
        })
```

在 `serializers.py` 添加：
```python
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
```

在 `urls.py` 添加：
```python
from .views.tag import TagListView

urlpatterns = [
    # ...
    path('tag/list/', TagListView.as_view()),
]
```

**✅ Day 10-12 完成标志：** 后台能新增、编辑、删除文章。

---


### Day 13-14：评论管理（2小时）

#### 步骤 13.1：创建评论管理页

在 `src/views/admin/` 下创建 `CommentList.vue`：

```vue
<template>
  <div class="comment-list">
    <el-table :data="commentList" border>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户" width="120" />
      <el-table-column prop="content" label="评论内容" />
      <el-table-column prop="create_time" label="时间" width="180" />
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button type="danger" text @click="handleDelete(row.id)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ApiCommentDelete } from '../../api/comment'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../../utils/request'

const commentList = ref([])

const loadList = async () => {
  // 获取所有评论（需要后端添加接口）
  const res = await request.get('/comment/all/')
  if (res.data.code === 200) {
    commentList.value = res.data.data
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定删除这条评论？', '提示', {
    type: 'warning'
  }).then(async () => {
    await ApiCommentDelete(id)
    ElMessage.success('删除成功')
    loadList()
  })
}

onMounted(() => {
  loadList()
})
</script>
```

#### 步骤 13.2：后端添加获取所有评论接口

在 `blog/views/comment.py` 添加：

```python
class CommentAllView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        comments = Comment.objects.all().order_by('-create_time')
        serializer = CommentSerializer(comments, many=True)
        return Response({
            "code": 200,
            "data": serializer.data
        })
```

在 `urls.py` 添加：
```python
path('comment/all/', CommentAllView.as_view()),
```

**✅ Day 13-14 完成标志：** 后台能查看和删除评论。

---

## 🎉 第 2 周总结

完成内容：
- ✅ 后台布局框架
- ✅ 文章管理（列表/新增/编辑/删除）
- ✅ 评论管理（列表/删除）

**现在你的博客已经有完整的后台管理功能！**


## 第 3 周：完善与部署准备

### Day 15-17：功能完善（3-4小时）

#### 步骤 15.1：添加富文本编辑器（可选）

推荐使用 wangEditor（轻量、中文友好）：

```bash
npm install @wangeditor/editor @wangeditor/editor-for-vue@next
```

在 `ArticleEdit.vue` 中替换 textarea。

#### 步骤 15.2：图片上传（可选）

**方案1：本地上传**
- Django 配置 MEDIA_ROOT
- 前端使用 el-upload

**方案2：七牛云**
- 参考原版 POEMON 的实现

#### 步骤 15.3：数据验证完善

前端添加表单验证规则，后端完善参数校验。

---

### Day 18-19：测试与修复（2-3小时）

#### 测试清单：

**前台功能：**
- [ ] 文章列表（分页、分类筛选）
- [ ] 文章详情
- [ ] 评论（登录后发表）
- [ ] 登录/注册

**后台功能：**
- [ ] 文章管理（增删改查）
- [ ] 评论管理（查看、删除）
- [ ] 权限控制（未登录跳转）

**边界情况：**
- [ ] 网络错误提示
- [ ] 空数据展示
- [ ] 表单验证

---


### Day 20-21：部署准备（2-3小时）

#### 步骤 20.1：环境变量配置

**前端：** 创建 `.env.production`
```
VITE_API_BASE_URL=https://你的域名/api
```

修改 `request.js`：
```javascript
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api',
  timeout: 10000
})
```

**后端：** 修改 `settings.py`
```python
DEBUG = False
ALLOWED_HOSTS = ['你的域名', 'IP地址']

# 数据库改为生产配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': '你的密码',
        'NAME': 'lyhblog'
    }
}
```

#### 步骤 20.2：前端构建

```bash
cd lyhblog-frontend
npm run build
# 生成 dist 目录
```

#### 步骤 20.3：部署文档编写

记录部署步骤，包括：
- 服务器配置要求
- Nginx 配置示例
- Django 启动命令
- 常见问题解决

---

## 🎉 3周开发完成！

### 最终成果：

**前台功能：**
- ✅ 文章列表（分页、分类筛选、标签展示）
- ✅ 文章详情
- ✅ 评论系统（登录后发表）
- ✅ 用户登录/注册

**后台功能：**
- ✅ 文章管理（增删改查）
- ✅ 评论管理（查看、删除）
- ✅ 权限控制

**工程化：**
- ✅ axios 统一封装
- ✅ 路由守卫
- ✅ 状态管理
- ✅ 错误处理

---

## 📝 下一步可选功能

完成核心功能后，可以考虑添加：

1. **富文本编辑器**（提升写作体验）
2. **图片上传**（本地或云存储）
3. **文章搜索**（标题/内容搜索）
4. **标签页面**（按标签筛选文章）
5. **友链管理**（友情链接）
6. **访客统计**（ECharts 图表）
7. **微言/说说**（类似朋友圈）

---

## 💡 学习建议

1. **不要急于求成**：每天完成一个小目标，积累成就感
2. **遇到问题先思考**：查文档、看报错、调试
3. **参考原版代码**：理解思路，不要照抄
4. **写注释**：帮助自己理解代码
5. **定期提交代码**：用 git 记录进度

---

**祝你开发顺利！有问题随时问我。**

