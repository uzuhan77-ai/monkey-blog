<template>
  <div class="home-page">
    <FrontHeader />

    <HomeHero
      :metrics="heroMetrics"
      :tech-stack="heroTechStack"
      @view-articles="scrollArticles"
      @view-project="goToProject"
      @view-about="goToAbout"
    />

    <HomeArticleSection
      :loading="loading"
      :keyword="keyword"
      :category-list="categoryList"
      :tag-list="tagList"
      :active-category-id="activeCategoryId"
      :active-tag-id="activeTagId"
      :article-list="articleList"
      :total="total"
      :size="size"
      :current="current"
      @update:keyword="keyword = $event"
      @search="handleSearch"
      @reset="handleAllClick"
      @select-category="handleCategoryClick"
      @select-tag="handleTagClick"
      @change-page="handlePageChange"
      @view-detail="goToDetail"
    />

    <HomeProjectSection :highlights="projectHighlights" />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ApiArticleList } from '../api/article'
import { ApiCategoryList } from '../api/category'
import { ApiTagList } from '../api/tag'
import FrontHeader from '../components/FrontHeader.vue'
import HomeArticleSection from '../components/home/home-article-section.vue'
import HomeHero from '../components/home/home-hero.vue'
import HomeProjectSection from '../components/home/home-project-section.vue'

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

const goToProject = () => {
  router.push('/project')
}

const goToAbout = () => {
  router.push('/about')
}

const scrollArticles = () => {
  document.getElementById('home-article-section')?.scrollIntoView({
    behavior: 'smooth',
    block: 'start',
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
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(207, 201, 190, 0.38), transparent 28%),
    linear-gradient(180deg, #f6f3ed 0%, #efeae1 100%);
  color: #1f1f1b;
}
</style>
