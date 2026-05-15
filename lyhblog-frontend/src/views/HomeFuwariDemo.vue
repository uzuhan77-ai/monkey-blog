<template>
    <div class="home-page">

        <!--顶部导航-->
        <FrontHeader />

        <main class="home-shell">

            <!--左侧栏-->
            <aside class="sidebar">

                <!--个人信息卡-->
                <section class="profile-card">
                    <div>头像占位</div>
                    <h1>博客名</h1>
                    <p>简洁占位</p>

                </section>

                <!--分类-->
                <section>
                    <h2>标签</h2>
                    <button
                        v-for="cat in categoryList"
                        :key="cat.id"
                    >
                    {{ cat.name }}
                </button>
                    <button>分类占位</button>
                </section>

                <!--标签-->
                <section>
                    <h2>标签</h2>
                    <button
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
                    <article>
                        <span>时间</span>
                        <span>分类</span>
                        <h3>文章标题</h3>
                        <p>摘要占位</p>
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
import { ApiCategoryList } from '../api/category'
import { ApiTagList } from '../api/tag'
import { ApiArticleList } from '../api/article'

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