# lyhblog 下一步开发：分类与标签管理

> 这一轮的目标：
>
> 1. 后台可以管理分类
> 2. 后台可以管理标签
> 3. 文章编辑页依赖的分类/标签，不再只能“读”，而是能真正维护

---

## 一、为什么下一步做这个

你现在已经有：

- 后台文章列表
- 后台文章新增/编辑
- 后台评论管理

但文章编辑页里的：

- 分类下拉
- 标签多选

目前都只是“从后端读出来”，后台还没有对应的管理页面。

所以当前最顺的一步就是：

1. 先做分类管理
2. 再做标签管理

这两块做法几乎一样，标签就是把分类那套再抄一遍。

---

## 二、开始前先自查上一轮有没有完全落地

我按你当前仓库快照看，上一轮权限收口可能还有两个小残留。

如果你本地已经改好了，就跳过这一节。

如果还没改完，先补这两个点，不然后面 `/admin/category`、`/admin/tag` 路由会出问题：

### 1. `Login.vue`

登录成功后，应该调用：

```javascript
userStore.setLoginInfo(res.data)
```

而不是：

```javascript
userStore.setToken(res.data.token)
```

### 2. `router/index.js`

后台路由应该带上：

```javascript
meta: { requiresAuth: true, requiresAdmin: true }
```

并且 `beforeEach` 最后一定要有：

```javascript
next()
```

否则路由可能卡住不跳转。

---

## 三、这一轮要改哪些文件

### 后端

- `lyhblog-backend/blog/views/category.py`
- `lyhblog-backend/blog/views/tag.py`
- `lyhblog-backend/blog/urls.py`

### 前端

- 新建 `lyhblog-frontend/src/api/category.js`
- 新建 `lyhblog-frontend/src/api/tag.js`
- 新建 `lyhblog-frontend/src/views/admin/CategoryList.vue`
- 新建 `lyhblog-frontend/src/views/admin/TagList.vue`
- `lyhblog-frontend/src/router/index.js`
- `lyhblog-frontend/src/views/admin/Layout.vue`

---

## 四、先做分类管理

---

## 五、后端：分类 CRUD

### 完整代码：`lyhblog-backend/blog/views/category.py`

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Category
from ..serializers import CategorySerializer


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all().order_by('id')
        serializer = CategorySerializer(categories, many=True)
        return Response({
            "code": 200,
            "data": serializer.data,
            "message": "获取分类列表成功"
        })


class CategoryAddView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        name = (request.data.get('name') or '').strip()

        if not name:
            return Response({
                "code": 400,
                "message": "分类名称不能为空"
            }, status=400)

        if Category.objects.filter(name=name).exists():
            return Response({
                "code": 400,
                "message": "分类已存在"
            }, status=400)

        category = Category.objects.create(name=name)
        return Response({
            "code": 200,
            "message": "分类新增成功",
            "data": CategorySerializer(category).data
        })


class CategoryUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        category_id = request.data.get('id')
        name = (request.data.get('name') or '').strip()

        if not category_id:
            return Response({
                "code": 400,
                "message": "缺少分类 id"
            }, status=400)

        if not name:
            return Response({
                "code": 400,
                "message": "分类名称不能为空"
            }, status=400)

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({
                "code": 404,
                "message": "分类不存在"
            }, status=404)

        if Category.objects.filter(name=name).exclude(id=category_id).exists():
            return Response({
                "code": 400,
                "message": "分类名称已存在"
            }, status=400)

        category.name = name
        category.save()

        return Response({
            "code": 200,
            "message": "分类修改成功",
            "data": CategorySerializer(category).data
        })


class CategoryDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        category_id = request.data.get('id')

        if not category_id:
            return Response({
                "code": 400,
                "message": "缺少分类 id"
            }, status=400)

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({
                "code": 404,
                "message": "分类不存在"
            }, status=404)

        category.delete()

        return Response({
            "code": 200,
            "message": "分类删除成功"
        })
