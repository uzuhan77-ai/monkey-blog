<template>
    <div>
        <h1>文章列表</h1>
    </div>
    <div v-for="item in articleList" :key="item.id">
        <h2>{{ item.title }}</h2>
        <p>{{ item.create_time }}</p>
        <button @click="goToDetail(item.id)">查看详情</button>
    </div>
    <el-pagination
        background
        layout="total, prev, pager, next"
        :total="total"
        :page-size="size"
        v-model:current-page="current"
        @current-change="handlePageChange"
    
    />
</template>

<script setup>
import { ref,onMounted } from 'vue'
import { ApiArticleList } from '../api/article'
import {useRouter} from 'vue-router'
const router = useRouter()
const articleList = ref([])
const current = ref(1)
const size = ref(1)
const total = ref(0)
const getArticleList = async () => {
    try{
        const res = await ApiArticleList(
        { current: current.value,
          size: size.value 
        })
        if (res.data.code == 200){
            articleList.value = res.data.data
            total.value = res.data.total
        }
    }
    catch(error){
            console.error(error)
    }
}

onMounted(async () => {
    getArticleList()
})
const handlePageChange = (newPage) => {
    current.value = newPage //更新当前页码
    getArticleList() //重新获取文章列表
}

const goToDetail = (id) => {
    router.push({
        path: '/article',
        query: { id }
    })
}

</script>