<template>
  <div class="home-page">
    <h1>文章列表</h1>

    <div class="filter-panel">
      <div class="filter-row">
        <span class="filter-title">快速筛选:</span>
        <el-button 
          :type="activeCategoryId === null && activeTagId ===null ? 'primary' : 'default'"
          size="small"
          @click="handleAllClick"
        >
          全部文章
        </el-button>
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
    <el-skeleton v-if="loading" :rows="5" animated/>

    <el-empty v-else-if="articleList.length === 0" description="暂无文章"/>

    <el-row v-else :gutter="20">
      <el-col
        v-for="item in articleList"
        :key="item.id"
        :xs="24"
        :sm="12"
        :md="8"
        style="margin-bottom: 20px"
      >
        <el-card class="article-card"shadow="hover" @click="goToDetail(item.id)">
          <h3 class="article-title">
            {{ item.title }}
          </h3>

          <p class="article-summary">
            {{ item.content?.substring(0,50) || '暂无内容' }}
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
  </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue'
import { ApiArticleList } from '../api/article'
import { ApiCategoryList } from '../api/category'
import { ApiTagList } from '../api/tag'
import { useRouter } from 'vue-router'
import {ElMessage} from 'element-plus'

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

const getArticleList = async () => {
  loading.value = true
  try {
    const res = await ApiArticleList({
      current: current.value,
      size: size.value,
      category_id: activeCategoryId.value,
      tag_id: activeTagId.value

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