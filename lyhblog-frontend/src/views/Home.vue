<template>
    <div class="home-page">
      <h1>文章列表</h1>
  
      <!-- 分类筛选 -->
      <div class="filter-panel">

        <div class="filter-row">
          <span class="filte-title">快速筛选:</span>
    
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
            :size="small"
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
      <!-- 文章列表 -->
      <el-row :gutter="20">
        <el-col
          v-for="item in articleList"
          :key="item.id"
          :xs="24"
          :sm="12"
          :md="8"
          style="margin-bottom: 20px"
        >
          <el-card 
            class="article-card"
            shadow="hover" 
            @click="goToDetail(item.id)"
          >
  
            <!-- 标题 -->
            <h3 style="margin:0 0 10px 0; font-size:18px;">
              {{ item.title }}
            </h3>
  
            <!-- 内容摘要 -->
            <p style="color:#606266; font-size:14px;">
              {{ item.content?.substring(0,50) || '暂无内容' }}
            </p>
  
            <!-- 分类 + 标签 -->
            <div style="margin-top:10px;">
              <span v-if="item.category" style="color:#409EFF; font-weight: bold">
                {{ item.category.name }}
              </span>
              <span v-else>
                未分类
              </span>
  
              <span v-if="item.tags && item.tags.length > 0" style="margin-left:10px;">
                <span v-for="tag in item.tags" :key="tag.id" class="tag">
                  {{ tag.name }}
                </span>
              </span>
            </div>
  
            <!-- 时间 + 按钮 -->
            <div style="margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
              <span style="color:#999; font-size:12px;">
                {{ item.create_time }}
              </span>
  
              <el-button type="primary" text size="small">
                阅读全文 ➔
              </el-button>
            </div>
  
          </el-card>
        </el-col>
      </el-row>
  
      <!-- 分页 -->
      <div style="display:flex; justify-content:center; margin-top:20px;">
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
  import { ApiArticleList, ApiCategoryList } from '../api/article'
  import { useRouter } from 'vue-router'
  import {ElMessage} from 'element-plus'
  
  const loading = ref(false)
  const router = useRouter()
  
  const articleList = ref([])
  const current = ref(1)
  const size = ref(6)
  const total = ref(0)
  
  const categoryList = ref([])
  const activeCategoryId = ref(null)
  
  const getArticleList = async () => {
    loading.value = true
    try {
      const res = await ApiArticleList({
        current: current.value,
        size: size.value,
        category_id: activeCategoryId.value
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
  
  onMounted(() => {
    getArticleList()
    getCategoryList()
  })
  
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
  
  const handleCategoryClick = (categoryId) => {
    activeCategoryId.value = categoryId
    current.value = 1
    getArticleList()
  }
  </script>
  
  <style scoped>
  .tag {
    margin-left: 5px;
    background: #ecf5ff;
    color: #409eff;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 12px;
  }
  
  .article-card {
    cursor: pointer;
    transition: all 0.3s;
    height: 100%;
    display: flex;
    flex-direction: column;
  }
  
  .article-card:hover {
    transform: translateY(-5px);
  }
  </style>