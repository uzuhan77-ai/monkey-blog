<template>
    <div class="detail-page">
         <div class="article-detail">
            <h1>{{ article.title }}</h1>

            <div class="meta">
              <span>{{ article.create_time }}</span>

              <span v-if="article.category" class="category">
                {{ article.category.name }}
              </span>

              <span v-else class="empty-text">
                未分类
              </span>
            </div>

            <div v-if="article.tags && article.tags.length > 0" class="tags">
              <span v-for="tag in article.tags" :key="tag.id" class="tag">
                {{ tag.name }}
              </span>
            </div>

            <div v-if="article.summary" class="summary">
              {{ article.summary }}
            </div>

            <div class="content">
              {{ article.content }}
            </div>
         </div>

         <!-- 评论区 -->
         <CommentSection v-if="article.id" :article-id="article.id" />

    </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ApiArticleDetail } from '../api/article'
import { ElMessage } from 'element-plus'
import CommentSection from '../components/CommentSection.vue'

const route = useRoute()
const article = ref({})

const getArticle = async () => {
  const id = route.query.id
  if (!id){
    ElMessage.error('缺少文章 id')
    return
  }
  try{
    const res = await ApiArticleDetail(id)
    if (res.data.code === 200) {
      article.value = res.data.data
    }
  }catch(error){
    ElMessage.error('文章详情加载失败')
  }
}

onMounted(() => {
  getArticle()
})
</script>

<style>
.detail-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px;
}

.article-detail {
  background: #fff;
  padding: 24px;
  border-radius: 10px;
  margin-bottom: 24px;
}

.meta {
  display: flex;
  gap: 12px;
  align-items: center;
  color: #909399;
  font-size: 14px;
  margin-bottom: 12px;
}

.category {
  color: #409eff;
  font-weight: bold;
}

.empty-text {
  color: #999;
}

.tags {
  margin-bottom: 16px;
}

.tag {
  display: inline-block;
  margin-right: 8px;
  background: #ecf5ff;
  color: #409eff;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.summary {
  padding: 12px;
  background: #f5f7fa;
  color: #606266;
  border-left: 4px solid #409eff;
  margin-bottom: 20px;
}

.content {
  white-space: pre-wrap;
  line-height: 1.8;
  color: #303133;
}

</style>
