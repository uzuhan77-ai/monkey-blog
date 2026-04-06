# lyhblog 继续开发完整代码参考

> 这份文档不是直接替你改项目。
> 是把你下一步最需要的“完整代码”集中放在一起，方便你自己照着敲。
> 当前重点覆盖：
>
> - 后台文章编辑页 `ArticleEdit.vue`
> - 后台评论管理页 `CommentList.vue`
> - 对应前端接口文件
> - 必须同步的后端小修

---

## 一、先说清楚

如果你只改前端，不改下面两个后端点，前端完整代码也跑不通：

1. `TagSerializer` 里写成了 `field`，应该是 `fields`
2. 评论删除前后端接口路径目前不一致

所以这份文档我会把“前端完整代码”和“后端必须同步的完整代码”一起给你。

---

## 二、前端完整代码

### 1. `lyhblog-frontend/src/api/article.js`

```javascript
import request from '../utils/request'

export function ApiArticleList(data) {
  return request.post('/article/listArticle/', data)
}

export function ApiArticleDetail(id) {
  return request.get('/article/getArticleById/', {
    params: { id }
  })
}

export const ApiArticleAdd = (data) => {
  return request.post('/article/add/', data)
}

export const ApiArticleDelete = (id) => {
  return request.post('/article/delete/', { id })
}

export const ApiArticleUpdate = (data) => {
  return request.post('/article/update/', data)
}

export const ApiTagList = () => {
  return request.get('/tag/list/')
}

export function ApiLogin(data) {
  return request.post('/user/login/', data)
}

export function ApiRegister(data) {
  return request.post('/user/register/', data)
}

export function ApiCategoryList() {
  return request.get('/category/listCategory/')
}
```

---

### 2. `lyhblog-frontend/src/api/comment.js`

```javascript
import request from '../utils/request'

export const ApiCommentList = (articleId) => {
  return request.get('/comment/list/', {
    params: { article_id: articleId }
  })
    }

export const ApiCommentAdd = (data) => {
  return request.post('/comment/add/', data)
}

export const ApiCommentAll = () => {
  return request.get('/comment/all/')
}

export const ApiCommentDelete = (id) => {
  return request.post('/comment/delete/', { id })
}
```

---

### 3. `lyhblog-frontend/src/views/admin/ArticleEdit.vue`

```vue
<template>
  <div class="article-edit">
    <h2>{{ isEdit ? '编辑文章' : '新增文章' }}</h2>

    <el-form :model="form" label-width="80px">
      <el-form-item label="标题">
        <el-input v-model="form.title" placeholder="请输入标题" />
      </el-form-item>

      <el-form-item label="分类">
        <el-select v-model="form.category_id" placeholder="请选择分类" clearable>
          <el-option
            v-for="cat in categories"
            :key="cat.id"
            :label="cat.name"
            :value="cat.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="标签">
        <el-select v-model="form.tags" multiple placeholder="请选择标签" clearable>
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
import {
  ApiArticleAdd,
  ApiArticleDetail,
  ApiArticleUpdate,
  ApiCategoryList,
  ApiTagList
} from '../../api/article'

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

const loadOptions = async () => {
  try {
    const [categoryRes, tagRes] = await Promise.all([
      ApiCategoryList(),
      ApiTagList()
    ])

    if (categoryRes.data.code === 200) {
      categories.value = categoryRes.data.data
    }

    if (tagRes.data.code === 200) {
      tags.value = tagRes.data.data
    }
  } catch (error) {
    ElMessage.error('分类或标签加载失败')
  }
}

const loadArticleDetail = async () => {
  if (!isEdit.value) return

  try {
    const res = await ApiArticleDetail(route.params.id)
    if (res.data.code === 200) {
      const article = res.data.data

      form.value = {
        title: article.title || '',
        category_id: article.category?.id || null,
        tags: article.tags ? article.tags.map((item) => item.id) : [],
        summary: article.summary || '',
        content: article.content || ''
      }
    }
  } catch (error) {
    ElMessage.error('文章详情加载失败')
  }
}

const handleSubmit = async () => {
  if (!form.value.title || !form.value.content) {
    ElMessage.warning('标题和内容不能为空')
    return
  }

  try {
    if (isEdit.value) {
      const res = await ApiArticleUpdate({
        id: route.params.id,
        ...form.value
      })

      if (res.data.code === 200) {
        ElMessage.success('文章修改成功')
        router.push('/admin/article')
      }
    } else {
      const res = await ApiArticleAdd(form.value)

      if (res.data.code === 200) {
        ElMessage.success('文章新增成功')
        router.push('/admin/article')
      }
    }
  } catch (error) {
    ElMessage.error(isEdit.value ? '文章修改失败' : '文章新增失败')
  }
}

const goBack = () => {
  router.back()
}

onMounted(async () => {
  await loadOptions()
  await loadArticleDetail()
})
</script>
```

