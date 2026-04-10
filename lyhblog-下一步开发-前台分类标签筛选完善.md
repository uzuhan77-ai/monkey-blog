# lyhblog 下一步开发：前台分类/标签筛选完善

> 这一轮的目标：
>
> 1. 文章详情页展示分类和标签
> 2. 首页不仅能按分类筛选，还能按标签筛选
> 3. 后端文章列表接口支持 `tag_id`

---

## 一、为什么下一步做这个

你现在已经做完：

- 后台文章管理
- 后台分类管理
- 后台标签管理
- 文章编辑页绑定分类和标签

下一步就应该让这些数据在前台真正发挥作用。

也就是说：

- 后台维护分类/标签
- 写文章时选择分类/标签
- 前台首页按分类/标签筛文章
- 详情页展示文章所属分类/标签

这一步做完，你的博客就更像一个完整博客系统了。

---

## 二、这一轮要改哪些文件

### 后端

- `lyhblog-backend/blog/views/article.py`

### 前端

- `lyhblog-frontend/src/views/Home.vue`
- `lyhblog-frontend/src/views/ArticleDetail.vue`

这一轮不需要新增模型，也不需要新增数据库迁移。

---

## 三、第 1 步：后端文章列表支持标签筛选

### 当前问题

你现在的文章列表接口只支持分类筛选：

```python
category_id = request.data.get('category_id')
```

现在要加上标签筛选：

```python
tag_id = request.data.get('tag_id')
```

---

## 四、后端完整代码：`lyhblog-backend/blog/views/article.py`

> 如果你只想最小改动，也可以只改 `ArticleListView`。
> 下面给的是完整 `article.py`，方便你对照。

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Article
from ..serializers import ArticleSerializer


class ArticleListView(APIView):
    def post(self, request):
        current = int(request.data.get('current', 1))
        size = int(request.data.get('size', 10))
        category_id = request.data.get('category_id')
        tag_id = request.data.get('tag_id')

        queryset = Article.objects.all()

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)

        queryset = queryset.distinct()

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
                "message": "缺少文章 ID 参数"
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
                "message": "缺少文章 id"
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
                "message": "缺少文章 id"
            }, status=400)

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({
                "code": 404,
                "message": "文章不存在"
            }, status=404)

        article.delete()

        return Response({
            "code": 200,
            "message": "文章删除成功"
        })
```

---

## 五、后端这一步怎么验收

你可以先用前端页面验收，也可以用接口工具验收。

### 按分类筛选

请求：

```json
{
  "current": 1,
  "size": 6,
  "category_id": 1,
  "tag_id": null
}
```

### 按标签筛选

请求：

```json
{
  "current": 1,
  "size": 6,
  "category_id": null,
  "tag_id": 2
}
```

### 全部文章

请求：

```json
{
  "current": 1,
  "size": 6,
  "category_id": null,
  "tag_id": null
}
```

---

## 六、第 2 步：首页加标签筛选

### 当前首页已有能力

你的首页现在已经有：

- 文章列表
- 分页
- 分类筛选
- 文章卡片展示标签

现在要补：

- 加载标签列表
- 点击标签筛选文章
- 点击“全部文章”恢复全部文章

---

## 七、前端完整代码：`lyhblog-frontend/src/views/Home.vue`

```vue
<template>
  <div class="home-page">
    <h1>文章列表</h1>

    <div class="filter-panel">
      <div class="filter-row">
        <span class="filter-title">快速筛选：</span>
        <el-button
          :type="activeCategoryId === null && activeTagId === null ? 'primary' : 'default'"
          size="small"
          @click="handleAllClick"
        >
          全部文章
        </el-button>
      </div>

      <div class="filter-row">
        <span class="filter-title">分类：</span>
        <el-button
          :type="activeCategoryId === null ? 'primary' : 'default'"
          size="small"
          @click="handleCategoryClick(null)"
        >
          全部分类
        </el-button>

        <el-button
          v-for="cat in categoryList"
          :key="cat.id"
          :type="activeCategoryId === cat.id ? 'primary' : 'default'"
          size="small"
          @click="handleCategoryClick(cat.id)"
        >
          {{ cat.name }}
        </el-button>
      </div>

      <div class="filter-row">
        <span class="filter-title">标签：</span>
        <el-button
          :type="activeTagId === null ? 'primary' : 'default'"
          size="small"
          @click="handleTagClick(null)"
        >
          全部标签
        </el-button>

        <el-button
          v-for="tag in tagList"
          :key="tag.id"
          :type="activeTagId === tag.id ? 'primary' : 'default'"
          size="small"
          @click="handleTagClick(tag.id)"
        >
          {{ tag.name }}
        </el-button>
      </div>
    </div>

    <el-skeleton v-if="loading" :rows="5" animated />

    <el-empty v-else-if="articleList.length === 0" description="暂无文章" />

    <el-row v-else :gutter="20">
      <el-col
        v-for="item in articleList"
        :key="item.id"
        :xs="24"
        :sm="12"
        :md="8"
        style="margin-bottom: 20px"
      >
        <el-card class="article-card" shadow="hover" @click="goToDetail(item.id)">
          <h3 class="article-title">
            {{ item.title }}
          </h3>

          <p class="article-summary">
            {{ item.summary || item.content?.substring(0, 50) || '暂无内容' }}
          </p>

          <div class="article-meta">
            <span v-if="item.category" class="category-name">
              {{ item.category.name }}
            </span>
            <span v-else class="empty-text">
              未分类
            </span>

            <span v-if="item.tags && item.tags.length > 0" class="tag-list">
              <span v-for="tag in item.tags" :key="tag.id" class="tag">
                {{ tag.name }}
              </span>
            </span>
          </div>

          <div class="article-footer">
            <span>{{ item.create_time }}</span>
            <el-button type="primary" text size="small">
              阅读全文
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <div class="pagination-box">
      <el-pagination
        background
        layout="total, prev, pager, next"
        :total="total"
        :page-size="size"
        v-model:current-page="current"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ApiArticleList } from '../api/article'
