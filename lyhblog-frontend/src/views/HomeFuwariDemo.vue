<template>
    <div class="home-page">

        <!--顶部导航-->
        <FrontHeader />

        <main class="home-shell">

            <!--左侧栏-->
            <FrontSidebar
                :category-list="categoryList"
                :tag-list="labelList"
                :category-id="categoryId"
                :tag-id="tagId"
                @select-category="handleCategoryClick"
                @select-tag="handleTagClick"
            />

            <!--右侧文章区-->
            <section class="content">


                <!--文章列表-->
                <el-skeleton v-if="loading" :rows="6" animated />
                
                <el-empty v-else-if="articleList.length === 0" description="暂无文章" />


                <div class="post-list" v-else>
                    <article
                        v-for="item in articleList"
                        :key="item.id"
                        class="post-card glass-card"
                        @click="goToDetail(item.id)"
                    >
                        <h3>{{ item.title }}</h3>       <!--文章标题-->
                        <div class="post-meta">
                            <span>{{ item.create_time }}</span>              <!--文章发布时间--> 

                            <span v-if="item.category" @click.stop="handleCategoryClick(item.category.id)">
                              {{ item.category.name }}                        <!--文章分类-->
                            </span>

                            <template v-if="item.tags && item.tags.length">
                              <span 
                                v-for="tag in item.tags" 
                                :key="tag.id"
                                @click.stop="handleTagClick(tag.id)"
                              >
                                {{ tag.name }}    <!--文章标签-->
                              </span>
                            </template>
                            <span v-else>无标签</span>

                        </div>

                        <p>{{item.summary || '暂无摘要'}}</p>     <!--文章摘要-->
                    </article>
                </div>

                <!--分页-->
                <div class="pagination-box">
                  <el-pagination
                    background
                    layout="prev,pager,next"
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

<script setup>
import {ref,onMounted,watch} from 'vue'
import { useRouter,useRoute } from 'vue-router'
import { ApiCategoryList } from '../api/category'
import { ApiTagList } from '../api/tag'
import { ApiArticleList } from '../api/article'
import FrontHeader from '../components/FrontHeader.vue'
import FrontSidebar from '../components/FrontSidebar.vue'

const categoryList = ref([]) //分类列表
const labelList = ref([]) //标签列表

const articleList = ref([])
const total = ref(0)
const current = ref(1)
const size = ref(6)
const loading = ref(false)

const categoryId = ref(null)
const tagId = ref(null)
const keyword = ref('')

const router = useRouter()
const route = useRoute()

const goToDetail = (id) =>{
    //用router.push跳转
    //路径是/article
    //id是query参数
    router.push({
        path: '/article',
        query: { id }
    })
}



const getCategoryList = async () =>{
    const res = await ApiCategoryList() //调接口
    categoryList.value =res.data.data 
}

const getLabelList = async () =>{
    const res = await ApiTagList() //调接口
    labelList.value = res.data.data
}

const getArticleList = async () =>{
    loading.value = true   //开始加载，显示骨架
    try{
        const res = await ApiArticleList({
            current: current.value,
            size: size.value,
            category_id: categoryId.value,
            tag_id: tagId.value,
            keyword: keyword.value.trim(),
        })
        console.log('query:', {
        categoryId: categoryId.value,
        tagId: tagId.value,
        total: res.data.total
      })
        articleList.value = res.data.data
        total.value = res.data.total
    }catch(error){
        console.error('文章加载失败',error)
    }finally{
        loading.value = false   //不管成功失败，加载结束
    }
}


const handleCategoryClick = (id) =>{
  categoryId.value = id
  tagId.value = null 
  current.value = 1
  keyword.value = ''
  if(route.query.keyword){
    router.replace({
      path: route.path,
      query: {},
    })}
  getArticleList()
  scrollToArticles()
}

const handleTagClick = (id) =>{
  tagId.value = id
  categoryId.value = null 
  current.value = 1
  keyword.value= '' 
  if(route.query.keyword){
    router.replace({
      path: route.path,
      query: {},  
  })}
  getArticleList()
  scrollToArticles()
}

const handlePageChange =(page) =>{
  current.value = page
  getArticleList()
  scrollToArticles()
}

const scrollToArticles = () =>{
  document.querySelector('.content')?.scrollIntoView({ 
     behavior: 'smooth',
     block: 'start',})
}


onMounted(()=>{
    getCategoryList() //页面挂载完成后自动执行
    getLabelList() 
    if(route.query.keyword){
      keyword.value = String(route.query.keyword)
    }
    getArticleList()
})

