<template>
    <div class="detail-page">
      <FrontHeader />
        <main class="detail-shell">
          <el-skeleton v-if="loading" class="article-detail"   :rows="6" animated />

          <el-empty v-else-if="errorMessage" :description="errorMessage" >
            <el-button type="primary" @click="goHome">返回首页</el-button>
          </el-empty>

          <template v-else>
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
          </template>
        </main>

    </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute,useRouter } from 'vue-router'
import { ApiArticleDetail } from '../api/article'
import { ElMessage } from 'element-plus'
import CommentSection from '../components/CommentSection.vue'
import FrontHeader from '../components/FrontHeader.vue'

const route = useRoute()
const article = ref({})

const router = useRouter()
const loading = ref(false)
const errorMessage = ref('')

const getArticle = async () => {
  const id = route.query.id
  if (!id){
    errorMessage.value = '缺少文章id'
    ElMessage.error('缺少文章 id')
    return
  }
  loading.value = true
  errorMessage.value = ''
  try{
    const res = await ApiArticleDetail(id)
    if (res.data.code === 200 && res.data.data) {
      article.value = res.data.data
    }else{
      errorMessage.value = res.data.message || '文章不存在'
      ElMessage.error(errorMessage.value)
    }
  }catch(error){
    errorMessage.value = '文章详情加载失败'
    ElMessage.error('文章详情加载失败')
  }finally{
    loading.value = false
  }
}

const goHome = () => {
  router.push('/')
}


onMounted(() => {
  getArticle()
})
</script>

<style>
.detail-page {
  min-height: 100vh;
  max-width: none;
  margin: 0;
  padding: 0;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(246, 248, 251, 0.74)),
    #f6f8fb;
  color: #1f2430;
}

.detail-shell {
  width: min(900px, calc(100% - 44px));
  margin: 0 auto;
  padding: 28px 0 72px;
}

.article-detail {
  position: relative;
  margin: 0 0 24px;
  padding: 28px 36px 34px;
  border: 1px solid rgba(31, 36, 48, 0.055);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.026);
  backdrop-filter: blur(16px);
  overflow: hidden;
}

.article-detail h1 {
  position: relative;
  margin: 0 0 14px;
  max-width: 760px;
  padding-left: 18px;
  color: rgba(31, 36, 48, 0.94);
  font-size: 36px;
  line-height: 1.22;
  font-weight: 800;
  letter-spacing: 0;
  text-wrap: pretty;
}

.article-detail h1::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.25em;
  width: 4px;
  height: 20px;
  border-radius: 8px;
  background: #2f8df4;
}

.article-detail .meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  color: rgba(31, 36, 48, 0.5);
  font-size: 14px;
  line-height: 1.45;
  margin-bottom: 16px;
}

.article-detail .meta span {
  min-height: 22px;
  display: inline-flex;
  align-items: center;
  color: rgba(31, 36, 48, 0.46);
  font-weight: 600;
}

.article-detail .meta span + span::before {
  content: "/";
  margin-right: 8px;
  color: rgba(31, 36, 48, 0.22);
  font-weight: 500;
}

.article-detail .category {
  color: #2f8df4;
  font-weight: 600;
}

.article-detail .empty-text {
  color: rgba(31, 36, 48, 0.38);
}

.article-detail .tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 22px;
}

.article-detail .tag {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 4px 10px;
  border-radius: 9px;
  background: rgba(47, 141, 244, 0.07);
  color: rgba(47, 111, 171, 0.82);
  font-size: 13px;
  font-weight: 650;
  transition:
    background 0.2s ease,
    color 0.2s ease;
}

.article-detail .tag:hover {
  background: rgba(47, 141, 244, 0.11);
  color: #2f8df4;
}

.article-detail .tag::before {
  content: "#";
  margin-right: 2px;
  color: rgba(47, 141, 244, 0.62);
}

.article-detail .summary {
  position: relative;
  margin: 0 0 26px;
  padding: 15px 18px 15px 22px;
  border-radius: 12px;
  background: rgba(246, 250, 255, 0.64);
  color: rgba(31, 36, 48, 0.62);
  font-size: 15px;
  line-height: 1.74;
  text-wrap: pretty;
}

