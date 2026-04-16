# lyhblog 前台改版计划与完整代码

## 1. 这份文档解决什么问题

你当前的 `lyhblog-frontend` 前台已经具备文章列表、文章详情、登录注册、后台管理这些基础能力，但前台首页仍然偏“列表页”，缺少一个更像个人项目站的展示结构。

这次改版目标不是换框架，也不是去学 Astro，而是借鉴参考项目的页面组织方式，把你现有的 Vue 前台改成更像“可展示项目”的结构。

本次改版重点：

1. 首页增加 Hero 区，让别人一进来就知道你是谁、项目是什么。
2. 新增项目页 `/project`，把 `lyhblog` 当成一个作品来展示。
3. 新增关于页 `/about`，把你的定位、当前阶段、技术栈和下一步计划说清楚。
4. 不改后端接口，先只改前端结构和展示方式。

---

## 2. 阶段计划

### 第一阶段：前台结构升级

目标：先把页面结构搭起来，让前台从“普通列表页”升级成“个人项目站”。

要做的事情：

1. 新增公共前台导航组件 `FrontHeader.vue`
2. 重写首页 `Home.vue`
3. 新增项目页 `Project.vue`
4. 新增关于页 `About.vue`
5. 更新路由 `router/index.js`

这一阶段完成后，你的前台结构会变成：

```text
/
/project
/about
/article?id=xx
/login
/register
/admin/...
```

### 第二阶段：文章详情页优化

目标：把文章详情页也做得更像博客，而不是单纯内容展示。

可以后续再做：

1. 文章详情顶部增加返回入口和相关推荐
2. 评论区样式优化
3. Markdown 渲染优化
4. 阅读数、上一篇/下一篇、相关文章

### 第三阶段：简历化包装

目标：让 `lyhblog` 不只是练手项目，而是能写进简历的项目。

后续可以继续补：

1. README
2. API 文档
3. Docker 部署
4. 环境变量改造
5. Redis 缓存
6. 搜索功能
7. 后台统计面板

---

## 3. 本次落地范围

本次代码只涉及前端，不改后端接口。

本次改动范围：

- `lyhblog-frontend/src/components/FrontHeader.vue` 新增
- `lyhblog-frontend/src/router/index.js` 替换
- `lyhblog-frontend/src/views/Home.vue` 替换
- `lyhblog-frontend/src/views/Project.vue` 新增
- `lyhblog-frontend/src/views/About.vue` 新增

不需要改的地方：

- 后端 Django 接口
- 登录注册接口
- 评论接口
- 后台管理页面

---

## 4. 使用方式

按下面顺序操作：

1. 新建 `src/components/FrontHeader.vue`
2. 用文档里的完整代码替换 `src/router/index.js`
3. 用文档里的完整代码替换 `src/views/Home.vue`
4. 新建 `src/views/Project.vue`
5. 新建 `src/views/About.vue`
6. 运行构建检查

命令：

```bat
cd D:\Monkey-blog\lyhblog-frontend
npm.cmd run build
```

如果想本地预览：

```bat
cd D:\Monkey-blog\lyhblog-frontend
npm.cmd run dev
```

---

## 5. 完整代码

### 5.1 `src/components/FrontHeader.vue`

