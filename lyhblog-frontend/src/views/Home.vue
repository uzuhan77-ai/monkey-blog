<template>
  <div class="home-page">
    <FrontHeader />
    <section class="hero-section">
      <div class="hero-section">
        <p class="hero-label">PERSONAL PROJECT / CONTENT SYSTEM</p>
        <h1>把 blog 做成能展示的项目</h1>
        <p class="hero-desc">
          当前已经完成文章列表、文章详情、分类标签筛选、登录注册、评论和后台基础管理。
        </p>

        <div class="hero-actions">
          <el-button type="primary" size="large" @click="scrollArticles">
            查看文章
          </el-button>
          <el-button plain size="large" @click="router.push('/project')">
            查看项目
          </el-button>
          <el-button text size="large" @click="router.push('/About')">
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

    <section ref="acticleSectionRef" class="article-section">
      <div class="section-head">
        <div>
          <p class="section-label">ARTICLE LIST</p>
          <h2>最新文章</h2>
        </div>
        <p class="section-tip">先把内容管理系统做完整，再继续做项目包装。</p> 
      </div>
        
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
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleAllClick">重置</el-button>
        </div>

        <div class="filter-row">
          <span class="filter-title">分类:</span>
          
          <el-button 
            :type="activeCategoryId ===null ? 'primary' : 'default'"
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
      
      <el-skeleton v-if="loading" :rows="6" animated/>

      <el-empty v-else-if="articleList.length === 0" description="暂无文章"/>

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

      <!-- 分页 -->
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
import { ref, onMounted } from 'vue'
import { ApiArticleList } from '../api/article'
import { ApiCategoryList } from '../api/category'
import { ApiTagList } from '../api/tag'
import { useRouter } from 'vue-router'
import {ElMessage} from 'element-plus'
import FrontHeader from '../components/FrontHeader.vue'
import {computed} from 'vue'

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

const heroTechStack = ['Django', 'DRF' , 'Vue3' , 'Element' , 'Axios' , 'Pinia']

const stats = computed(() =>[
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
      keyword: keyword.value.trim()

    })
    if (res.data.code == 200) {
      articleList.value = res.data.data
      total.value = res.data.total
    }
      if(!activeCategoryId.value && !activeTagId.value && !keyword.value.trim()){
        dashboardTotal.value = res.data.total
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
const getTagList = async () =>{
  try{
    const res = await ApiTagList()
    if(res.data.code == 200){
      tagList.value = res.data.data
    }
  }catch(error){
    ElMessage.error('标签列表加载失败')
  }
}

const handleAllClick = () =>{
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

const handleTagClick = (tagId) =>{
  activeTagId.value = tagId
  current.value = 1
  getArticleList()
}

const handleSearch = () =>{
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

const scrollArticles = () =>{
  articleSectionRef.value?.scrollIntoView({behavior: 'smooth' , block: 'start'})
}

const getArticleSummary = (item) =>{
  if(item.summary){
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