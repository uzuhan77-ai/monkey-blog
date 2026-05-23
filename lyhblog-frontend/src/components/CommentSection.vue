<template>
    <div class="comment-section">
        <h3>评论{{ comments.length }}</h3>

        <!-- 发表评论 -->
        <div v-if="isLogin" class="comment-form">
            <el-input
                v-model="commentContent"
                type="textarea"
                :rows="3"
                placeholder="writedown your comments"
            />
            <el-button
                type="primary"
                @click="handleSubmit"
                :loading="submitting"
                style="margin-top: 10px;"
            >
                发表评论
            </el-button>
        </div>
        <div v-else class="login-tip">
            <el-button type="primary" text @click="goLogin">
                登录后发表评论
            </el-button>
        </div>


        <!-- 评论列表 -->
        <div class="commment-list">
            <div v-for="item in comments" :key="item.id" class="comment-item">
                <div class="comment-header">
                    <span class="username">{{ item.username }}</span>
                    <span class="time">{{ item.create_time }}</span>
                </div>
                <div class="comment-content">{{ item.content }}</div>
            </div>

            <el-empty v-if="comments.length === 0" description="暂无评论" />
        </div>
    </div>
</template>

<script setup>
import {ref, onMounted, computed} from 'vue'
import { useRouter } from 'vue-router'
import {ApiCommentList, ApiCommentAdd} from '../api/comment'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'

const props = defineProps({
    articleId:{
        type:Number,
        required:true
    }
})

const router = useRouter()
const useStore = useUserStore()
const isLogin = computed(() => useStore.isLogin)



const comments = ref([])
const commentContent = ref('')
const submitting = ref(false)


const loadComments = async () =>{
    try{
        const res = await ApiCommentList(props.articleId)
        if(res.data.code==200){
            comments.value= res.data.data
        }
    }catch(error){
        console.error(error)
    }
}

const handleSubmit = async () =>{
    try{
        if(!commentContent.value.trim()){
            ElMessage.warning('请输入评论内容')
            return
        }
        const res = await ApiCommentAdd({
            article_id:props.articleId,
            content:commentContent.value,
        })
        if(res.data.code==200){
            ElMessage.success('评论成功')
            commentContent.value=''
            loadComments()
        }
    }catch(error){
        ElMessage.error('评论失败')
    }finally{
        submitting.value = false
    }
}
const goLogin = () =>{
    router.push('/login')
}
onMounted(() =>{
    loadComments()
})

</script>



<style scoped>
.comment-section {
  margin-top: 40px;
  padding: 24px;
  border: 1px solid rgba(31, 36, 48, 0.06);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 2px 12px rgba(15, 23, 42, 0.035);
  backdrop-filter: blur(16px);
}

.comment-section h3 {
  margin: 0 0 18px;
  color: rgba(31, 36, 48, 0.9);
  font-size: 18px;
  line-height: 1.3;
  font-weight: 700;
}

.comment-form {
  margin: 18px 0 22px;
}

.comment-form :deep(.el-textarea__inner) {
  min-height: 104px;
  border-color: rgba(31, 36, 48, 0.08);
  border-radius: 14px;
  background: rgba(246, 250, 255, 0.62);
  color: rgba(31, 36, 48, 0.78);
  line-height: 1.7;
  box-shadow: none;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    background 0.2s ease;
}

.comment-form :deep(.el-textarea__inner:focus) {
  border-color: rgba(47, 141, 244, 0.24);
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.055);
}

.comment-form :deep(.el-button) {
  min-height: 36px;
  padding: 8px 16px;
  border: 0;
  border-radius: 999px;
  background: #2f8df4;
  box-shadow: 0 8px 18px rgba(47, 141, 244, 0.18);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    background 0.2s ease;
}

.comment-form :deep(.el-button:hover) {
  background: #267fdf;
  box-shadow: 0 10px 24px rgba(47, 141, 244, 0.22);
  transform: translateY(-1px);
}

.login-tip {
  margin: 18px 0 22px;
  text-align: center;
  padding: 22px;
  border-radius: 14px;
  background: rgba(47, 141, 244, 0.055);
  color: rgba(31, 36, 48, 0.58);
}

.login-tip :deep(.el-button) {
  color: #2f8df4;
  font-weight: 600;
}

.commment-list {
  display: flex;
  flex-direction: column;
}

.comment-item {
  padding: 16px 0;
  border-bottom: 1px solid rgba(31, 36, 48, 0.07);
}

.comment-item:first-child {
  padding-top: 4px;
}

.comment-item:last-child {
  border-bottom: 0;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
}

.username {
  color: #2f8df4;
  font-size: 14px;
  font-weight: 700;
}

.time {
  color: rgba(31, 36, 48, 0.4);
  font-size: 12px;
  line-height: 1.6;
}

.comment-content {
  color: rgba(31, 36, 48, 0.68);
  line-height: 1.75;
  text-wrap: pretty;
}

@media (max-width: 640px) {
  .comment-section {
    padding: 20px 18px;
  }

  .comment-header {
    flex-direction: column;
    gap: 2px;
  }
}
</style>