```vue
<template>
  <header class="front-header">
    <div class="header-inner">
      <router-link to="/" class="brand">
        <span class="brand-mark">LYH</span>
        <div class="brand-text">
          <strong>lyhblog</strong>
          <span>Django + Vue 内容管理系统</span>
        </div>
      </router-link>

      <nav class="nav-list">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-link"
          :class="{ active: isActive(item.path) }"
        >
          {{ item.label }}
        </router-link>
      </nav>

      <div class="nav-actions">
        <router-link to="/login" class="ghost-link">登录</router-link>
        <router-link to="/register" class="solid-link">注册</router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const navItems = [
  { path: '/', label: '首页' },
  { path: '/project', label: '项目' },
  { path: '/about', label: '关于' },
]

const isActive = (path) => route.path === path
</script>

<style scoped>
.front-header {
  position: sticky;
  top: 0;
  z-index: 20;
  backdrop-filter: blur(12px);
  background: rgba(247, 245, 240, 0.88);
  border-bottom: 1px solid rgba(25, 40, 34, 0.08);
}

.header-inner {
  max-width: 1180px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: #17211b;
}

.brand-mark {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, #1f4d3b, #9bb089);
  color: #fff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  letter-spacing: 1px;
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.brand-text strong {
  font-size: 16px;
}

.brand-text span {
  font-size: 12px;
  color: #5d6b63;
}

.nav-list {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-link {
  padding: 10px 14px;
  border-radius: 999px;
  text-decoration: none;
  color: #44524b;
  transition: all 0.2s ease;
}

.nav-link:hover,
.nav-link.active {
  background: #1f4d3b;
  color: #fff;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ghost-link,
.solid-link {
  text-decoration: none;
  font-size: 14px;
}

.ghost-link {
  color: #1f4d3b;
}

.solid-link {
  padding: 10px 14px;
  border-radius: 999px;
  background: #1f4d3b;
  color: #fff;
}

@media (max-width: 860px) {
  .header-inner {
    flex-direction: column;
    align-items: stretch;
  }

  .nav-list,
  .nav-actions {
    justify-content: center;
    flex-wrap: wrap;
  }
}
</style>
```

---

### 5.2 `src/router/index.js`

