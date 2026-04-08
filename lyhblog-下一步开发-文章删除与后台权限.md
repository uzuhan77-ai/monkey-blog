# lyhblog 下一步开发：文章删除与后台权限

> 这一轮先不要开新功能。  
> 最该先补的是两件事：
>
> 1. 后台文章列表的“删除”要变成真删除
> 2. 后台页面要限制为管理员才能进入

---

## 一、这一轮为什么先做这两步

你现在的后台已经有这些基础：

- 文章列表页
- 文章新增/编辑页
- 评论管理页

但还差两个关键闭环：

1. `ArticleList.vue` 里的删除只是弹窗后提示成功，还没有真的调接口
2. 前端路由守卫现在只判断“有没有 token”，没有判断“是不是管理员”

如果这两步不补：

- 后台文章管理不算真正可用
- 普通用户也能进后台页面

所以当前最合适的顺序就是：

1. 先补文章真删除
2. 再补管理员权限判断

---

## 二、第 1 步：先补文章真删除

### 你要改的文件

- `lyhblog-frontend/src/views/admin/ArticleList.vue`

### 这一段的目标

- 点击删除按钮
- 调用后端 `/article/delete/`
- 删除成功后刷新列表

### 说明

你现在的 `src/api/article.js` 里 `ApiArticleDelete` 已经有了，所以这一步主要改页面逻辑。

### 完整代码：`lyhblog-frontend/src/views/admin/ArticleList.vue`

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
import { ApiArticleList, ApiArticleDelete } from '../../api/article'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const articleList = ref([])
const current = ref(1)
const size = ref(10)
const total = ref(0)

const loadList = async () => {
  try {
    const res = await ApiArticleList({
      current: current.value,
      size: size.value
    })

    if (res.data.code === 200) {
      articleList.value = res.data.data
      total.value = res.data.total
    }
  } catch (error) {
    ElMessage.error('文章列表加载失败')
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
  })
    .then(async () => {
      try {
        const res = await ApiArticleDelete(id)

        if (res.data.code === 200) {
          ElMessage.success('删除成功')
          await loadList()
        }
      } catch (error) {
        ElMessage.error('删除失败')
      }
    })
    .catch(() => {})
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

### 这一小步的验收

你改完后，自己测试：

1. 打开 `/admin/article`
2. 点击某篇文章的删除按钮
3. 确认弹窗后，文章能真的被删掉
4. 列表自动刷新

---

## 三、第 2 步：补后台管理员权限

这一部分的目标是：

- 普通登录用户不能进入 `/admin`
- 管理员登录后可以进入 `/admin`
- 页面右上角能显示用户名

这一段一共改 4 个文件：

- `lyhblog-backend/blog/views/auth.py`
- `lyhblog-frontend/src/stores/user.js`
- `lyhblog-frontend/src/views/Login.vue`
- `lyhblog-frontend/src/router/index.js`

---

## 四、后端登录接口要返回管理员信息

### 为什么这一步要改

前端要判断一个用户能不能进后台，必须知道：

- 用户名
- 是否管理员

这里的“是否管理员”建议返回 `user.is_staff`，这样和 Django/DRF 里的 `IsAdminUser` 保持一致。

### 完整代码：`lyhblog-backend/blog/views/auth.py`

```python
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


class TestView(APIView):
    def get(self, request):
        return Response({'message': 'hello', 'code': 200}, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        account = request.data.get('account')
        password = request.data.get('password')

        if not account or not password:
            return Response({
                "code": 400,
                "message": "账号和密码不能为空"
            }, status=400)

        user = authenticate(username=account, password=password)
        if user is None:
            return Response({
                "code": 400,
                "message": "账号或密码错误"
            }, status=400)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "code": 200,
            "message": "登录成功",
            "token": token.key,
            "username": user.username,
            "is_admin": user.is_staff
        })


class RegisterView(APIView):
    def post(self, request):
        account = request.data.get('account')
        password = request.data.get('password')

        if not account or not password:
            return Response({
                "code": 400,
                "message": "账号和密码不能为空"
            }, status=400)

        if User.objects.filter(username=account).exists():
            return Response({
                "code": 400,
                "message": "用户名已存在"
            }, status=400)

        User.objects.create_user(username=account, password=password)

        return Response({
            "code": 200,
            "message": "注册成功"
        })
```

