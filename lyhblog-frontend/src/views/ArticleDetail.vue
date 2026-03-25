<template>
    <div>
        <h1>文章详情页</h1>
    </div>

    <div style="max-width: 800px; margin: 0 auto; padding: 20px;">
        <div v-if="loading" style="text-align: center; padding : 50px">
            <p style="font-size: 18px;"> 文章加载中..</p>
        </div>

        <div v-else-if="article">
            <h1 style="text-align: center; color: #303133; margin-bottom: 20px;">{{ article.title }}</h1>
            <div style="text-align: center; color: #909399; 
                font-size: 14px; margin-bottom: 30px;
                background: #f4f4f5; padding: 10px; border-radius: 6px;">
                <span> 发布时间:{{ article.create_time }}</span>
            </div>
            

            <div style="white-space:pre-wrap ;">
                {{ article.content }}
            </div>
            
            <hr>
            <h3>评论{{ commentList.length }}条</h3>
            <!-- 输入评论框 -->
            <div style="margin-top: 20px;" v-if="isLogin">
                <el-input
                    v-model="commentContent"
                    type="textarea"
                    :rows="3"
                    placeholder="写下你的评论吧..."
                    maxlength="200"
                    show-word-limit
                />
                    <div style="text-align: right; margin-top: 10px;">
                        <el-button type="primary" @click="submitComment">发表评论</el-button>
                    </div>
            </div>
            
                <!-- 未登录提示 -->
            <div v-if="!isLogin" style="text-align: center; padding: 20px; background: #f4f4f5; border-radius: 8px; color: #606266; margin-top: 20px;">
                <p>请先 
                    <el-link type="primary" @click="router.push('/login')">登录</el-link> 
                    后发表评论
                </p>
            </div>

            <el-empty v-if="commentList.length === 0"
                description="还没有人评论，快来抢沙发"
                :image-size="80"
            />

            <div v-for="comment in commentList" :key="comment.id"
                style="padding: 15px 0; border-bottom: 1px dashed #ebeef5;">
                <!-- <p>
                    <b>{{ comment.username }}</b>
                    {{ comment.content }}
                </p> -->
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <el-avatar :size="32" style="background:#409EFF">
                        {{ comment.username.charAt(0).toUpperCase() }}
                    </el-avatar>
                    <span style="font-weight: bold; margin: 0 10px;">{{ comment.username }}</span>
                    <span style="font-size: 12px; color: #909399;">{{ comment.create_time }}</span>
                </div>
                <div style="margin-left: 42px; color: #606266; line-height: 1.5;">
                        {{ comment.content }}
                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
import {ref, onMounted} from 'vue'
import { useRoute,useRouter} from 'vue-router'
import { ApiArticleDetail, ApiCommentList, ApiCommentAdd } from '../api/article'
import {ElMessage} from 'element-plus'

const route = useRoute()
const router = useRouter()
const isLogin = ref(false)

const article = ref(null)
const loading = ref(true)
const commentList = ref([])
const commentContent = ref('')



onMounted(async () => {
    const id = route.query.id
    // 检查登录状态
    if( localStorage.getItem('user_token')){
        isLogin.value = true
    }

    try{
        const res = await ApiArticleDetail({
            id: id
        })
        if (res.data.code === 200){
            article.value = res.data.data
        }

        const commentRes = await ApiCommentList({
            article_id: id
        })
        if (commentRes.data.code === 200){
            commentList.value = commentRes.data.data
        }
    }catch(error){
        console.error('获取失败', error)
    }finally{
        loading.value = false
    }
})

const submitComment = async () =>{
    // 检查登录
    if(!isLogin.value){
        ElMessage.warning('请先登录')
        router.push('/login')
        return
    }


    // 检查是否输入内容
    if (!commentContent.value.trim()){
        ElMessage.warning('评论不能为空')
        return
    }
    try{
        // 调用发表评论接口
        const res = await ApiCommentAdd({
            article_id: article.value.id,
            content: commentContent.value
        })
        if (res.data.code === 200){
            ElMessage.success('评论成功')
            // 清空输入框
            commentContent.value = ''

            // 重新获取评论列表
            const commentRes = await ApiCommentList({
                article_id: route.query.id
            })
            if (commentRes.data.code === 200){
                commentList.value = commentRes.data.data
            }
            
        }
    }catch(error){
        console.error('发表评论失败', error)
        ElMessage.error('评论失败，请稍后再试')
    }
}




</script>