import { ApiCategoryList } from '../api/category'
import { ApiTagList } from '../api/tag'

const router = useRouter()

const loading = ref(false)
const articleList = ref([])
const current = ref(1)
const size = ref(6)
const total = ref(0)

const categoryList = ref([])
const tagList = ref([])
const activeCategoryId = ref(null)
const activeTagId = ref(null)

const getArticleList = async () => {
  loading.value = true

  try {
    const res = await ApiArticleList({
      current: current.value,
      size: size.value,
      category_id: activeCategoryId.value,
      tag_id: activeTagId.value
    })

    if (res.data.code === 200) {
      articleList.value = res.data.data
      total.value = res.data.total
    }
  } catch (error) {
    ElMessage.error('文章列表加载失败')
  } finally {
    loading.value = false
  }
}

const getCategoryList = async () => {
  try {
    const res = await ApiCategoryList()
    if (res.data.code === 200) {
      categoryList.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('分类列表加载失败')
  }
}

const getTagList = async () => {
  try {
    const res = await ApiTagList()
    if (res.data.code === 200) {
      tagList.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('标签列表加载失败')
  }
}

const handleAllClick = () => {
  activeCategoryId.value = null
  activeTagId.value = null
  current.value = 1
  getArticleList()
}

const handleCategoryClick = (categoryId) => {
  activeCategoryId.value = categoryId
  current.value = 1
  getArticleList()
}

const handleTagClick = (tagId) => {
  activeTagId.value = tagId
  current.value = 1
  getArticleList()
}

const handlePageChange = (newPage) => {
  current.value = newPage
  getArticleList()
}

const goToDetail = (id) => {
  router.push({
    path: '/article',
    query: { id }
  })
}

onMounted(() => {
  getArticleList()
  getCategoryList()
  getTagList()
})
</script>

<style scoped>
.home-page {
  padding: 20px;
}

.filter-panel {
  background: #fff;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.filter-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 12px;
}

.filter-row:last-child {
  margin-bottom: 0;
}

.filter-title {
  min-width: 80px;
  font-weight: bold;
  color: #303133;
}

.article-card {
  cursor: pointer;
  transition: all 0.3s;
  height: 100%;
}

.article-card:hover {
  transform: translateY(-5px);
}

.article-title {
  margin: 0 0 10px 0;
  font-size: 18px;
}

.article-summary {
  color: #606266;
  font-size: 14px;
  min-height: 42px;
}

.article-meta {
  margin-top: 10px;
}

.category-name {
  color: #409eff;
  font-weight: bold;
}

.empty-text {
  color: #999;
}

.tag-list {
  margin-left: 10px;
}

.tag {
  margin-left: 5px;
  background: #ecf5ff;
  color: #409eff;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.article-footer {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #999;
  font-size: 12px;
}

.pagination-box {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>
```

---

## 八、首页筛选逻辑说明

这几个状态很关键：

```javascript
const activeCategoryId = ref(null)
const activeTagId = ref(null)
```

它们分别表示：

- 当前选中的分类 id
- 当前选中的标签 id

请求文章列表时一起传给后端：

```javascript
category_id: activeCategoryId.value,
tag_id: activeTagId.value
```

后端会根据这两个参数筛选文章。

如果都是 `null`，就是全部文章。

---

## 九、第 3 步：文章详情页展示分类和标签

### 当前问题

你的文章详情页目前只显示：

- 标题
- 时间
- 正文
- 评论

现在要加：

- 分类
- 标签
- 摘要

---

## 十、前端完整代码：`lyhblog-frontend/src/views/ArticleDetail.vue`

```vue
<template>
  <div class="detail-page">
    <div class="article-detail">
      <h1>{{ article.title }}</h1>

      <div class="meta">
        <span>{{ article.create_time }}</span>

        <span v-if="article.category" class="category">
          {{ article.category.name }}
        </span>

        <span v-else class="empty-text">
          未分类
        </span>
      </div>

      <div v-if="article.tags && article.tags.length > 0" class="tags">
        <span v-for="tag in article.tags" :key="tag.id" class="tag">
          {{ tag.name }}
        </span>
      </div>

      <p v-if="article.summary" class="summary">
        {{ article.summary }}
      </p>

      <div class="content">
        {{ article.content }}
      </div>
    </div>

    <CommentSection v-if="article.id" :article-id="article.id" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ApiArticleDetail } from '../api/article'
import CommentSection from '../components/CommentSection.vue'

const route = useRoute()
const article = ref({})

const getArticle = async () => {
  const id = route.query.id

  if (!id) {
    ElMessage.error('缺少文章 id')
    return
  }

  try {
    const res = await ApiArticleDetail(id)
    if (res.data.code === 200) {
      article.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('文章详情加载失败')
  }
}

onMounted(() => {
  getArticle()
})
</script>

<style scoped>
.detail-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px;
}

.article-detail {
  background: #fff;
  padding: 24px;
  border-radius: 10px;
  margin-bottom: 24px;
}

.meta {
  display: flex;
  gap: 12px;
  align-items: center;
  color: #909399;
  font-size: 14px;
  margin-bottom: 12px;
}

.category {
  color: #409eff;
  font-weight: bold;
}

.empty-text {
  color: #999;
}

.tags {
  margin-bottom: 16px;
}

.tag {
  display: inline-block;
  margin-right: 8px;
  background: #ecf5ff;
  color: #409eff;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.summary {
  padding: 12px;
  background: #f5f7fa;
  color: #606266;
  border-left: 4px solid #409eff;
  margin-bottom: 20px;
}

.content {
  white-space: pre-wrap;
  line-height: 1.8;
  color: #303133;
}
</style>
```

---

## 十一、这一轮怎么验收

### 1. 后端接口

先确认文章列表接口支持：

- 不传 `category_id` 和 `tag_id`
- 只传 `category_id`
- 只传 `tag_id`
- 同时传 `category_id` 和 `tag_id`

### 2. 首页分类筛选

- 打开首页
- 点击某个分类
- 文章列表发生变化
- 分页仍正常

### 3. 首页标签筛选

- 点击某个标签
- 文章列表发生变化
- 分页仍正常

### 4. 全部文章

- 点击“全部文章”
- 分类和标签筛选都清空
- 文章恢复全部列表

### 5. 详情页

- 点击文章进入详情页
- 能看到分类
- 能看到标签
- 有摘要时能看到摘要
- 评论区仍正常显示

---

## 十二、容易踩的坑

### 1. 后端标签筛选字段不是 `tag_id`

前端传的是：

```javascript
tag_id
```

后端也要取：

```python
tag_id = request.data.get('tag_id')
```

不要写成 `tags` 或 `tagId`。

### 2. 多对多筛选写法

标签是多对多字段，筛选时要写：

```python
queryset = queryset.filter(tags__id=tag_id)
```

不是：

```python
queryset = queryset.filter(tag_id=tag_id)
```

### 3. 首页要加载标签列表

别忘了在 `onMounted` 里调用：

```javascript
getTagList()
```

### 4. 详情页要判断标签是否存在

安全写法是：

```vue
<div v-if="article.tags && article.tags.length > 0">
```

不要直接默认 `article.tags.length` 一定存在。

---

## 十三、推荐动手顺序

不要一口气改完所有文件。

按这个顺序最稳：

1. 先改后端 `ArticleListView`
2. 重启后端
3. 打开首页确认原来的文章列表还能加载
4. 再改 `Home.vue` 加标签列表和标签筛选
5. 测试分类筛选
6. 测试标签筛选
7. 最后改 `ArticleDetail.vue` 展示分类和标签

---

## 十四、这一轮做完以后，下一步做什么

这一步做完以后，博客核心链路基本是：

- 后台写文章
- 后台管理分类/标签
- 前台按分类/标签浏览文章
- 前台看文章详情和评论

下一步建议做：

1. 富文本或 Markdown 编辑器
2. 后台首页统计概览
3. 前台页面样式统一优化

最推荐先做：

```text
Markdown 编辑器
```

因为现在文章正文只是普通 textarea，写长文章体验会比较差。