---

### 4. `lyhblog-frontend/src/views/admin/CommentList.vue`

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
import { ElMessage, ElMessageBox } from 'element-plus'
import { ApiCommentAll, ApiCommentDelete } from '../../api/comment'

const commentList = ref([])

const loadList = async () => {
  try {
    const res = await ApiCommentAll()
    if (res.data.code === 200) {
      commentList.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('评论列表加载失败')
  }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定删除这条评论？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      const res = await ApiCommentDelete(id)
      if (res.data.code === 200) {
        ElMessage.success('删除成功')
        loadList()
      }
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

onMounted(() => {
  loadList()
})
</script>
```

---

## 三、后端必须同步的完整代码

### 1. `lyhblog-backend/blog/serializers.py`

这里最关键的是 `TagSerializer` 的 `fields`。

```python
from rest_framework import serializers
from .models import Article, Category, Tag, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    create_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True
    )

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'summary',
            'content',
            'create_time',
            'tags',
            'category'
        ]


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    create_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'create_time', 'article', 'username']
```

---

### 2. `lyhblog-backend/blog/urls.py`

这里关键是把评论删除路径统一成 `/comment/delete/`，和前端一致。

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
    CategoryListView,
)
from .views.comment import (
    CommentListView,
    CommentAddView,
    CommentDeleteView,
    CommentAllView,
)
from .views.tag import TagListView

urlpatterns = [
    path('test/', TestView.as_view(), name='test'),

    path('article/listArticle/', ArticleListView.as_view(), name='article-list'),
    path('article/getArticleById/', ArticleDetailView.as_view(), name='article-detail'),
    path('article/add/', ArticleAddView.as_view(), name='article-add'),
    path('article/delete/', ArticleDeleteView.as_view(), name='article-delete'),
    path('article/update/', ArticleUpdateView.as_view(), name='article-update'),

    path('user/login/', LoginView.as_view(), name='login'),
    path('user/register/', RegisterView.as_view(), name='register'),

    path('category/listCategory/', CategoryListView.as_view(), name='category-list'),
    path('tag/list/', TagListView.as_view(), name='tag-list'),

    path('comment/list/', CommentListView.as_view(), name='comment-list'),
    path('comment/add/', CommentAddView.as_view(), name='comment-add'),
    path('comment/all/', CommentAllView.as_view(), name='comment-all'),
    path('comment/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]
```

---

### 3. `lyhblog-backend/blog/views/article.py`

这份完整代码主要是统一新增、更新、删除权限写法，并保证 `tags`、`category_id` 都能正常处理。

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Article
from ..serializers import ArticleSerializer


class ArticleListView(APIView):
    def post(self, request):
        current = int(request.data.get('current', 1))
        size = int(request.data.get('size', 10))
        category_id = request.data.get('category_id')

        queryset = Article.objects.all()
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        total = queryset.count()
        start = (current - 1) * size
        end = start + size

        articles = queryset.order_by('-create_time')[start:end]
        serializer = ArticleSerializer(articles, many=True)

        return Response({
            "code": 200,
            "data": serializer.data,
            "total": total,
            "message": "成功获取文章列表"
        })


class ArticleDetailView(APIView):
    def get(self, request):
        article_id = request.GET.get('id')
        if not article_id:
            return Response({
                "code": 400,
                "message": "缺少文章ID参数"
            }, status=400)

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({
                "code": 404,
                "message": "文章不存在"
            }, status=404)

        serializer = ArticleSerializer(article)
        return Response({
            "code": 200,
            "data": serializer.data,
            "message": "成功获取文章详情"
        })


