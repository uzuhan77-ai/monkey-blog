<template>
    <div>
        <!-- 文章内容 -->
         <div class="article-detail">
            <h1>{{ article.title }}</h1>
            <div class="meta">{{ article.create_time }}</div>
            <div class="content">{{ article.content }}</div>
         </div>

         <!-- 评论区 -->
         <CommentSection v-if="article.id" :article-id="article.id" />

    </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ApiArticleDetail } from '../api/article'
import CommentSection from '../components/CommentSection.vue'

const route = useRoute()
const article = ref({})

const getArticle = async () => {
  const id = route.query.id
  const res = await ApiArticleDetail(id)
  if (res.data.code === 200) {
    article.value = res.data.data
  }
}

onMounted(() => {
  getArticle()
})
</script>
```