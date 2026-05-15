# Fuwari 风格主页改造学习文档

本文档只讲如何把当前 Vue + Django 博客主页改成接近 `https://chr0mium.link/` / Fuwari 的视觉风格。先从主页开始，不改后端，不换 Astro，不直接复制 Fuwari 源码。

## 1. 改造目标

当前项目结构：

```text
D:\Monkey-blog
  lyhblog-frontend
    src
      views
        Home.vue
      components
        FrontHeader.vue
      api
        article.js
        category.js
        tag.js
  lyhblog-backend
```

主页第一版目标：

```text
顶部：FrontHeader

主体：两栏布局
  左侧 sidebar
    个人信息卡
    分类卡
    标签卡

  右侧 content
    最新文章标题区
    搜索框
    文章卡片列表
    分页
```

为了避免把当前能跑的首页改坏，第一版不要直接改 `Home.vue`。先新增一个演示页面：

```text
lyhblog-frontend/src/views/HomeFuwariDemo.vue
```

再加一个临时路由：

```text
/home-fuwari
```

这样你可以访问新页面看效果，原来的 `/` 首页不受影响。

确认效果满意后，再决定：

```text
方案 A：把 / 的路由指向 HomeFuwariDemo.vue
方案 B：把 HomeFuwariDemo.vue 的内容复制回 Home.vue
```

先不要拆组件。等你写顺后，再拆：

```text
ProfileCard.vue
PostCard.vue
BlogLayout.vue
```

## 2. 后端数据字段

你的文章列表接口是：

```js
ApiArticleList(data)
```

实际请求：

```text
POST /article/listArticle/
```

返回结构：

```js
{
  code: 200,
  data: [
    {
      id,
      title,
      summary,
      content,
      create_time,
      category,
      tags
    }
  ],
  total,
  message
}
```

可用字段：

```js
item.id
item.title
item.summary
item.content
item.create_time
item.category?.name
item.tags
```

注意：你的项目没有 `published` 字段，也没有 `publish_time` 字段。主页和归档页都应该用：

```js
item.create_time
```

## 3. 新建演示页面

先新建文件：

```text
lyhblog-frontend/src/views/HomeFuwariDemo.vue
```

后面的 template、script、style 都先写在这个文件里。

## 4. HomeFuwariDemo.vue 模板

把 `HomeFuwariDemo.vue` 的 `<template>` 写成下面这个结构。

```vue
<template>
  <div class="home-page">
    <FrontHeader />

    <main class="home-shell">
      <aside class="sidebar">
        <section class="profile-card glass-card">
          <div class="avatar">LYH</div>
          <h1>lyhblog</h1>
          <p>Django + Vue 搭建的个人博客，记录学习、项目和工程实践。</p>

          <div class="stats">
            <div>
              <strong>{{ postTotal }}</strong>
              <span>文章</span>
            </div>
            <div>
              <strong>{{ categoryList.length }}</strong>
              <span>分类</span>
            </div>
            <div>
              <strong>{{ tagList.length }}</strong>
              <span>标签</span>
            </div>
          </div>
        </section>

        <section class="glass-card widget-card">
          <h2>分类</h2>
          <button
            class="chip"
            :class="{ active: activeCategoryId === null }"
            @click="handleAllClick"
          >
            全部
          </button>
          <button
            v-for="cat in categoryList"
            :key="cat.id"
            class="chip"
            :class="{ active: activeCategoryId === cat.id }"
            @click="handleCategoryClick(cat.id)"
          >
            {{ cat.name }}
          </button>
        </section>

        <section class="glass-card widget-card">
          <h2>标签</h2>
          <button
            v-for="tag in tagList"
            :key="tag.id"
            class="chip"
            :class="{ active: activeTagId === tag.id }"
            @click="handleTagClick(tag.id)"
          >
            #{{ tag.name }}
          </button>
        </section>
      </aside>

      <section class="content">
        <div class="content-head">
          <div>
            <p class="eyebrow">RECENT POSTS</p>
            <h2>最新文章</h2>
          </div>

          <div class="search-box">
            <el-input
              v-model="keyword"
              clearable
              placeholder="搜索文章"
              @keyup.enter="handleSearch"
            />
            <el-button type="primary" @click="handleSearch">搜索</el-button>
          </div>
        </div>

        <el-skeleton v-if="loading" :rows="6" animated />

        <el-empty v-else-if="articleList.length === 0" description="暂无文章" />

        <div v-else class="post-list">
          <article
            v-for="item in articleList"
            :key="item.id"
            class="post-card glass-card"
            @click="goToDetail(item.id)"
          >
            <div class="post-meta">
              <span>{{ item.create_time }}</span>
              <span>{{ item.category?.name || '未分类' }}</span>
            </div>

            <h3>{{ item.title }}</h3>
            <p>{{ getArticleSummary(item) }}</p>

            <div class="post-footer">
              <div class="post-tags">
                <span v-for="tag in item.tags || []" :key="tag.id">
                  #{{ tag.name }}
                </span>
              </div>
              <span class="read-more">阅读</span>
            </div>
          </article>
        </div>

        <div class="pagination-box">
          <el-pagination
            background
            layout="total, prev, pager, next"
            :total="total"
            :page-size="size"
            :current-page="current"
            @current-change="handlePageChange"
          />
        </div>
      </section>
    </main>
  </div>
</template>
```