class ArticleAddView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        summary = request.data.get('summary', '')
        category_id = request.data.get('category_id')
        tags = request.data.get('tags', [])

        if not title or not content:
            return Response({
                "code": 400,
                "message": "标题和内容不能为空"
            }, status=400)

        article = Article.objects.create(
            title=title,
            content=content,
            summary=summary,
            category_id=category_id
        )

        if tags:
            article.tags.set(tags)

        return Response({
            "code": 200,
            "message": "文章发布成功"
        })


class ArticleUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        article_id = request.data.get('id')
        if not article_id:
            return Response({
                "code": 400,
                "message": "缺少文章id"
            }, status=400)

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({
                "code": 404,
                "message": "文章不存在"
            }, status=404)

        article.title = request.data.get('title', article.title)
        article.content = request.data.get('content', article.content)
        article.summary = request.data.get('summary', article.summary)
        article.category_id = request.data.get('category_id', article.category_id)
        article.save()

        tags = request.data.get('tags')
        if tags is not None:
            article.tags.set(tags)

        return Response({
            "code": 200,
            "message": "文章修改成功"
        })


class ArticleDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        article_id = request.data.get('id')
        if not article_id:
            return Response({
                "code": 400,
                "message": "缺少文章id"
            }, status=400)

        try:
            article = Article.objects.get(id=article_id)
            article.delete()
            return Response({
                "code": 200,
                "message": "文章删除成功"
            })
        except Article.DoesNotExist:
            return Response({
                "code": 404,
                "message": "文章不存在"
            }, status=404)
```

---

### 4. `lyhblog-backend/blog/views/comment.py`

这里主要是确保后台评论列表和删除接口能用。

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Comment, Article
from ..serializers import CommentSerializer


class CommentListView(APIView):
    def get(self, request):
        article_id = request.GET.get('article_id')
        if not article_id:
            return Response({
                "code": 400,
                "message": "缺少文章id"
            }, status=400)

        comments = Comment.objects.filter(article_id=article_id).order_by('-create_time')
        serializer = CommentSerializer(comments, many=True)

        return Response({
            "code": 200,
            "message": "获取评论列表成功",
            "data": serializer.data
        })


class CommentAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        article_id = request.data.get('article_id')
        content = request.data.get('content')

        if not article_id or not content:
            return Response({
                "code": 400,
                "message": "参数不完整"
            }, status=400)

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({
                "code": 404,
                "message": "文章不存在"
            }, status=404)

        comment = Comment.objects.create(
            article=article,
            user=request.user,
            content=content
        )

        return Response({
            "code": 200,
            "message": "评论发表成功",
            "data": CommentSerializer(comment).data
        })


class CommentAllView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        comments = Comment.objects.all().order_by('-create_time')
        serializer = CommentSerializer(comments, many=True)
        return Response({
            "code": 200,
            "data": serializer.data
        })


class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        comment_id = request.data.get('id')

        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return Response({
                "code": 200,
                "message": "评论删除成功"
            })
        except Comment.DoesNotExist:
            return Response({
                "code": 404,
                "message": "评论不存在"
            }, status=404)
```

---

## 四、你照着改的时候顺序别乱

推荐顺序：

1. 先改后端 `serializers.py`
2. 再改后端 `urls.py`
3. 再改后端 `article.py`
4. 再改后端 `comment.py`
5. 再改前端 `api/article.js`
6. 再改前端 `api/comment.js`
7. 再改前端 `ArticleEdit.vue`
8. 再改前端 `CommentList.vue`

---

## 五、改完后的验收

### 1. ArticleEdit

- 打开 `/admin/article/add`
- 分类能显示
- 标签能显示
- 新增文章成功
- 打开 `/admin/article/edit/1`
- 能看到旧数据
- 修改后能保存

### 2. CommentList

- 打开 `/admin/comment`
- 评论列表能出来
- 点删除能成功
- 删除后列表刷新

---

## 六、你接下来怎么用这份文档

最好的用法不是一次性全抄，而是：

1. 先照着写 `api/article.js`
2. 再写 `ArticleEdit.vue`
3. 跑通后再写评论管理

这样你更容易知道每一段代码为什么要这么写。