```js
import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
  },
  {
    path: '/project',
    name: 'Project',
    component: () => import('../views/Project.vue'),
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue'),
  },
  {
    path: '/article',
    name: 'ArticleDetail',
    component: () => import('../views/ArticleDetail.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/register.vue'),
  },
  {
    path: '/admin',
    component: () => import('../views/admin/Layout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    redirect: '/admin/article',
    children: [
      {
        path: 'article',
        name: 'AdminArticle',
        component: () => import('../views/admin/ArticleList.vue'),
      },
      {
        path: 'article/add',
        name: 'AdminArticleAdd',
        component: () => import('../views/admin/ArticleEdit.vue'),
      },
      {
        path: 'article/edit/:id',
        name: 'AdminArticleEdit',
        component: () => import('../views/admin/ArticleEdit.vue'),
      },
      {
        path: 'comment',
        name: 'AdminComment',
        component: () => import('../views/admin/CommentList.vue'),
      },
      {
        path: 'category',
        name: 'AdminCategory',
        component: () => import('../views/admin/CategoryList.vue'),
      },
      {
        path: 'tag',
        name: 'AdminTag',
        component: () => import('../views/admin/TagList.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const requiresAdmin = to.matched.some((record) => record.meta.requiresAdmin)

  if (requiresAuth && !userStore.isLogin) {
    next({
      path: '/login',
      query: { redirect: to.fullPath },
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

### 5.3 `src/views/Home.vue`

```vue
<template>
  <div class="home-page">
    <FrontHeader />

    <section class="hero-section">
      <div class="hero-content">
        <p class="hero-label">PERSONAL PROJECT / CONTENT SYSTEM</p>
        <h1>把 blog 做成能展示的项目</h1>
        <p class="hero-desc">
          lyhblog 是一个基于 Django REST Framework + Vue3 的前后端分离内容管理系统，
          当前已经完成文章列表、文章详情、分类标签筛选、登录注册、评论和后台基础管理。
        </p>

        <div class="hero-actions">
          <el-button type="primary" size="large" @click="scrollToArticles">
            查看文章
          </el-button>
          <el-button plain size="large" @click="router.push('/project')">
            查看项目
          </el-button>
          <el-button text size="large" @click="router.push('/about')">
            关于我
          </el-button>
        </div>

        <div class="tech-stack">
          <span v-for="item in heroTechStack" :key="item" class="tech-pill">
            {{ item }}
          </span>
        </div>
      </div>

      <div class="hero-panel">
        <div class="stats-grid">
          <div v-for="item in stats" :key="item.label" class="stat-card">
            <span class="stat-label">{{ item.label }}</span>
            <strong class="stat-value">{{ item.value }}</strong>
          </div>
        </div>

        <div class="hero-note">
          <span class="note-title">当前阶段</span>
          <p>
            先把这个 blog 做成一个完整、可展示、可部署的全栈项目，
            再继续往 Python 后端 / 爬虫方向延伸。
          </p>
        </div>
      </div>
    </section>

    <section ref="articleSectionRef" class="article-section">
      <div class="section-head">
        <div>
          <p class="section-label">ARTICLE LIST</p>
          <h2>最新文章</h2>
        </div>
        <p class="section-tip">先把内容管理系统做完整，再继续做项目包装。</p>
      </div>

      <div class="filter-panel">
        <div class="filter-row">
          <span class="filter-title">搜索</span>
          <el-input
            v-model="keyword"
            class="search-input"
            clearable
            placeholder="输入标题或内容关键词"
            @keyup.enter="handleSearch"
          />
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleAllClick">重置</el-button>
        </div>

        <div class="filter-row">
          <span class="filter-title">分类</span>
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
          <span class="filter-title">标签</span>
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

      <el-skeleton v-if="loading" :rows="6" animated />
      <el-empty v-else-if="articleList.length === 0" description="暂无文章" />

      <div v-else class="article-grid">
        <article
          v-for="item in articleList"
          :key="item.id"
          class="article-card"
          @click="goToDetail(item.id)"
        >
          <div class="article-top">
            <span class="article-category">
              {{ item.category?.name || '未分类' }}
            </span>
            <span class="article-date">{{ item.create_time }}</span>
          </div>

          <h3 class="article-title">{{ item.title }}</h3>
          <p class="article-summary">{{ getArticleSummary(item) }}</p>

          <div class="tag-list">
            <span
              v-for="tag in item.tags || []"
              :key="tag.id"
              class="tag-item"
            >
              {{ tag.name }}
            </span>
          </div>

          <div class="article-footer">
            <span>点击查看详情</span>
            <span class="arrow">→</span>
          </div>
        </article>
      </div>

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
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import FrontHeader from '../components/FrontHeader.vue'
import { ApiArticleList } from '../api/article'
import { ApiCategoryList } from '../api/category'
import { ApiTagList } from '../api/tag'

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
const articleSectionRef = ref(null)

const heroTechStack = ['Django', 'DRF', 'Vue 3', 'Element Plus', 'Axios', 'Pinia']

const stats = computed(() => [
  { label: '文章总数', value: dashboardTotal.value || total.value },
  { label: '分类数量', value: categoryList.value.length },
  { label: '标签数量', value: tagList.value.length },
])

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
      articleList.value = res.data.data
      total.value = res.data.total

      if (!activeCategoryId.value && !activeTagId.value && !keyword.value.trim()) {
        dashboardTotal.value = res.data.total
      }
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
  keyword.value = ''
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