---

## 五、前端用户状态里要存管理员信息

### 完整代码：`lyhblog-frontend/src/stores/user.js`

```javascript
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('user_info') || 'null'),
    isAdmin: localStorage.getItem('is_admin') === 'true'
  }),

  actions: {
    setLoginInfo(data) {
      this.token = data.token
      this.userInfo = {
        username: data.username
      }
      this.isAdmin = data.is_admin

      localStorage.setItem('token', data.token)
      localStorage.setItem('user_info', JSON.stringify(this.userInfo))
      localStorage.setItem('is_admin', String(data.is_admin))
    },

    logout() {
      this.token = ''
      this.userInfo = null
      this.isAdmin = false

      localStorage.removeItem('token')
      localStorage.removeItem('user_info')
      localStorage.removeItem('is_admin')
    }
  },

  getters: {
    isLogin: (state) => !!state.token
  }
})
```

---

## 六、登录页要把用户名和管理员身份存进去

### 完整代码：`lyhblog-frontend/src/views/Login.vue`

```vue
<template>
  <div>
    <h1>登录</h1>

    <input type="text" v-model="account" placeholder="账号" />
    <input type="password" v-model="password" placeholder="密码" />

    <button @click="handleLogin">登录</button>
    <button @click="router.push('/register')">没有账号？去注册</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ApiLogin } from '../api/article'
import { useUserStore } from '../stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const account = ref('')
const password = ref('')

const handleLogin = async () => {
  if (!account.value || !password.value) {
    ElMessage.error('账号和密码不能为空')
    return
  }

  try {
    const res = await ApiLogin({
      account: account.value,
      password: password.value
    })

    if (res.data.code === 200) {
      userStore.setToken(res.data.token)

      ElMessage.success('登录成功')

      const redirect = route.query.redirect || (res.data.is_admin ? '/admin/article' : '/')
      router.push(redirect)
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '登录失败')
  }
}
</script>
```

---

## 七、路由守卫要拦住普通用户

### 完整代码：`lyhblog-frontend/src/router/index.js`

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
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
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/register.vue')
  },
    
  {
    path: '/admin',
    component: () => import('../views/admin/Layout.vue'),
    meta: { requiresAuth: true},
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

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const requiresAdmin = to.matched.some((record) => record.meta.requiresAdmin)

  if (requiresAuth && !userStore.isLogin) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
    return
  }

  if (requiresAdmin && !userStore.isAdmin) {
    ElMessage.error('没有后台权限')
    next('/')
    return
  }

  next()
})

export default router
```

---

## 八、这一轮做完后怎么验收

你按这个顺序测：

### 1. 文章删除

- 登录管理员账号
- 进入 `/admin/article`
- 删除一篇文章
- 删除后列表刷新

### 2. 管理员权限

- 用普通用户登录
- 手动访问 `/admin/article`
- 应该被拦回首页

### 3. 管理员登录跳转

- 用管理员登录
- 登录成功后可以进入后台
- 右上角能看到用户名

---

## 九、这一步做完以后，你再做什么

这一轮全部通过后，下一步再做：

1. 分类管理页
2. 标签管理页

原因是：

- 文章编辑页已经依赖分类和标签
- 现在虽然能读分类和标签，但后台还不能管理它们

所以最顺的节奏是：

1. 文章真删除
2. 管理员权限
3. 分类管理
4. 标签管理

---

## 十、你现在就照这个顺序写

不要同时改一大堆文件。

推荐顺序：

1. 先只改 `ArticleList.vue`
2. 测试文章删除
3. 再改 `auth.py`
4. 再改 `user.js`
5. 再改 `Login.vue`
6. 最后改 `router/index.js`
7. 再整体验收后台权限

如果你写到某一步卡住，直接带着这句话来找我：

- `我现在写到 ArticleList 删除了，帮我看`
- `我现在写到 user store 了，帮我查`
- `我现在普通用户还能进 /admin，帮我看`

这样我可以直接接着你当前卡住的位置继续带你。