.article-detail .summary::before {
  content: "";
  position: absolute;
  left: 0;
  top: 15px;
  bottom: 15px;
  width: 4px;
  border-radius: 8px;
  background: #2f8df4;
}

.article-detail .content {
  padding-top: 26px;
  border-top: 1px dashed rgba(31, 36, 48, 0.12);
  white-space: pre-wrap;
  color: rgba(31, 36, 48, 0.74);
  font-size: 17px;
  line-height: 1.94;
  text-wrap: pretty;
}

.article-detail .content :where(p, ul, ol, blockquote, pre, table) {
  margin: 0 0 18px;
}

.article-detail .content :where(h2, h3) {
  margin: 34px 0 14px;
  color: rgba(31, 36, 48, 0.9);
  line-height: 1.35;
  letter-spacing: 0;
}

.article-detail .content h2 {
  position: relative;
  padding-left: 14px;
  font-size: 25px;
}

.article-detail .content h2::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.28em;
  width: 4px;
  height: 1.04em;
  border-radius: 8px;
  background: #2f8df4;
}

.article-detail .content h3 {
  font-size: 20px;
}

.article-detail .content :where(a) {
  color: #2f8df4;
  text-decoration: none;
  border-bottom: 1px solid rgba(47, 141, 244, 0.24);
}

.article-detail .content :where(a:hover) {
  border-bottom-color: rgba(47, 141, 244, 0.72);
}

.article-detail .content :where(blockquote) {
  padding: 15px 18px;
  border-left: 4px solid rgba(47, 141, 244, 0.72);
  border-radius: 0 12px 12px 0;
  background: rgba(47, 141, 244, 0.05);
  color: rgba(31, 36, 48, 0.64);
}

.article-detail .content :where(code) {
  padding: 2px 6px;
  border-radius: 7px;
  background: rgba(31, 36, 48, 0.055);
  color: rgba(31, 36, 48, 0.78);
  font-size: 0.92em;
}

.article-detail .content :where(pre) {
  padding: 16px;
  border-radius: 14px;
  background: rgba(31, 36, 48, 0.92);
  color: rgba(255, 255, 255, 0.9);
  overflow-x: auto;
}

.article-detail .content :where(pre code) {
  padding: 0;
  background: transparent;
  color: inherit;
}

.article-detail .content :where(img) {
  max-width: 100%;
  border-radius: 14px;
  box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
}

.detail-page .comment-section {
  margin: 0;
  padding: 26px;
  border: 1px solid rgba(31, 36, 48, 0.055);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.026);
  backdrop-filter: blur(16px);
}

.detail-page .comment-section h3 {
  position: relative;
  margin: 0 0 18px;
  padding-left: 14px;
  color: rgba(31, 36, 48, 0.9);
  font-size: 18px;
  line-height: 1.3;
}

.detail-page .comment-section h3::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.16em;
  width: 4px;
  height: 1.08em;
  border-radius: 8px;
  background: #2f8df4;
}

.detail-page .login-tip {
  border-radius: 14px;
  background: rgba(47, 141, 244, 0.055);
}

.detail-page .comment-item {
  border-bottom: 1px solid rgba(31, 36, 48, 0.07);
}

.detail-page .username {
  color: #2f8df4;
}

.detail-page .el-empty {
  margin: 28px auto 0;
  padding: 46px 24px;
  border: 1px solid rgba(31, 36, 48, 0.055);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.026);
}

.detail-page .el-empty .el-button {
  border-color: #2f8df4;
  border-radius: 11px;
  background: #2f8df4;
  font-weight: 700;
}

.detail-page .el-skeleton.article-detail {
  min-height: 360px;
}

@media (max-width: 640px) {
  .detail-shell {
    width: min(100% - 28px, 860px);
    padding: 22px 0 56px;
  }

  .article-detail {
    padding: 28px 22px 32px;
  }

  .article-detail h1 {
    font-size: 29px;
  }

  .meta {
    gap: 8px;
  }
}
</style>