const scrollToArticles = () => {
  articleSectionRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const getArticleSummary = (item) => {
  if (item.summary) {
    return item.summary
  }

  if (item.content) {
    return item.content.slice(0, 90)
  }

  return '暂无文章摘要'
}

onMounted(() => {
  getArticleList()
  getCategoryList()
  getTagList()
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(177, 193, 160, 0.35), transparent 28%),
    linear-gradient(180deg, #f7f5f0 0%, #eef2ea 100%);
  color: #18231d;
}

.hero-section,
.article-section {
  max-width: 1180px;
  margin: 0 auto;
  padding: 40px 24px;
}

.hero-section {
  display: grid;
  grid-template-columns: 1.25fr 0.9fr;
  gap: 24px;
  align-items: stretch;
}

.hero-content,
.hero-panel,
.filter-panel,
.article-card {
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(24, 35, 29, 0.08);
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(24, 35, 29, 0.06);
}

.hero-content {
  padding: 36px;
}

.hero-label,
.section-label,
.note-title {
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-size: 12px;
  color: #6a786f;
}

.hero-content h1 {
  margin: 16px 0;
  font-size: 46px;
  line-height: 1.15;
}

.hero-desc {
  margin: 0;
  max-width: 680px;
  font-size: 16px;
  line-height: 1.8;
  color: #4b5851;
}

.hero-actions {
  margin-top: 28px;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.tech-stack {
  margin-top: 28px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tech-pill {
  padding: 8px 14px;
  border-radius: 999px;
  background: #e4ecdf;
  color: #234735;
  font-size: 13px;
}

.hero-panel {
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.stat-card {
  padding: 18px;
  border-radius: 18px;
  background: linear-gradient(180deg, #f8faf7 0%, #edf4e9 100%);
}

.stat-label {
  display: block;
  margin-bottom: 8px;
  font-size: 13px;
  color: #69776f;
}

.stat-value {
  font-size: 28px;
  color: #153f2f;
}

.hero-note {
  padding: 22px;
  border-radius: 18px;
  background: #183428;
  color: #eef4ef;
}

.hero-note p {
  margin: 12px 0 0;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.84);
}

.section-head {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 16px;
  margin-bottom: 20px;
}

.section-head h2 {
  margin: 10px 0 0;
  font-size: 32px;
}

.section-tip {
  margin: 0;
  color: #607067;
}

.filter-panel {
  padding: 24px;
  margin-bottom: 24px;
}

.filter-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-row + .filter-row {
  margin-top: 14px;
}

.filter-title {
  min-width: 64px;
  color: #38453f;
  font-weight: 600;
}

.search-input {
  width: 320px;
}

.article-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
}

.article-card {
  padding: 24px;
  cursor: pointer;
  transition: transform 0.22s ease, box-shadow 0.22s ease;
}

.article-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 24px 60px rgba(24, 35, 29, 0.1);
}

.article-top,
.article-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.article-category {
  color: #1f4d3b;
  font-weight: 600;
}

.article-date {
  color: #7a8880;
  font-size: 13px;
}

.article-title {
  margin: 18px 0 12px;
  font-size: 22px;
  line-height: 1.4;
}

.article-summary {
  margin: 0;
  min-height: 78px;
  color: #526059;
  line-height: 1.8;
}

.tag-list {
  margin-top: 18px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  padding: 6px 10px;
  border-radius: 999px;
  background: #eef3ec;
  color: #365848;
  font-size: 12px;
}

.article-footer {
  margin-top: 22px;
  color: #365848;
  font-size: 14px;
}

.arrow {
  font-size: 18px;
}

.pagination-box {
  margin-top: 28px;
  display: flex;
  justify-content: center;
}

@media (max-width: 1024px) {
  .hero-section {
    grid-template-columns: 1fr;
  }

  .article-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 34px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .article-grid {
    grid-template-columns: 1fr;
  }

  .section-head {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-input {
    width: 100%;
  }
}
</style>
```

---

### 5.4 `src/views/Project.vue`

```vue
<template>
  <div class="project-page">
    <FrontHeader />

    <section class="project-hero">
      <div class="hero-card intro-card">
        <p class="eyebrow">PROJECT OVERVIEW</p>
        <h1>lyhblog 前后端分离内容管理系统</h1>
        <p class="hero-desc">
          这是我当前最重要的个人项目，目标不是只做一个能增删改查的博客，
          而是把它打磨成一个可以展示项目思路、前后端能力和后续成长路线的作品。
        </p>

        <div class="hero-actions">
          <el-button type="primary" size="large" @click="router.push('/')">
            查看首页
          </el-button>
          <el-button plain size="large" @click="router.push('/admin/article')">
            查看后台
          </el-button>
        </div>
      </div>

      <div class="hero-card status-card">
        <p class="eyebrow">CURRENT STATUS</p>
        <div class="status-grid">
          <div class="status-item" v-for="item in statusItems" :key="item.label">
            <span>{{ item.label }}</span>
            <strong>{{ item.value }}</strong>
          </div>
        </div>
      </div>
    </section>

    <section class="project-section">
      <div class="section-head">
        <div>
          <p class="eyebrow">TECH STACK</p>
          <h2>当前技术栈</h2>
        </div>
      </div>

      <div class="tag-wrap">
        <span v-for="item in techStack" :key="item" class="stack-tag">
          {{ item }}
        </span>
      </div>
    </section>

    <section class="project-section">
      <div class="section-head">
        <div>
          <p class="eyebrow">MODULES</p>
          <h2>项目模块拆分</h2>
        </div>
      </div>

      <div class="module-grid">
        <article class="module-card" v-for="item in modules" :key="item.title">
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
          <ul>
            <li v-for="point in item.points" :key="point">{{ point }}</li>
          </ul>
        </article>
      </div>
    </section>

    <section class="project-section two-column">
      <div class="panel-card">
        <p class="eyebrow">COMPLETED</p>
        <h2>当前已完成</h2>
        <ul class="plain-list">
          <li v-for="item in completedList" :key="item">{{ item }}</li>
        </ul>
      </div>

      <div class="panel-card">
        <p class="eyebrow">NEXT STEP</p>
        <h2>下一步计划</h2>
        <ul class="plain-list">
          <li v-for="item in nextSteps" :key="item">{{ item }}</li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import FrontHeader from '../components/FrontHeader.vue'

const router = useRouter()

const statusItems = [
  { label: '项目定位', value: '全栈内容管理系统' },
  { label: '当前阶段', value: '前台结构升级中' },
  { label: '核心目标', value: '做成可展示项目' },
]

const techStack = [
  'Python',
  'Django',
  'Django REST Framework',
  'Vue 3',
  'Vue Router',
  'Pinia',
  'Axios',
  'Element Plus',
  'MySQL',
]

const modules = [
  {
    title: '前台展示模块',
    description: '负责文章列表、文章详情、分类筛选、标签筛选和基础内容浏览。',
    points: ['首页文章列表', '分类标签筛选', '文章详情', '评论展示与提交'],
  },
  {
    title: '用户认证模块',
    description: '负责用户登录、注册、Token 认证和基础访问控制。',
    points: ['登录', '注册', 'Token 保存', '后台路由守卫'],
  },
  {
    title: '后台管理模块',
    description: '负责文章、分类、标签和评论的后台管理。',
    points: ['文章新增编辑删除', '评论列表与删除', '分类管理', '标签管理'],
  },
]

const completedList = [
  '前台文章列表页',
  '文章详情页',
  '登录注册页',
  '后台文章管理',
  '后台评论管理',
  '后台分类管理',
  '后台标签管理',
]

const nextSteps = [
  '优化前台首页结构和视觉层次',
  '增加项目展示页和关于页',
  '清理乱码文本与文案表达',
  '补充 README 与部署文档',
  '后续增加缓存、搜索、部署方案',
]
</script>

<style scoped>
.project-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f7f5f0 0%, #eef2ea 100%);
  color: #18231d;
}

.project-hero,
.project-section {
  max-width: 1180px;
  margin: 0 auto;
  padding: 40px 24px;
}

.project-hero {
  display: grid;
  grid-template-columns: 1.3fr 0.9fr;
  gap: 24px;
}

.hero-card,
.module-card,
.panel-card {
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.84);
  border: 1px solid rgba(24, 35, 29, 0.08);
  box-shadow: 0 20px 60px rgba(24, 35, 29, 0.06);
}

.intro-card,
.status-card,
.panel-card {
  padding: 32px;
}

.eyebrow {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-size: 12px;
  color: #6b796f;
}

.intro-card h1 {
  margin: 16px 0;
  font-size: 40px;
  line-height: 1.2;
}

.hero-desc {
  margin: 0;
  color: #4b5851;
  line-height: 1.8;
}

.hero-actions {
  margin-top: 24px;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.status-grid {
  margin-top: 18px;
  display: grid;
  gap: 14px;
}

.status-item {
  padding: 18px;
  border-radius: 18px;
  background: #edf4e9;
}

.status-item span {
  display: block;
  margin-bottom: 8px;
  color: #5e6d64;
  font-size: 13px;
}

.status-item strong {
  font-size: 20px;
  color: #173e2f;
}

.section-head h2,
.panel-card h2 {
  margin: 12px 0 0;
  font-size: 30px;
}

.tag-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.stack-tag {
  padding: 10px 16px;
  border-radius: 999px;
  background: #dfe8d8;
  color: #234735;
}

.module-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
}

.module-card {
  padding: 28px;
}

.module-card h3 {
  margin-top: 0;
  margin-bottom: 12px;
  font-size: 22px;
}

.module-card p {
  margin: 0 0 16px;
  color: #526059;
  line-height: 1.8;
}

.module-card ul,
.plain-list {
  margin: 0;
  padding-left: 18px;
  color: #334139;
  line-height: 1.9;
}

.two-column {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
}

@media (max-width: 1024px) {
  .project-hero,
  .two-column,
  .module-grid {
    grid-template-columns: 1fr;
  }
}
</style>
```

---

### 5.5 `src/views/About.vue`

```vue
<template>
  <div class="about-page">
    <FrontHeader />

    <section class="about-hero">
      <div class="hero-main">
        <p class="eyebrow">ABOUT ME</p>
        <h1>关于这个项目，也关于现在的我</h1>
        <p class="hero-desc">
          我现在正通过 `lyhblog` 这个项目，系统地练习 Django + Vue 的前后端分离开发。
          现阶段目标不是假装自己已经是成熟工程师，而是先把一个完整项目真正做完、讲清楚、跑起来。
        </p>
      </div>

      <div class="hero-side">
        <p class="eyebrow">CURRENT FOCUS</p>
        <ul class="focus-list">
          <li v-for="item in currentFocus" :key="item">{{ item }}</li>
        </ul>
      </div>
    </section>

    <section class="about-section two-column">
      <div class="panel-card">
        <p class="eyebrow">PROFILE</p>
        <h2>当前定位</h2>
        <div class="info-list">
          <div class="info-item" v-for="item in profileInfo" :key="item.label">
            <span>{{ item.label }}</span>
            <strong>{{ item.value }}</strong>
          </div>
        </div>
      </div>

      <div class="panel-card">
        <p class="eyebrow">SKILLS</p>
        <h2>当前掌握的技术</h2>
        <div class="tag-wrap">
          <span v-for="item in skills" :key="item" class="skill-tag">{{ item }}</span>
        </div>
      </div>
    </section>

    <section class="about-section two-column">
      <div class="panel-card">
        <p class="eyebrow">ROADMAP</p>
        <h2>接下来要补的能力</h2>
        <ul class="plain-list">
          <li v-for="item in nextPlan" :key="item">{{ item }}</li>
        </ul>
      </div>

      <div class="panel-card">
        <p class="eyebrow">CONTACT</p>
        <h2>项目信息</h2>
        <ul class="plain-list">
          <li>项目名：lyhblog</li>
          <li>项目形态：前后端分离内容管理系统</li>
          <li>当前方向：先完成 blog，再延伸到 Python 后端 / 爬虫方向</li>
          <li>仓库地址：后续补充到 GitHub</li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script setup>
import FrontHeader from '../components/FrontHeader.vue'

const currentFocus = [
  '完成前台结构升级',
  '把项目做成可展示作品',
  '补齐项目文档与部署说明',
  '为后续 Python 后端 / 爬虫方向打基础',
]

const profileInfo = [
  { label: '当前阶段', value: '项目学习者' },
  { label: '主线技术栈', value: 'Django + Vue' },
  { label: '当前目标', value: '做完并包装好 lyhblog' },
]

const skills = [
  'Python',
  'Django',
  'Django REST Framework',
  'Vue 3',
  'Vue Router',
  'Pinia',
  'Axios',
  'Element Plus',
  'MySQL 基础',
  'Git / GitHub 基础',
]

const nextPlan = [
  '继续完善前后台 CRUD 闭环',
  '清理乱码文案和项目表达',
  '补充 README、截图和 API 说明',
  '补充部署故事：Nginx、Docker、云服务器',
  '后续单独做一个小型爬虫 / 数据管理项目',
]
</script>

<style scoped>
.about-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #f7f5f0 0%, #eef2ea 100%);
  color: #18231d;
}

.about-hero,
.about-section {
  max-width: 1180px;
  margin: 0 auto;
  padding: 40px 24px;
}

.about-hero {
  display: grid;
  grid-template-columns: 1.25fr 0.9fr;
  gap: 24px;
}

.hero-main,
.hero-side,
.panel-card {
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.84);
  border: 1px solid rgba(24, 35, 29, 0.08);
  box-shadow: 0 20px 60px rgba(24, 35, 29, 0.06);
  padding: 32px;
}

