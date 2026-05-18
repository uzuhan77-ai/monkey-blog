<template>
    <div class="home-page">

        <!--顶部导航-->
        <FrontHeader />

        <main class="home-shell">

            <!--左侧栏-->
            <aside class="sidebar">

                <!--个人信息卡-->
                <section class="profile-card glass-card">
                    <div>头像占位</div>
                    <h1>博客名</h1>
                    <p>简洁占位</p>

                </section>

                <!--分类-->
                <section class="glass-card widget-card">
                    <h2>分类</h2>
                    <button class="chip"
                        v-for="cat in categoryList"
                        :key="cat.id"
                    >
                    {{ cat.name }}
                </button>
                    <button>分类占位</button>
                </section>

                <!--标签-->
                <section class="glass-card widget-card">
                    <h2>标签</h2>
                    <button class="chip"
                        v-for="label in labelList"
                        :key="label.id"
                    >
                    {{ label.name }}
                </button>
                </section>

            </aside>

            <!--右侧文章区-->
            <section class="content">

                <!--搜索栏-->
                <div>
                    <h2>最新文章</h2>
                    <input placeholder="搜索文章" />
                    <button>搜索</button>
                </div>

                <!--文章列表-->
                <div>
                    <article
                        v-for="item in articleList"
                        :key="item.id"
                        @click="goToDetail(item.id)"    
                    >
                        <span>{{ item.create_time }}</span>
                        <span>{{item.category?.name|| '未分类'}}</span>
                        <h3>{{ item.title }}</h3>
                        <p>{{item.summary || '暂无摘要'}}</p>
                    </article>
                </div>

                <!--分页-->
                <div>分页占位</div>

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
      linear-gradient(180deg, rgba(255, 255, 255, 0.72), rgba(255, 255, 255, 0.22)),
      #f4f1ea;
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

.content-head {
  margin-bottom: 18px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.post-card {
  padding: 24px;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.post-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 24px 70px rgba(31, 31, 27, 0.1);
}

.post-meta {
  color: #777d73;
  font-size: 13px;
  display: flex;
  gap: 12px;
}

.post-card h3 {
  margin: 14px 0 10px;
  font-size: 24px;
  color: #1d241f;
}

.post-card p {
  color: #62675f;
  line-height: 1.8;
}

.pagination-box {
  margin-top: 26px;
  display: flex;
  justify-content: center;
}
</style>