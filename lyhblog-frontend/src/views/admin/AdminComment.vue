<template>
    <h2>评论管理系统</h2>
    <el-table :data="commentList" border>
        <el-table-column prop="id" label="ID" width="60px" />
        <el-table-column prop="article_title" label="所属文章"/>
        <el-table-column prop="username" label="评论用户"/>
        <el-table-column prop="content" label="评论内容"/>
        <el-table-column prop="create_time" label="评论时间"/>
        <el-table-column label="操作">
            <template #default="scope">
                <el-button
                    size="small"
                    type="danger"
                    @click="handleDelete(scope.row.id)"
                >删除</el-button>
            </template>
        </el-table-column>
    </el-table>


    <el-pagination 
        layout="prev,pager,next,total"
        :total="total"
        :page-size="size"
        v-model:current-page="current"
        @current-change="handlePageChange"  
    />

</template>

<script setup>
import {onMounted, ref} from 'vue'

import { ApiAdminCommentList ,ApiAdminCommentDelete} from '../../api/article'
const total = ref(0)
const size = ref(1) //每页几条
const current = ref(1)
const commentList = ref([])


const getCommentList = async () =>{
    const res = await ApiAdminCommentList(
        {   current: current.value,
            size: size.value
        }
    )
    if (res.data.code ==200){
        commentList.value= res.data.data
        total.value= res.data.total
    }
}


onMounted( ()=>{
    getCommentList()
})
const handlePageChange = (newPage) =>{
    current.value= newPage
    getCommentList()
}

const handleDelete = async (id) =>{
    const confirmDelete = confirm('确定删除')
    if(!confirmDelete) return 

    const res = await ApiAdminCommentDelete({id})

    if(res.data.code == 200){
        alert('删除成功')
    }
    if(commentList.value.length===1 && current.value >1 ){
        current.value -= 1
    }
    getCommentList()
}
</script>