watch(
  () => route.query.keyword,
  (newKeyword) => {
    if(!newKeyword) return

    keyword.value = String(newKeyword)
    current.value = 1
    categoryId.value = null
    tagId.value = null

    getArticleList()
    scrollToArticles()
  }
)


</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.78), rgba(246, 250, 255, 0.5)),
    #f6f8fb;
  color: #1f2430;
}

.home-shell {
  width: min(1168px, calc(100% - 48px));
  margin: 0 auto;
  padding: 28px 0 64px;
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr);
  align-items: start;
  gap: 16px;
}

.glass-card {
  border: 1px solid rgba(31, 36, 48, 0.06);
  background: rgba(255, 255, 255, 0.86);
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.035);
  backdrop-filter: blur(16px);
  border-radius: 16px;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.state-card {
  padding: 28px;
}

.post-card {
  position: relative;
  min-height: 138px;
  padding: 26px 78px 24px 36px;
  cursor: pointer;
  overflow: hidden;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    border-color 0.2s ease,
    background 0.2s ease;
}

.post-card.glass-card {
  border-color: rgba(31, 36, 48, 0.045);
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.028);
  border-radius: 16px;
}

.post-card::after {
  content: "›";
  position: absolute;
  top: 12px;
  right: 12px;
  bottom: 12px;
  width: 52px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  background: rgba(47, 141, 244, 0.08);
  color: #2f8df4;
  font-size: 38px;
  line-height: 1;
  opacity: 0.72;
  transition:
    background 0.2s ease,
    opacity 0.2s ease,
    transform 0.2s ease;
}

.post-card:hover {
  transform: translateY(-1px);
  border-color: rgba(47, 141, 244, 0.18);
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 10px 26px rgba(15, 23, 42, 0.06);
}

.post-card:hover::after {
  opacity: 1;
  background: rgba(47, 141, 244, 0.14);
  transform: translateX(2px);
}

.post-meta {
  color: rgba(31, 36, 48, 0.5);
  font-size: 13px;
  line-height: 1.45;
  margin-bottom: 13px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.post-meta span {
  padding: 0;
  border-radius: 0;
  background: transparent;
  color: rgba(31, 36, 48, 0.5);
  font-weight: 500;
}

.post-meta span + span::before {
  content: "/";
  margin-right: 10px;
  color: rgba(31, 36, 48, 0.22);
}

.post-meta span:first-child {
  color: rgba(31, 36, 48, 0.42);
}

.post-meta span:not(:first-child) {
  cursor: pointer;
  transition: color 0.2s ease;
}

.post-meta span:not(:first-child):hover {
  color: #2f8df4;
}

.post-card h3 {
  position: relative;
  margin: 0 0 12px;
  padding-left: 18px;
  padding-right: 10px;
  font-size: 28px;
  line-height: 1.26;
  color: rgba(31, 36, 48, 0.92);
  letter-spacing: 0;
  text-wrap: pretty;
  transition:
    color 0.2s ease,
    transform 0.2s ease;
}

.post-card h3::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.22em;
  width: 4px;
  height: 1.18em;
  border-radius: 999px;
  background: #2f8df4;
}

.post-card:hover h3 {
  color: #2f8df4;
  transform: translateX(2px);
}

.post-card p {
  margin: 0;
  color: rgba(31, 36, 48, 0.66);
  line-height: 1.7;
  font-size: 15px;
  display: -webkit-box;
  overflow: hidden;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  text-wrap: pretty;
}

.pagination-box {
  margin-top: 28px;
  display: flex;
  justify-content: center;
}

.pagination-box :deep(.el-pagination.is-background .el-pager li),
.pagination-box :deep(.el-pagination.is-background button) {
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.035);
  transition:
    background 0.2s ease,
    color 0.2s ease,
    transform 0.2s ease;
}

.pagination-box :deep(.el-pagination.is-background .el-pager li.is-active) {
  background: #2f8df4;
}

.pagination-box :deep(.el-pagination.is-background .el-pager li:hover),
.pagination-box :deep(.el-pagination.is-background button:hover) {
  color: #2f8df4;
  transform: translateY(-1px);
}

@media (max-width: 900px) {
  .home-shell {
    grid-template-columns: 1fr;
    gap: 16px;
  }

}

@media (max-width: 640px) {
  .home-shell {
    width: min(100% - 28px, 1168px);
    padding-top: 22px;
  }

  .post-card {
    min-height: 0;
    padding: 22px 22px 68px;
  }

  .post-card::after {
    top: auto;
    right: 14px;
    bottom: 12px;
    left: 14px;
    width: auto;
    height: 42px;
    font-size: 30px;
  }

  .post-card h3 {
    font-size: 23px;
  }

  .post-card p {
    -webkit-line-clamp: 3;
  }
}
</style>
