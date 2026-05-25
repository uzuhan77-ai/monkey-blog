<template>
    <div class="detail-page">
      <FrontHeader />
        <main class="detail-shell">
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
        </main>

    </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ApiArticleDetail } from '../api/article'
import { ElMessage } from 'element-plus'
import CommentSection from '../components/CommentSection.vue'
import FrontHeader from '../components/FrontHeader.vue'

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
  min-height: 100vh;
  max-width: none;
  margin: 0;
  padding: 0;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.86), rgba(246, 250, 255, 0.48)),
    #f6f8fb;
  color: #1f2430;
}

.detail-shell {
  width: min(900px, calc(100% - 48px));
  margin: 0 auto;
  padding: 30px 0 72px;
}

.article-detail {
  position: relative;
  margin: 0 0 24px;
  padding: 38px 46px 44px;
  border: 1px solid rgba(31, 36, 48, 0.055);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 2px 12px rgba(15, 23, 42, 0.032);
  backdrop-filter: blur(16px);
  overflow: hidden;
}

.article-detail::before {
  content: "";
  position: absolute;
  inset: 0 0 auto;
  height: 4px;
  background: linear-gradient(90deg, #2f8df4, rgba(47, 141, 244, 0.16), transparent 72%);
}

.article-detail h1 {
  position: relative;
  margin: 0 0 18px;
  max-width: 760px;
  padding-left: 18px;
  color: rgba(31, 36, 48, 0.94);
  font-size: 38px;
  line-height: 1.18;
  font-weight: 800;
  letter-spacing: 0;
  text-wrap: pretty;
}

.article-detail h1::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.16em;
  width: 4px;
  height: 1.24em;
  border-radius: 999px;
  background: #2f8df4;
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  color: rgba(31, 36, 48, 0.5);
  font-size: 14px;
  line-height: 1.45;
  margin-bottom: 14px;
}

.meta span {
  min-height: 32px;
  padding: 0 11px;
  border-radius: 10px;
  display: inline-flex;
  align-items: center;
  background: rgba(47, 141, 244, 0.055);
  color: rgba(31, 36, 48, 0.52);
  font-weight: 600;
}

.meta span + span::before {
  content: "";
  width: 0;
  margin: 0;
}

.category {
  color: #2f8df4;
  font-weight: 600;
}

.empty-text {
  color: rgba(31, 36, 48, 0.38);
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 24px;
}

.tag {
  display: inline-flex;
  align-items: center;
  min-height: 30px;
  padding: 5px 11px;
  border-radius: 10px;
  background: rgba(47, 141, 244, 0.08);
  color: rgba(47, 111, 171, 0.88);
  font-size: 13px;
  font-weight: 650;
}

.tag::before {
  content: "#";
  margin-right: 2px;
  color: rgba(47, 141, 244, 0.62);
}

.summary {
  position: relative;
  margin: 0 0 30px;
  padding: 17px 20px 17px 24px;
  border-radius: 14px;
  background: rgba(47, 141, 244, 0.055);
  color: rgba(31, 36, 48, 0.68);
  font-size: 15px;
  line-height: 1.76;
  text-wrap: pretty;
}

.summary::before {
  content: "";
  position: absolute;
  left: 0;
  top: 16px;
  bottom: 16px;
  width: 4px;
  border-radius: 999px;
  background: #2f8df4;
}

.article-detail .content {
  padding-top: 30px;
  border-top: 1px solid rgba(31, 36, 48, 0.07);
  white-space: pre-wrap;
  color: rgba(31, 36, 48, 0.76);
  font-size: 17px;
  line-height: 1.92;
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
  border-radius: 999px;
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
  background: rgba(47, 141, 244, 0.055);
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
  box-shadow: 0 2px 12px rgba(15, 23, 42, 0.032);
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
  border-radius: 999px;
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
