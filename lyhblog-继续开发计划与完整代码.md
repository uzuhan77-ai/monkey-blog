# lyhblog 继续开发计划与完整代码

## 说明

这份文档不是部署文档，而是继续开发文档。  
适合你现在这种状态：

1. 博客核心功能已经有雏形
2. 前台分类和标签筛选已经完成
3. 后台文章、评论、分类、标签管理也已经基本打通
4. 现在要继续把项目做完整，最后再上线

这份文档分为两部分：

1. 你当前项目还缺什么
2. 下一步最适合继续写的功能和完整代码

---

## 一、你当前项目做到哪里了

按现在代码状态看，你已经完成了这些：

### 已完成

1. 用户登录
2. 用户注册
3. 前台文章列表
4. 前台文章详情
5. 前台评论列表与发表评论
6. 前台按分类筛选
7. 前台按标签筛选
8. 后台文章列表
9. 后台文章新增/编辑/删除
10. 后台评论管理
11. 后台分类管理
12. 后台标签管理
13. 管理员权限拦截

### 现在还缺的，才是项目继续往下做的重点

1. 首页筛选状态修复与关键词搜索收尾
2. 页面体验完善
3. README 项目说明
4. 环境变量改造
5. Ubuntu / 阿里云部署
6. 图片上传
7. Markdown 编辑器
8. Redis 缓存
9. Docker 部署

---

## 二、建议你接下来的开发顺序

不要乱跳，建议按这个顺序做。

### 计划 1：先补“用户能直接感知”的功能

1. 首页筛选状态修复与关键词搜索收尾
2. 文章摘要显示优化
3. 列表空状态和加载状态优化
4. 后台分页优化

### 计划 2：再补“项目完整度”

1. README
2. 环境变量
3. 上线配置
4. 项目截图

### 计划 3：最后补“简历加分项”

1. Markdown 编辑器
2. 图片上传
3. Redis 热门文章缓存
4. Docker Compose

---

## 三、为什么下一步建议你先做“首页筛选状态修复 + 关键词搜索收尾”

原因有 4 个：

1. 它和你现在已经完成的“分类 / 标签筛选”是同一条线
2. 改动范围小，前后端都好理解
3. 很适合放到项目介绍里讲
4. 做完以后首页功能就更完整了

所以这份文档下面给你的完整代码，就是：

**首页筛选状态修复 + 关键词搜索**

功能目标：

1. 首页新增搜索框
2. 支持按关键词搜索文章
3. 搜索和分类/标签筛选可以组合使用
4. 点击“全部文章”时，分类、标签、关键词一起重置
5. 修复“点完分类再点全部文章时，高亮像跳到全部标签”的显示问题

---

## 四、实现计划

### 计划 1：后端支持 keyword 参数

在文章列表接口中接收 `keyword`，对：

1. `title`
2. `summary`
3. `content`

做模糊匹配。

### 计划 2：前端首页加搜索框

在首页筛选区域增加：

1. 输入框
2. 搜索按钮
3. 回车搜索

### 计划 3：把搜索和现有筛选组合起来

请求文章列表时同时带上：

1. 分类 id
2. 标签 id
3. keyword

### 计划 4：重置逻辑

点“全部文章”时同时清空：

1. 分类
2. 标签
3. 搜索关键词

### 计划 5：修复筛选高亮冲突

你现在这个 bug 的根本原因是：

1. “全部文章”
2. “全部分类”
3. “全部标签”

这三个按钮都在用 `null` 作为高亮判断条件。  
当分类和标签都被清空时，这 3 个按钮会同时满足高亮条件，所以看起来像状态乱跳。

解决方式：

1. 单独增加 `categoryTouched`
2. 单独增加 `tagTouched`
3. 用 `isAllMode` 控制“全部文章”
4. 用 `categoryTouched` 控制“全部分类”
5. 用 `tagTouched` 控制“全部标签”

---

## 五、需要改动的文件

1. `lyhblog-backend/blog/views/article.py`
2. `lyhblog-frontend/src/views/Home.vue`

---

## 六、后端完整代码

文件：`lyhblog-backend/blog/views/article.py`

你要做两件事：

1. 增加 `Q` 的导入
2. 修改文章列表接口

### 第一步：在顶部 import 增加这一行

```python
from django.db.models import Q
```

### 第二步：把 `ArticleListView` 改成下面这版

```python
class ArticleListView(APIView):
    def post(self, request):
        current = int(request.data.get('current', 1))
        size = int(request.data.get('size', 10))
        category_id = request.data.get('category_id')
        tag_id = request.data.get('tag_id')
        keyword = (request.data.get('keyword') or '').strip()

        queryset = Article.objects.all()

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) |
                Q(summary__icontains=keyword) |
                Q(content__icontains=keyword)
            )

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
            "message": "成功获取文章列表",
        })
```

---

## 七、前端完整代码

文件：`lyhblog-frontend/src/views/Home.vue`

下面给的是完整可参考版本。  
你可以直接对照着改。

