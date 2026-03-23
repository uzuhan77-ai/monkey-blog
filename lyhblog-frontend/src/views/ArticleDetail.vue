<template>
    <div>
        <h1>文章详情页</h1>
    </div>

    <div v-if=" loading">
        正在加载中...
    </div>

    <div v-else-if="article">
        <h1>{{ article.title }}</h1>

        <p>发布时间：{{ article.create_time }}</p>

        <hr>
        <div style="white-space:pre-wrap ;">
            {{ article.content }}
        </div>
        
        <hr>
        <h3>评论{{ commentList.length }}条</h3>
        <!-- 输入评论框 -->
        <div style="margin-top: 20px;" v-if="isLogin">
            <textarea v-model="commentContent"
                placeholder="写下你的评论"
                rows="3"
                style="width: 100%; padding: 8px;"
            ></textarea>
            <div style="margin-top: 10px;">
                <button @click="submitComment">发表评论</button>
            </div>

        </div>

        <div v-if="commentList.length === 0">暂无评论，快来抢沙发吧！</div>

        <div v-for="comment in commentList" :key="comment.id">
            <p>
                <b>{{ comment.username }}</b>
                {{ comment.content }}
            </p>
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