.eyebrow {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-size: 12px;
  color: #6b796f;
}

.hero-main h1,
.panel-card h2 {
  margin: 16px 0 0;
  font-size: 38px;
  line-height: 1.2;
}

.hero-desc {
  margin-top: 18px;
  color: #4b5851;
  line-height: 1.9;
}

.focus-list,
.plain-list {
  margin: 18px 0 0;
  padding-left: 18px;
  line-height: 1.9;
  color: #334139;
}

.two-column {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
}

.info-list {
  margin-top: 18px;
  display: grid;
  gap: 14px;
}

.info-item {
  padding: 18px;
  border-radius: 18px;
  background: #edf4e9;
}

.info-item span {
  display: block;
  color: #5e6d64;
  font-size: 13px;
  margin-bottom: 8px;
}

.info-item strong {
  font-size: 20px;
  color: #173e2f;
}

.tag-wrap {
  margin-top: 18px;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.skill-tag {
  padding: 10px 16px;
  border-radius: 999px;
  background: #dfe8d8;
  color: #234735;
}

@media (max-width: 1024px) {
  .about-hero,
  .two-column {
    grid-template-columns: 1fr;
  }
}
</style>
```

---

## 6. 实施顺序建议

推荐你按下面顺序落地：

1. 先新增 `FrontHeader.vue`
2. 再替换 `router/index.js`
3. 再替换 `Home.vue`
4. 然后新增 `Project.vue`
5. 最后新增 `About.vue`
6. 跑一次 `npm.cmd run build`

这样做的原因是：

- 先把路由和公共导航搭起来
- 再做首页
- 然后补项目页和关于页
- 整体结构更清楚，不容易改乱

---

## 7. 为什么这套改法适合你当前阶段

原因很简单：

1. 不需要换框架
2. 不需要重做后端
3. 能直接提升你项目的展示感
4. 能把 `lyhblog` 从“博客练手项目”往“可写进简历的项目”推进一大步

你现在最应该做的不是再开一个新坑，而是把现有项目包装完整。

---

## 8. 下一步建议

这份代码落完以后，下一步建议做下面几件事：

1. 优化 `ArticleDetail.vue` 的阅读页结构
2. 清理前端乱码中文
3. 补项目 README
4. 给首页和项目页补几张截图
5. 最后再做部署和 Docker

如果继续往后写下一份文档，建议标题可以叫：

`lyhblog-前台详情页优化与项目包装.md`