### 模板要点

`glass-card` 是通用玻璃卡片样式，后面 CSS 会定义。

`sidebar` 是左侧固定信息栏。

`content` 是右侧文章主区域。

`postTotal` 用于显示总文章数，避免你筛选分类后左侧总数跟着变小。

`item.category?.name` 使用了可选链，文章没有分类时不会报错。

## 5. HomeFuwariDemo.vue 脚本

把 `HomeFuwariDemo.vue` 的 `<script setup>` 写成下面这个版本。

```vue
<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ApiArticleList } from '../api/article'
import { ApiCategoryList } from '../api/category'
import { ApiTagList } from '../api/tag'
import FrontHeader from '../components/FrontHeader.vue'

const router = useRouter()

const loading = ref(false)
const articleList = ref([])
const current = ref(1)
const size = ref(6)
const total = ref(0)
const dashboardTotal = ref(0)

const categoryList = ref([])
const tagList = ref([])
const activeCategoryId = ref(null)
const activeTagId = ref(null)
const keyword = ref('')

const postTotal = computed(() => dashboardTotal.value || total.value)

const stripHtml = (text = '') => {
  return String(text).replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim()
}

const getArticleSummary = (item) => {
  return stripHtml(item.summary || item.content || '').slice(0, 96) || '暂无摘要'
}

const getArticleList = async () => {
  loading.value = true
  try {
    const res = await ApiArticleList({
      current: current.value,
      size: size.value,
      category_id: activeCategoryId.value,
      tag_id: activeTagId.value,
      keyword: keyword.value.trim(),
    })

    if (res.data.code === 200) {
      articleList.value = res.data.data || []
      total.value = Number(res.data.total || 0)
    }

    if (!activeCategoryId.value && !activeTagId.value && !keyword.value.trim()) {
      dashboardTotal.value = Number(res.data.total || 0)
    }
  } catch (error) {
    ElMessage.error('文章加载失败')
  } finally {
    loading.value = false
  }
}

const getCategoryList = async () => {
  try {
    const res = await ApiCategoryList()
    if (res.data.code === 200) {
      categoryList.value = res.data.data || []
    }
  } catch (error) {
    ElMessage.error('分类列表加载失败')
  }
}

const getTagList = async () => {
  try {
    const res = await ApiTagList()
    if (res.data.code === 200) {
      tagList.value = res.data.data || []
    }
  } catch (error) {
    ElMessage.error('标签列表加载失败')
  }
}

const handleAllClick = () => {
  activeCategoryId.value = null
  activeTagId.value = null
  keyword.value = ''
  current.value = 1
  getArticleList()
}

const handleCategoryClick = (categoryId) => {
  activeCategoryId.value = categoryId
  activeTagId.value = null
  current.value = 1
  getArticleList()
}

const handleTagClick = (tagId) => {
  activeTagId.value = tagId
  activeCategoryId.value = null
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
    query: { id },
  })
}

onMounted(() => {
  getArticleList()
  getCategoryList()
  getTagList()
})
</script>
```

### 脚本要点

`ref` 用于保存可变状态。

```js
const articleList = ref([])
```

