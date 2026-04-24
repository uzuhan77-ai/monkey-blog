# lyhblog 首页 Home.vue 参考代码

日期: 2026-04-24

适用文件:
- `D:\Monkey-blog\lyhblog-frontend\src\views\Home.vue`

说明:
- 这是首页改版的完整参考代码文档
- 不会自动改你的项目文件
- 你可以直接对照这份文档，手动替换 `Home.vue`
- 视频文件建议放到 `lyhblog-frontend/public/videos/home-hero.mp4`
- 如果暂时没有视频，这版代码会显示占位提示，不会白屏

---

## 替换建议

直接把 `Home.vue` 整体替换为下面这版。

```vue
<template>
  <div class="home-page">
    <FrontHeader />

    <section class="hero-section">
      <div class="hero-video-panel">
        <div class="hero-media">
          <video
            v-if="!videoError"
            class="hero-video"
            :src="heroVideoSrc"
            autoplay
            muted
            loop
            playsinline
            @error="handleVideoError"
          ></video>

          <div v-else class="hero-video-placeholder">
            <span>这里后续替换为项目录屏视频</span>
          </div>

          <div class="hero-media-mask"></div>
        </div>

        <div class="hero-overlay">
          <p class="hero-label">LYHBLOG / PERSONAL CONTENT SYSTEM</p>
          <h1 class="hero-title">把 blog 做成一个真正可展示的项目</h1>
          <p class="hero-desc">
            用 Django 与 Vue 搭建前后端分离的内容系统，记录学习、沉淀内容，
            也把它当成我的工程作品。
          </p>

          <div class="hero-actions">
            <el-button type="primary" size="large" @click="scrollArticles">
              查看文章
            </el-button>
            <el-button plain size="large" @click="router.push('/project')">
              查看项目
            </el-button>
            <el-button text size="large" @click="router.push('/about')">
              关于我
            </el-button>
          </div>

          <div class="hero-status">
            当前阶段：先把博客首页、文章体验和内容结构打磨完整，AI 功能后置。
          </div>
        </div>
      </div>

      <div class="hero-bottom-row">
        <div class="hero-meta-grid">
          <article
            v-for="item in heroMetrics"
            :key="item.label"
            class="meta-card"
          >
            <span class="meta-label">{{ item.label }}</span>
            <strong class="meta-value">{{ item.value }}</strong>
            <p class="meta-desc">{{ item.desc }}</p>
          </article>
        </div>

        <div class="hero-tech-panel">
          <p class="section-label">TECH STACK</p>
          <h2>先把内容系统做完整，再继续打磨展示和部署</h2>
          <p class="tech-desc">
            首页重新定型为视频首屏，下面继续承接搜索、分类、标签和文章列表，
            整体回到一个真正可阅读、可展示的博客项目。
          </p>

          <div class="tech-stack">
            <span v-for="item in heroTechStack" :key="item" class="tech-pill">
              {{ item }}
            </span>
          </div>
        </div>
      </div>
    </section>

    <section ref="articleSectionRef" class="article-section">
      <div class="section-head">
        <div>
          <p class="section-label">ARTICLE LIST</p>
          <h2>最新文章</h2>
        </div>
        <p class="section-tip">
          先把内容系统做完整，再继续打磨项目展示和部署能力。
        </p>
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
          v-model:current-page="current"
          background
          layout="total, prev, pager, next"
          :total="total"
          :page-size="size"
          @current-change="handlePageChange"
        />
      </div>
    </section>

    <section class="project-section">
      <div class="project-copy">
        <p class="section-label">PROJECT NOTE</p>
        <h2>现在的重点不是扩功能，而是把博客体验做扎实</h2>
        <p class="project-desc">
          这个项目当前聚焦首页、文章详情、分类标签和后台管理，
          先把它做成一套完整、可展示、可持续迭代的内容系统。
        </p>
      </div>

      <div class="project-grid">
        <article
          v-for="item in projectHighlights"
          :key="item.title"
          class="project-card"
        >
          <h3>{{ item.title }}</h3>
          <p>{{ item.desc }}</p>
        </article>
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

const loading = ref(false)
const router = useRouter()

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

const videoError = ref(false)
const heroVideoSrc = '/videos/home-hero.mp4'

const heroTechStack = [
  'Django',
  'DRF',
  'Vue 3',
  'Element Plus',
  'Axios',
  'Pinia',
]

const projectHighlights = [
  {
    title: '首页重新定型',
    desc: '视频首屏、内容导向、简约风格，先把首页的第一眼体验做稳定。',
  },
  {
    title: '文章体验优先',
    desc: '保留搜索、分类、标签和文章承接，让首页既能展示，也能真正阅读。',
  },
  {
    title: '后台继续补齐',
    desc: '围绕分类、标签、评论和管理入口继续完善，先把博客主线做完整。',
  },
]

const heroMetrics = computed(() => [
  {
    label: '文章总数',
    value: dashboardTotal.value || total.value,
    desc: '首页直接承接内容展示，不做空页面。',
  },
  {
    label: '分类数量',
    value: categoryList.value.length,
    desc: '保留按主题筛选，强化内容结构。',
  },
  {
    label: '标签数量',
    value: tagList.value.length,
    desc: '继续补齐标签体系和阅读入口。',
  },
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
      articleList.value = res.data.data || []
      total.value = Number(res.data.total || 0)
    }

    if (
      !activeCategoryId.value &&
      !activeTagId.value &&
      !keyword.value.trim()
    ) {
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

const scrollArticles = () => {
  articleSectionRef.value?.scrollIntoView({
    behavior: 'smooth',
    block: 'start',
  })
}

const handleVideoError = () => {
  videoError.value = true
}

const stripHtml = (text = '') => {
  return String(text)
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}

const getArticleSummary = (item) => {
  if (item.summary) {
    return stripHtml(item.summary).slice(0, 90)
  }

  if (item.content) {
    return stripHtml(item.content).slice(0, 90)
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
    radial-gradient(circle at top left, rgba(207, 201, 190, 0.38), transparent 28%),
    linear-gradient(180deg, #f6f3ed 0%, #efeae1 100%);
  color: #1f1f1b;
}

.hero-section,
.article-section,
.project-section {
  max-width: 1180px;
  margin: 0 auto;
  padding: 36px 24px;
}

.hero-video-panel,
.filter-panel,
.article-card,
.project-card,
.meta-card,
.hero-tech-panel {
  border: 1px solid rgba(31, 31, 27, 0.08);
  background: rgba(255, 255, 255, 0.68);
  box-shadow: 0 20px 60px rgba(31, 31, 27, 0.06);
  backdrop-filter: blur(14px);
}

.hero-video-panel {
  position: relative;
  min-height: 560px;
  overflow: hidden;
  border-radius: 32px;
}

.hero-media,
.hero-video,
.hero-media-mask {
  position: absolute;
  inset: 0;
}

.hero-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-video-placeholder {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  background:
    linear-gradient(135deg, rgba(119, 117, 106, 0.18), rgba(255, 255, 255, 0.12)),
    #d8d2c8;
  color: #5f5a4f;
  font-size: 16px;
  letter-spacing: 0.04em;
}

.hero-media-mask {
  background:
    linear-gradient(90deg, rgba(21, 20, 18, 0.62) 0%, rgba(21, 20, 18, 0.22) 48%, rgba(21, 20, 18, 0.08) 100%),
    linear-gradient(180deg, rgba(21, 20, 18, 0.12) 0%, rgba(21, 20, 18, 0.38) 100%);
}

.hero-overlay {
  position: relative;
  z-index: 2;
  min-height: 560px;
  max-width: 720px;
  padding: 52px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  color: #f7f2ea;
}

.hero-label,
.section-label {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(247, 242, 234, 0.78);
}

.section-label {
  color: #7a7366;
}

.hero-title {
  margin: 16px 0 18px;
  font-size: 52px;
  line-height: 1.1;
  font-weight: 600;
}

.hero-desc {
  margin: 0;
  max-width: 560px;
  font-size: 16px;
  line-height: 1.9;
  color: rgba(247, 242, 234, 0.88);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 28px;
}

.hero-status {
  margin-top: 22px;
  display: inline-flex;
  width: fit-content;
  max-width: 100%;
  padding: 12px 16px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.14);
  color: rgba(247, 242, 234, 0.92);
  font-size: 14px;
  line-height: 1.6;
}

.hero-bottom-row {
  margin-top: 20px;
  display: grid;
  grid-template-columns: 1.25fr 0.9fr;
  gap: 20px;
}

.hero-meta-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.meta-card,
.hero-tech-panel {
  border-radius: 24px;
  padding: 24px;
}

.meta-label {
  display: block;
  font-size: 13px;
  color: #716b60;
}

.meta-value {
  display: block;
  margin-top: 12px;
  font-size: 34px;
  line-height: 1;
  color: #22201b;
}

.meta-desc {
  margin: 14px 0 0;
  color: #666154;
  line-height: 1.8;
  font-size: 14px;
}

.hero-tech-panel h2 {
  margin: 10px 0 14px;
  font-size: 28px;
  line-height: 1.35;
}

.tech-desc {
  margin: 0;
  color: #625d51;
  line-height: 1.85;
}

.tech-stack {
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tech-pill {
  padding: 8px 14px;
  border-radius: 999px;
  background: rgba(111, 127, 106, 0.12);
  color: #5d6a59;
  font-size: 13px;
}

.section-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
}

.section-head h2,
.project-copy h2 {
  margin: 10px 0 0;
  font-size: 34px;
  line-height: 1.25;
}

.section-tip,
.project-desc {
  margin: 0;
  color: #676153;
  line-height: 1.85;
}

.filter-panel {
  padding: 24px;
  border-radius: 24px;
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
  min-width: 52px;
  color: #373227;
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
  border-radius: 24px;
  padding: 24px;
  cursor: pointer;
  transition: transform 0.22s ease, box-shadow 0.22s ease;
}

.article-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 24px 60px rgba(31, 31, 27, 0.1);
}

.article-top,
.article-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.article-category {
  color: #5d6a59;
  font-weight: 600;
}

.article-date {
  color: #847d70;
  font-size: 13px;
}

.article-title {
  margin: 18px 0 12px;
  font-size: 22px;
  line-height: 1.45;
  color: #1f1f1b;
}

.article-summary {
  margin: 0;
  min-height: 78px;
  color: #5f5a4f;
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
  background: rgba(111, 127, 106, 0.1);
  color: #5d6a59;
  font-size: 12px;
}

.article-footer {
  margin-top: 22px;
  color: #5d6a59;
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

.project-section {
  display: grid;
  grid-template-columns: 0.95fr 1.05fr;
  gap: 20px;
  padding-top: 8px;
  padding-bottom: 60px;
}

.project-copy {
  padding: 8px 0;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.project-card {
  border-radius: 24px;
  padding: 24px;
}

.project-card h3 {
  margin: 0 0 12px;
  font-size: 20px;
  line-height: 1.4;
}

.project-card p {
  margin: 0;
  color: #645e52;
  line-height: 1.8;
}

@media (max-width: 1024px) {
  .hero-bottom-row,
  .project-section,
  .project-grid {
    grid-template-columns: 1fr;
  }

  .hero-meta-grid,
  .article-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .hero-video-panel,
  .hero-overlay {
    min-height: 500px;
  }
}

@media (max-width: 768px) {
  .hero-section,
  .article-section,
  .project-section {
    padding-left: 16px;
    padding-right: 16px;
  }

  .hero-video-panel,
  .hero-overlay {
    min-height: 440px;
  }

  .hero-overlay {
    padding: 24px;
  }

  .hero-title {
    font-size: 34px;
  }

  .hero-status {
    border-radius: 20px;
  }

  .hero-meta-grid,
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

## 你手动改时注意这几点

1. 路由里 About 是 `/about`，按钮跳转别写错
2. `articleSectionRef` 要和模板里的 `ref` 保持一致
3. 如果你没有视频文件，不影响页面显示
4. 如果后端返回的 `summary` 或 `content` 带 HTML，这版代码已经做了去标签处理
5. 这版是结构和基础样式参考，不是最终视觉稿

---

## 视频文件放置建议

推荐路径:

`D:\Monkey-blog\lyhblog-frontend\public\videos\home-hero.mp4`

如果目录没有，你自己建一下:

- `public`
- `public/videos`

---

## 结论

这份文档就是你要的“完整代码版参考文档”。  
你先照着改 `Home.vue`，改完如果有报错或者样式结构不对，我再继续帮你收。
