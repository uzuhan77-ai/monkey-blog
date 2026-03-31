<template>
    <div class="comment-section">
        <h3>评论{{ comments.length }}</h3>

        <!-- 发表评论 -->
        <div v-if="isLogin" class="comment-form">
            <el-input
                v-model="commentContent"
                type="textarea"
                :row="3"
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
                <div class="comment-list">{{ item.content }}</div>
            </div>

            <el-empty v-if="comments.length === 0" description="暂无评论" />
        </div>
    </div>
</template>

<script setup>
import {ref, onMounted, computed} from 'vue'
import {ApiCommentList, ApiCommentAdd} from '../api/comment'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'

const props = defineProps({
    articleId:{
        type:Number,
        require:true
    }
})

const router = usrRouter()
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
        if(!commentContent.vlaue){
            ElMessage.warning('请输入评论内容')
            return
        }
        const res = await ApiCommentAdd({
            article_id:props.articleId,
            content:commentContent.value,
        })
        if(res.data.code=200){
            ElMessage.success('评论成功')
            commentContent.value=''
            loadComments()
        }
    }catch(error){
        ElMessage.success('评论失败')
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
  padding: 20px;
  background: #fff;
  border-radius: 8px;
}

.comment-form {
  margin: 20px 0;
}

.login-tip {
  margin: 20px 0;
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 4px;
}

.comment-item {
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.username {
  font-weight: bold;
  color: #409eff;
}

.time {
  color: #999;
  font-size: 12px;
}

.comment-content {
  color: #606266;
  line-height: 1.6;
}
</style>
```
