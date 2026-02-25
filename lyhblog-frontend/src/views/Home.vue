<template>
    <div>
        <h1>文章列表</h1>
    </div>
    <div v-for="item in articleList" :key="item.id">
        <h2>{{ item.title }}</h2>
        <p>{{ item.create_time }}</p>
        <button @click="goToDetail(item.id)">查看详情</button>
    </div>
</template>

<script setup>
import { ref,onMounted } from 'vue'
import { ApiArticleList } from '../api/article'
import {useRouter} from 'vue-router'
const router = useRouter()
const articleList = ref([])
onMounted(async () => {
    try{
        const res = await ApiArticleList(
        { current: 1, size: 10 })
        articleList.value = res.data.data
    }
    catch(error){
            console.error(error)
    }
})

const goToDetail = (id) => {
    router.push({
        path: '/article',
        query: { id }
    })
}

</script>