```vue
<template>
  <div class="home-page">
    <h1>文章列表</h1>

    <div class="filter-panel">
      <div class="filter-row">
        <span class="filter-title">搜索:</span>
        <el-input
          v-model="keyword"
          class="search-input"
          clearable
          placeholder="输入标题或内容关键词"
          @keyup.enter="handleSearch"
        />
        <el-button type="primary" @click="handleSearch">
          搜索
        </el-button>
      </div>

      <div class="filter-row">
        <span class="filter-title">快速筛选:</span>
        <el-button
          :type="isAllMode ? 'primary' : 'default'"
          size="small"
          @click="handleAllClick"
        >
          全部文章
        </el-button>
      </div>

      <div class="filter-row">
        <span class="filter-title">分类:</span>

        <el-button
          :type="categoryTouched && activeCategoryId === null ? 'primary' : 'default'"
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
        <span class="filter-title">标签:</span>
        <el-button
          :type="tagTouched && activeTagId === null ? 'primary' : 'default'"
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
            <span v-else>
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
              阅读全文 ➔
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
import { ref, onMounted, computed } from 'vue'
import { ApiArticleList } from '../api/article'
import { ApiCategoryList } from '../api/category'
import { ApiTagList } from '../api/tag'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const router = useRouter()

const articleList = ref([])
const current = ref(1)
const size = ref(6)
const total = ref(0)

const categoryList = ref([])
const tagList = ref([])
const activeCategoryId = ref(null)
const activeTagId = ref(null)
const keyword = ref('')
const categoryTouched = ref(false)
const tagTouched = ref(false)

const isAllMode = computed(() => {
  return (
    activeCategoryId.value === null &&
    activeTagId.value === null &&
    keyword.value.trim() === '' &&
    !categoryTouched.value &&
    !tagTouched.value
  )
})

const getArticleList = async () => {
  loading.value = true
  try {
    const res = await ApiArticleList({
      current: current.value,
      size: size.value,
      category_id: activeCategoryId.value,
      tag_id: activeTagId.value,
      keyword: keyword.value.trim()
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

const getCategoryList = async () => {
  try {
    const res = await ApiCategoryList()
    if (res.data.code == 200) {
      categoryList.value = res.data.data
    }
  } catch (error) {
    console.error(error)
  }
}

const getTagList = async () => {
  try {
    const res = await ApiTagList()
    if (res.data.code == 200) {
      tagList.value = res.data.data
    }
  } catch (error) {
    ElMessage.error('标签列表加载失败')
  }
}

const handleAllClick = () => {
  activeCategoryId.value = null
  activeTagId.value = null
  categoryTouched.value = false
  tagTouched.value = false
  keyword.value = ''
  current.value = 1
  getArticleList()
}

const handleCategoryClick = (categoryId) => {
  categoryTouched.value = true
  activeCategoryId.value = categoryId
  current.value = 1
  getArticleList()
}

const handleTagClick = (tagId) => {
  tagTouched.value = true
  activeTagId.value = tagId
  current.value = 1
  getArticleList()
}

const handleSearch = () => {
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

.search-input {
  width: 280px;
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

## 八、改完后怎么自测

你写完以后，按下面顺序测：

### 基础测试

1. 不输入关键词，文章列表正常显示
2. 输入关键词后，能搜出相关文章
3. 输入不存在的关键词，显示空状态

### 组合筛选测试

1. 分类 + 关键词
2. 标签 + 关键词
3. 分类 + 标签 + 关键词

### 重置测试

1. 点“全部文章”
2. 分类清空
3. 标签清空
4. 搜索关键词清空
5. 只让“全部文章”高亮

### 当前 bug 专项测试

1. 先点某个分类，比如“爱情”
2. 再点“全部文章”
3. 不应该再出现“全部标签”像被自动选中的错觉
4. “全部分类”和“全部标签”不应和“全部文章”同时高亮

### 构建测试

前端：

```bash
cd lyhblog-frontend
npm run dev
```

再执行：

```bash
npm.cmd run build
```

后端：

```bash
cd lyhblog-backend
venv\Scripts\python.exe manage.py check
```

---

## 九、这个功能做完后，下一步做什么

我建议你继续按下面顺序写：

### 下一步计划 A：前台完善

1. 首页筛选状态修复与搜索收尾
2. 文章摘要显示优化
3. 详情页样式完善

### 下一步计划 B：后台体验完善

1. 评论分页
2. 文章列表删除和提示优化
3. 后台加载状态优化

### 下一步计划 C：上线准备

1. 环境变量
2. README
3. Ubuntu 部署
4. 阿里云部署

### 下一步计划 D：简历加分项

1. Markdown 编辑器
2. 图片上传
3. Redis 缓存
4. Docker Compose

---

## 十、你现在最该做什么

最适合你的顺序是：

1. 先把这份文档里的“首页筛选状态修复 + 搜索收尾”写完
2. 写完以后本地跑通
3. 下一步接“后台评论分页”
4. 再开始做环境变量改造
5. 再去 Ubuntu 部署
6. 最后迁阿里云

## 结论

你不是只剩部署了。  
你现在是“功能已经过半，接下来要边补功能边做上线准备”的阶段。

所以接下来最合理的节奏不是只看部署，而是：

1. 继续做一个个完整功能
2. 每做完一个就测试
3. 功能差不多后再统一部署

这才是最稳的做法。