```

---

## 六、前端：分类 API

### 新建文件：`lyhblog-frontend/src/api/category.js`

```javascript
import request from '../utils/request'

export const ApiCategoryList = () => {
  return request.get('/category/list/')
}

export const ApiCategoryAdd = (data) => {
  return request.post('/category/add/', data)
}

export const ApiCategoryUpdate = (data) => {
  return request.post('/category/update/', data)
}

export const ApiCategoryDelete = (id) => {
  return request.post('/category/delete/', { id })
}
```

---

## 七、前端：分类管理页

### 新建文件：`lyhblog-frontend/src/views/admin/CategoryList.vue`

```vue
<template>
  <div class="category-page">
    <div class="toolbar">
      <el-input
        v-model="form.name"
        placeholder="请输入分类名称"
        style="width: 240px"
      />
      <el-button type="primary" @click="handleSubmit">
        {{ form.id ? '保存修改' : '新增分类' }}
      </el-button>
      <el-button v-if="form.id" @click="resetForm">取消编辑</el-button>
    </div>

    <el-table :data="categoryList" border>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="分类名称" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button type="primary" text @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" text @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ApiCategoryList,
  ApiCategoryAdd,
  ApiCategoryUpdate,
  ApiCategoryDelete
} from '../../api/category'

const categoryList = ref([])

const form = ref({
  id: null,
  name: ''
})