在模板里可以直接写：

```vue
articleList.length
```

在 JS 里要写：

```js
articleList.value
```

`computed` 用于计算派生状态。

```js
const postTotal = computed(() => dashboardTotal.value || total.value)
```

这个值不用手动更新，只要 `dashboardTotal` 或 `total` 变了，它会自动变。

`stripHtml` 是为了避免摘要里出现 HTML 标签。

```js
String(text).replace(/<[^>]+>/g, ' ')
```

`handleCategoryClick` 和 `handleTagClick` 互相清空，是为了第一版筛选逻辑简单：

```js
activeCategoryId.value = categoryId
activeTagId.value = null
```

## 6. HomeFuwariDemo.vue 样式

把下面样式放到 `HomeFuwariDemo.vue` 底部：

```vue
<style scoped>
.home-page {
  min-height: 100vh;
  background:
    radial-gradient(circle at 12% 8%, rgba(126, 146, 120, 0.22), transparent 24rem),
    radial-gradient(circle at 88% 12%, rgba(59, 84, 111, 0.14), transparent 22rem),
    linear-gradient(180deg, #f6f3ed 0%, #ece7dd 100%);
  color: #1f211d;
}

.home-shell {
  width: min(1180px, calc(100% - 48px));
  margin: 0 auto;
  padding: 36px 0 64px;
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr);
  gap: 20px;
}

.glass-card {
  border: 1px solid rgba(31, 31, 27, 0.08);
  background: rgba(255, 255, 255, 0.74);
  box-shadow: 0 20px 60px rgba(31, 31, 27, 0.06);
  backdrop-filter: blur(16px);
  border-radius: 24px;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.profile-card {
  position: sticky;
  top: 96px;
  padding: 24px;
}

.avatar {
  width: 72px;
  height: 72px;
  border-radius: 20px;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #1f4d3b, #9bb089);
  color: #fff;
  font-weight: 800;
  letter-spacing: 0.08em;
}

.profile-card h1 {
  margin: 18px 0 0;
  font-size: 24px;
  color: #1d241f;
}

.profile-card p {
  margin: 10px 0 0;
  color: #62675f;
  line-height: 1.8;
}

.stats {
  margin-top: 22px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.stats div {
  padding: 12px 8px;
  border-radius: 16px;
  background: rgba(111, 127, 106, 0.1);
  text-align: center;
}

.stats strong {
  display: block;
  font-size: 22px;
  color: #1f4d3b;
}

.stats span {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: #6c746c;
}

.widget-card {
  padding: 20px;
}

.widget-card h2 {
  margin: 0 0 14px;
  font-size: 18px;
  color: #1d241f;
}

.chip {
  margin: 0 8px 8px 0;
  padding: 7px 12px;
  border: 0;
  border-radius: 999px;
  background: rgba(111, 127, 106, 0.1);
  color: #526157;
  cursor: pointer;
  transition: all 0.2s ease;
}

.chip:hover,
.chip.active {
  background: #1f4d3b;
  color: #fff;
}

.content {
  min-width: 0;
}

.content-head {
  margin-bottom: 18px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
}

.eyebrow {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.16em;
  color: #7a7366;
}

.content-head h2 {
  margin: 8px 0 0;
  font-size: 36px;
  color: #1d241f;
}

.search-box {
  width: min(380px, 100%);
  display: flex;
  gap: 10px;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.post-card {
  padding: 24px;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.post-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 24px 70px rgba(31, 31, 27, 0.1);
}

.post-meta,
.post-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.post-meta {
  color: #777d73;
  font-size: 13px;
}

.post-card h3 {
  margin: 14px 0 10px;
  font-size: 24px;
  line-height: 1.4;
  color: #1d241f;
}

.post-card p {
  margin: 0;
  color: #62675f;
  line-height: 1.8;
}

.post-footer {
  margin-top: 18px;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  color: rgba(31, 77, 59, 0.68);
  font-size: 13px;
}

.read-more {
  color: #1f4d3b;
  font-weight: 700;
}

.pagination-box {
  margin-top: 26px;
  display: flex;
  justify-content: center;
}

@media (max-width: 900px) {
  .home-shell {
    grid-template-columns: 1fr;
  }

  .profile-card {
    position: static;
  }
}

@media (max-width: 720px) {
  .home-shell {
    width: min(100% - 32px, 1180px);
    padding-top: 24px;
  }

  .content-head {
    align-items: flex-start;
    flex-direction: column;
  }

  .search-box {
    flex-direction: column;
  }
}
</style>
```

