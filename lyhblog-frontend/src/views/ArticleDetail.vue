<template>
    <div>
        <h1>文章详情页</h1>
    </div>

    <div v-if=" loading">
        正在加载中...
    </div>

    <div v-else-if="article">
        <h1>{{ article.title }}</h1>

        <P>发布时间：{{ article.create_time }}</P>

        <hr>
        <div style="white-space:pre-wrap ;">
            {{ article.content }}
        </div>
    </div>

</template>

<script setup>
import {ref, onMounted} from 'vue'
import { useRoute} from 'vue-router'
import { ApiArticleDetail } from '../api/article'

const route = useRoute()

const article = ref(null)
const loading = ref(true)


onMounted(async () => {
    const id = route.query.id

    try{
        const res = await ApiArticleDetail({id: id})
        console.log('详情数据：', res.data)

        article.value = res.data.data
    }catch(error){
        console.error('获取失败', error)
    }finally{
        loading.value = false
    }
})




</script>