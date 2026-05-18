<template>
    <div class="home-page">

        <!--顶部导航-->
        <FrontHeader />

        <main class="home-shell">

            <!--左侧栏-->
            <aside class="sidebar">

                <!--个人信息卡-->
                <section class="profile-card glass-card">
                  <div class="avatar">LYH</div>

                  <h1>LYH BLOG</h1>

                  <p> 记录AI编程和项目实践.</p>
                </section>

                <!--分类-->
                <section class="glass-card widget-card">
                    <h2>分类</h2>
                    <button class="chip"
                            v-for="cat in categoryList"
                            :key="cat.id"
                            :class="{active:categoryId == cat.id}"
                            @click="handleCategoryClick(cat.id)"
                        >
                        {{ cat.name }}
                    </button>
                </section>

                <!--标签-->
                <section class="glass-card widget-card">
                    <h2>标签</h2>
                    <button class="chip"
                        v-for="label in labelList"
                        :key="label.id"
                        :class="{active:tagId == label.id}"
                        @click="handleTagClick(label.id)"
                    >
                    {{ label.name }}
                  </button>
                </section>

            </aside>

            <!--右侧文章区-->
            <section class="content">

                <!--搜索栏-->
                <div class="content-head">
                    <h2>最新文章</h2>
                </div>

                <!--文章列表-->
                <div class="post-list">
                    <article
                        v-for="item in articleList"
                        :key="item.id"
                        class="post-card glass-card"
                        @click="goToDetail(item.id)"
                    >
                        <div class="post-meta">
                            <span>{{ item.create_time }}</span>
                            <span>{{item.category?.name|| '未分类'}}</span>
                            <span v-if="item.tags && item.tags.length">
                              {{item.tags[0].name}}
                            </span>
                            <span v-else>无标签</span>
                        </div>
                        <h3>{{ item.title }}</h3>
                        <p>{{item.summary || '暂无摘要'}}</p>
                        <div class="post-extra">
                          <span>阅读全文</span>
                        </div>
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
import {ref,onMounted} from 'vue'
import { useRouter } from 'vue-router'
import { ApiCategoryList } from '../api/category'
import { ApiTagList } from '../api/tag'
import { ApiArticleList } from '../api/article'
import FrontHeader from '../components/FrontHeader.vue'

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
        articleList.value = res.data.data
        total.value = res.data.total
    }catch(error){
        console.error('文章加载失败',error)
    }finally{
        loading.value = false   //不管成功失败，加载结束
    }
}

const handleSearch = () =>{
  current.value =1
  getArticleList()
}

const handleCategoryClick = (id) =>{
  categoryId.value = id
  tagId.value = null 
  current.value = 1
  getArticleList()
}

const handleTagClick = (id) =>{
  tagId.value = id
  categoryId.value = null 
  current.value = 1
  getArticleList()
}

const handlePageChange =(page) =>{
  current.value = page
  getArticleList()
}


onMounted(()=>{
    getCategoryList() //页面挂载完成后自动执行
    getLabelList() 
    getArticleList()
})


</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.82), rgba(246, 250, 255, 0.42)),
    #f6f8fb;
  color: #1f2430;
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
  border: 1px solid rgba(31, 36, 48, 0.06);
  background: rgba(255, 255, 255, 0.86);
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.035);
  backdrop-filter: blur(16px);
  border-radius: 16px;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-self: start;
  position: sticky;
  top: 96px;
}

.profile-card {
  padding: 26px 24px;
}

.avatar {
  width: 72px;
  height: 72px;
  border-radius: 18px;
  display: grid;
  place-items: center;
  background: rgba(47, 141, 244, 0.12);
  color: #2f8df4;
  font-weight: 800;
  box-shadow: 0 12px 24px rgba(47, 141, 244, 0.12);
}

.profile-card h1 {
  margin: 24px 0 0;
  color: rgba(31, 36, 48, 0.92);
  font-size: 30px;
  line-height: 1.16;
  letter-spacing: 0.02em;
}

.profile-card p {
  margin: 20px 0 0;
  color: rgba(31, 36, 48, 0.66);
  line-height: 1.75;
}

.widget-card {
  padding: 22px 20px 18px;
}

.widget-card h2 {
  position: relative;
  margin: 0 0 16px;
  padding-left: 12px;
  font-size: 18px;
  line-height: 1.3;
  color: rgba(31, 36, 48, 0.9);
}

.widget-card h2::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.22em;
  width: 4px;
  height: 1em;
  border-radius: 999px;
  background: #2f8df4;
}

.chip {
  margin: 0 8px 10px 0;
  padding: 7px 11px;
  border: 0;
  border-radius: 10px;
  background: rgba(47, 141, 244, 0.08);
  color: rgba(47, 111, 171, 0.92);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.chip:hover,
.chip.active {
  background: rgba(47, 141, 244, 0.14);
  color: #2f8df4;
  transform: translateY(-1px);
}

.widget-card > button:not(.chip) {
  display: none;
}

.content-head {
  margin-bottom: 18px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.state-card {
  padding: 28px;
}

.post-card {
  position: relative;
  padding: 26px 78px 24px 28px;
  cursor: pointer;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.post-card.glass-card {
  border-color: rgba(31, 36, 48, 0.06);
  background: rgba(255, 255, 255, 0.86);
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.035);
  border-radius: 16px;
}

.post-card::after {
  content: "›";
  position: absolute;
  top: 14px;
  right: 14px;
  bottom: 14px;
  width: 52px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  background: rgba(47, 141, 244, 0.08);
  color: #2f8df4;
  font-size: 36px;
  line-height: 1;
  opacity: 0.82;
  transition: background 0.2s ease, opacity 0.2s ease, transform 0.2s ease;
}

.post-card:hover {
  transform: translateY(-2px);
  border-color: rgba(47, 141, 244, 0.18);
  box-shadow: 0 14px 34px rgba(15, 23, 42, 0.08);
}

.post-card:hover::after {
  opacity: 1;
  background: rgba(47, 141, 244, 0.14);
  transform: translateX(2px);
}

.post-meta {
  color: rgba(31, 36, 48, 0.5);
  font-size: 13px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
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

.post-card h3 {
  position: relative;
  margin: 16px 0 12px;
  padding-left: 16px;
  font-size: 26px;
  line-height: 1.38;
  color: rgba(31, 36, 48, 0.92);
  transition: color 0.2s ease;
}

.post-card h3::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.32em;
  width: 4px;
  height: 1.05em;
  border-radius: 999px;
  background: #2f8df4;
}

.post-card:hover h3 {
  color: #2f8df4;
}

.post-card p {
  margin: 0;
  color: rgba(31, 36, 48, 0.66);
  line-height: 1.85;
}

.post-extra {
  margin-top: 18px;
  color: rgba(31, 36, 48, 0.38);
  font-size: 14px;
  font-weight: 500;
}

.post-extra span::after {
  content: " →";
  color: #2f8df4;
  font-weight: 700;
}

.pagination-box {
  margin-top: 26px;
  display: flex;
  justify-content: center;
}
</style>