const loadList = async () => {
  try {
    const res = await ApiCategoryList()
    if (res.data.code === 200) {
      categoryList.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('分类列表加载失败')
  }
}

const resetForm = () => {
  form.value = {
    id: null,
    name: ''
  }
}

const handleEdit = (row) => {
  form.value = {
    id: row.id,
    name: row.name
  }
}

const handleSubmit = async () => {
  if (!form.value.name.trim()) {
    ElMessage.warning('分类名称不能为空')
    return
  }

  try {
    const res = form.value.id
      ? await ApiCategoryUpdate(form.value)
      : await ApiCategoryAdd({ name: form.value.name })

    if (res.data.code === 200) {
      ElMessage.success(form.value.id ? '分类修改成功' : '分类新增成功')
      resetForm()
      loadList()
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '操作失败')
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定删除这个分类？', '提示', {
    type: 'warning'
  })
    .then(async () => {
      try {
        const res = await ApiCategoryDelete(id)
        if (res.data.code === 200) {
          ElMessage.success('分类删除成功')
          loadList()
        }
      } catch (error) {
        ElMessage.error(error.response?.data?.message || '删除失败')
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
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}
</style>
```

---

## 八、再做标签管理

标签管理基本就是把“分类”整套逻辑复制一份。

---

## 九、后端：标签 CRUD

### 完整代码：`lyhblog-backend/blog/views/tag.py`

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Tag
from ..serializers import TagSerializer


class TagListView(APIView):
    def get(self, request):
        tags = Tag.objects.all().order_by('id')
        serializer = TagSerializer(tags, many=True)
        return Response({
            "code": 200,
            "data": serializer.data,
            "message": "获取标签列表成功"
        })


class TagAddView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        name = (request.data.get('name') or '').strip()

        if not name:
            return Response({
                "code": 400,
                "message": "标签名称不能为空"
            }, status=400)

        if Tag.objects.filter(name=name).exists():
            return Response({
                "code": 400,
                "message": "标签已存在"
            }, status=400)

        tag = Tag.objects.create(name=name)
        return Response({
            "code": 200,
            "message": "标签新增成功",
            "data": TagSerializer(tag).data
        })


class TagUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        tag_id = request.data.get('id')
        name = (request.data.get('name') or '').strip()

        if not tag_id:
            return Response({
                "code": 400,
                "message": "缺少标签 id"
            }, status=400)

        if not name:
            return Response({
                "code": 400,
                "message": "标签名称不能为空"
            }, status=400)

        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return Response({
                "code": 404,
                "message": "标签不存在"
            }, status=404)

        if Tag.objects.filter(name=name).exclude(id=tag_id).exists():
            return Response({
                "code": 400,
                "message": "标签名称已存在"
            }, status=400)

        tag.name = name
        tag.save()

        return Response({
            "code": 200,
            "message": "标签修改成功",
            "data": TagSerializer(tag).data
        })


class TagDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        tag_id = request.data.get('id')

        if not tag_id:
            return Response({
                "code": 400,
                "message": "缺少标签 id"
            }, status=400)

        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return Response({
                "code": 404,
                "message": "标签不存在"
            }, status=404)

        tag.delete()

        return Response({
            "code": 200,
            "message": "标签删除成功"
        })
```

---

## 十、前端：标签 API

### 新建文件：`lyhblog-frontend/src/api/tag.js`

```javascript
import request from '../utils/request'

export const ApiTagList = () => {
  return request.get('/tag/list/')
}

export const ApiTagAdd = (data) => {
  return request.post('/tag/add/', data)
}

export const ApiTagUpdate = (data) => {
  return request.post('/tag/update/', data)
}

export const ApiTagDelete = (id) => {
  return request.post('/tag/delete/', { id })
}
```

---

## 十一、前端：标签管理页

### 新建文件：`lyhblog-frontend/src/views/admin/TagList.vue`

```vue
<template>
  <div class="tag-page">
    <div class="toolbar">
      <el-input
        v-model="form.name"
        placeholder="请输入标签名称"
        style="width: 240px"
      />
      <el-button type="primary" @click="handleSubmit">
        {{ form.id ? '保存修改' : '新增标签' }}
      </el-button>
      <el-button v-if="form.id" @click="resetForm">取消编辑</el-button>
    </div>

    <el-table :data="tagList" border>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="标签名称" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button type="primary" text @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" text @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ApiTagList,
  ApiTagAdd,
  ApiTagUpdate,
  ApiTagDelete
} from '../../api/tag'

const tagList = ref([])

const form = ref({
  id: null,
  name: ''
})

const loadList = async () => {
  try {
    const res = await ApiTagList()
    if (res.data.code === 200) {
      tagList.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('标签列表加载失败')
  }
}

const resetForm = () => {
  form.value = {
    id: null,
    name: ''
  }
}

const handleEdit = (row) => {
  form.value = {
    id: row.id,
    name: row.name
  }
}

const handleSubmit = async () => {
  if (!form.value.name.trim()) {
    ElMessage.warning('标签名称不能为空')
    return
  }

  try {
    const res = form.value.id
      ? await ApiTagUpdate(form.value)
      : await ApiTagAdd({ name: form.value.name })

    if (res.data.code === 200) {
      ElMessage.success(form.value.id ? '标签修改成功' : '标签新增成功')
      resetForm()
      loadList()
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '操作失败')
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定删除这个标签？', '提示', {
    type: 'warning'
  })
    .then(async () => {
      try {
        const res = await ApiTagDelete(id)
        if (res.data.code === 200) {
          ElMessage.success('标签删除成功')
          loadList()
        }
      } catch (error) {
        ElMessage.error(error.response?.data?.message || '删除失败')
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
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}
</style>
```

---

## 十二、把新接口挂到后端路由

### 完整代码：`lyhblog-backend/blog/urls.py`

```python
from django.urls import path

from .views import (
    TestView,
    ArticleListView,
    ArticleDetailView,
    ArticleAddView,
    ArticleDeleteView,
    ArticleUpdateView,
    LoginView,
    RegisterView,
)
from .views.category import (
    CategoryListView,
    CategoryAddView,
    CategoryUpdateView,
    CategoryDeleteView,
)
from .views.tag import (
    TagListView,
    TagAddView,
    TagUpdateView,
    TagDeleteView,
)
from .views.comment import (
    CommentListView,
    CommentAddView,
    CommentDeleteView,
    CommentAllView,
)

urlpatterns = [
    path('test/', TestView.as_view(), name='test'),

    path('user/login/', LoginView.as_view(), name='login'),
    path('user/register/', RegisterView.as_view(), name='register'),

    path('article/listArticle/', ArticleListView.as_view(), name='article-list'),
    path('article/getArticleById/', ArticleDetailView.as_view(), name='article-detail'),
    path('article/add/', ArticleAddView.as_view(), name='article-add'),
    path('article/delete/', ArticleDeleteView.as_view(), name='article-delete'),
    path('article/update/', ArticleUpdateView.as_view(), name='article-update'),

    path('category/list/', CategoryListView.as_view(), name='category-list'),
    path('category/add/', CategoryAddView.as_view(), name='category-add'),
    path('category/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('category/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    path('tag/list/', TagListView.as_view(), name='tag-list'),
    path('tag/add/', TagAddView.as_view(), name='tag-add'),
    path('tag/update/', TagUpdateView.as_view(), name='tag-update'),
    path('tag/delete/', TagDeleteView.as_view(), name='tag-delete'),

    path('comment/list/', CommentListView.as_view(), name='comment-list'),
    path('comment/add/', CommentAddView.as_view(), name='comment-add'),
    path('comment/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('comment/all/', CommentAllView.as_view(), name='comment-all'),
]
```

---

## 十三、把后台路由和菜单加上

这一段默认你上一轮“管理员权限”已经做完。

如果你当前 `router/index.js` 还是旧版，至少要保证两点：

- `/admin` 路由有 `requiresAdmin: true`
- `beforeEach` 最后有 `next()`

### `lyhblog-frontend/src/router/index.js`

在 `/admin` 的 `children` 里加这两段：

```javascript
{
  path: 'category',
  name: 'AdminCategory',
  component: () => import('../views/admin/CategoryList.vue')
},
{
  path: 'tag',
  name: 'AdminTag',
  component: () => import('../views/admin/TagList.vue')
}
```

如果你上一轮管理员权限还没收口，`/admin` 建议写成：

```javascript
meta: { requiresAuth: true, requiresAdmin: true }
```

### `lyhblog-frontend/src/views/admin/Layout.vue`

菜单里加这两项：

```vue
<el-menu-item index="/admin/category">
  <span>分类管理</span>
</el-menu-item>

<el-menu-item index="/admin/tag">
  <span>标签管理</span>
</el-menu-item>
```

---

## 十四、这一轮的验收顺序

### 1. 先验收分类管理

- 打开 `/admin/category`
- 列表能显示
- 可以新增分类
- 可以编辑分类
- 可以删除分类

### 2. 再验收标签管理

- 打开 `/admin/tag`
- 列表能显示
- 可以新增标签
- 可以编辑标签
- 可以删除标签

### 3. 最后验收文章编辑页

- 打开 `/admin/article/add`
- 分类下拉正常显示
- 标签下拉正常显示
- 新增完分类/标签后，文章编辑页能读到最新数据

---

## 十五、推荐你实际动手时的顺序

不要分类和标签一起乱改。

按这个顺序最稳：

1. 先改后端 `category.py`
2. 再改后端 `urls.py`
3. 再建前端 `api/category.js`
4. 再建 `CategoryList.vue`
5. 再加路由和菜单
6. 把分类跑通
7. 然后复制分类那一套去做标签

---

## 十六、这一轮做完以后，你再做什么

分类和标签管理做完后，下一步就可以做：

1. 后台首页概览
2. 富文本编辑器
3. 前台分类页 / 标签页

但这三件事都应该排在“分类/标签后台可维护”之后。

---

## 十七、如果你写到一半卡住，怎么来问我

直接带着你卡住的那一段来，不要只说“又不行了”。

例如：

- `我现在写到 category.py 了，帮我看`
- `我现在 /admin/category 能打开，但新增报 403`
- `我现在标签页能新增，但编辑不生效`

这样我可以直接接着你当前步骤往下带。
