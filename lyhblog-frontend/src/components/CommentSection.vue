<template>
    <div class="comment-section">
        <h3>评论{{ comments.length }}</h3>
        <div class="commment-list">
            <div v-for="item in comments" :key="item.id">
                <div>{{item.username}}</div>
                <div>{{item.content}}</div>
            </div>
        </div>
        <el-input 
            v-model="commentContent"
            type="textarea"
            placeholder="写评论"
        />

        <el-button @click="handleSubmit">提交</el-button>
        


    </div>
</template>

<script setup>
import {ref} from 'vue'
import {ApiCommentList, ApiCommentAdd} from '../api/comment'
import {onMounted} from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'
import { computed } from 'vue'
const comments = ref([])
const commentContent = ref('')
const useStore = useUserStore()
const isLogin = computed(() =>{useStore.isLogin})
const props = defineProps({
    articleId: Number
})

const loadComments = async () =>{
    const res = await ApiCommentList(props.articleId)
    comments.value = res.data.data
}

const handleSubmit = async () =>{
    if(!commentContent.vlaue){
        ElMessage.warning('请输入内容')
        return
    }
    const res = await ApiCommentAdd({
        article_id:props.articleId,
        content:commentContent.value,
    })
    if(res.data.code=200){
        ElMessage.success('评论成功')
        commentContent.value=''
        loadComments
    }
}

onMounted(() =>{
    loadComments()
})

</script>