## 7. 添加临时路由

改这个文件：

```text
lyhblog-frontend/src/router/index.js
```

在 `routes` 数组里加一项：

```js
{
  path: '/home-fuwari',
  name: 'HomeFuwariDemo',
  component: () => import('../views/HomeFuwariDemo.vue')
}
```

加完以后，启动前端：

```cmd
cd /d D:\Monkey-blog\lyhblog-frontend
npm run dev
```

然后访问：

```text
http://localhost:5173/home-fuwari
```

如果你电脑上的端口不是 `5173`，就看终端里 Vite 打印的地址。

原首页仍然是：

```text
http://localhost:5173/
```

这样两个页面可以对照。

## 8. 为什么这样写

### 两栏布局

```css
grid-template-columns: 280px minmax(0, 1fr);
```

意思是左侧固定 280px，右侧占剩余空间。

`minmax(0, 1fr)` 比 `1fr` 更稳，可以避免文章标题太长时把布局撑爆。

### 毛玻璃卡片

```css
background: rgba(255, 255, 255, 0.74);
backdrop-filter: blur(16px);
```

这是 Fuwari 风格的核心之一：半透明卡片 + 背景虚化。

### sidebar sticky

```css
position: sticky;
top: 96px;
```

滚动页面时，左侧个人卡片会停在离顶部 96px 的位置。

### 文章卡片 hover

```css
transform: translateY(-4px);
```

鼠标移上去轻微上浮，不需要复杂动画。

## 9. 手写顺序

建议严格按这个顺序做：

```text
1. 新建 HomeFuwariDemo.vue
2. 写入 template
3. 写入 script
4. 写入 style
5. 在 router/index.js 加 /home-fuwari
6. npm run dev
7. 打开 /home-fuwari 看是否渲染
8. 看接口是否加载文章
9. 测试分类、标签、搜索、分页
10. 和原首页 / 对照
```

启动前端：

```cmd
cd /d D:\Monkey-blog\lyhblog-frontend
npm run dev
```

## 10. 常见报错

### 页面空白

优先检查：

```text
FrontHeader 有没有 import
getArticleSummary 有没有定义
postTotal 有没有定义
template 中变量名和 script 中是否一致
```

### 分类点击没效果

检查：

```js
@click="handleCategoryClick(cat.id)"
```

和：

```js
const handleCategoryClick = (categoryId) => {}
```

名字必须一致。

### 标签点击没效果

检查：

```js
@click="handleTagClick(tag.id)"
```

### 文章跳转失败

检查当前文章详情路由是不是：

```js
path: '/article'
```

你的详情页目前是靠 query id：

```js
router.push({
  path: '/article',
  query: { id },
})
```

所以这里不要写 `/article/${id}`。

## 11. 满意后如何替换首页

等 `HomeFuwariDemo.vue` 效果满意后，有两种替换方式。

### 方式 A：路由直接指向新页面

改 `src/router/index.js`，把首页路由：

```js
{
  path: '/',
  name: 'Home',
  component: () => import('../views/Home.vue')
}
```

改成：

```js
{
  path: '/',
  name: 'Home',
  component: () => import('../views/HomeFuwariDemo.vue')
}
```

这个方式最稳，原来的 `Home.vue` 还保留着。

### 方式 B：复制回 Home.vue

把 `HomeFuwariDemo.vue` 里的内容复制到：

```text
src/views/Home.vue
```

这个方式更干净，但一旦复制错，首页会受影响。所以建议先用方式 A。

## 12. 下一步

主页 v1 写完后，再做：

```text
1. FrontHeader 改成更像 Fuwari 的悬浮导航
2. 新建 Archive.vue 归档时间线
3. ArticleDetail.vue 改成阅读卡片风格
4. 把 Home.vue 拆成组件
5. 加暗色模式
```

第一版目标不是完全像，而是先建立这个骨架：

```text
数据来自 Django
布局由 Vue 控制
视觉向 Fuwari 靠
```
