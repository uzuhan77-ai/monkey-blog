<template>
    <div class="comment-list">
        <el-table :data="commentList" border>
            <el-table-column prop="id" label="ID" width="80px" />
            <el-table-column prop="username" label="用户" width="120" />
            <el-table-column prop="content" label="评论内容" />
            <el-table-column prop="create_time" label="时间" width="180" />
            <el-table-column label="操作" width="100">
                <template #default="{ row }">
                    <el-button type="danger" text @click="handleDelete(row.id)">
                        删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        
        <div class="pagination-box">
            <el-pagination
                background
                layout="total,prev,pager,next"
                :total="total"
                :page-size="size"
                v-model:current-page="current"
                @current-change="loadList"
            />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ApiCommentDelete,ApiCommentAll } from '../../api/comment'
import { ElMessage, ElMessageBox } from 'element-plus'

const commentList = ref([])
const current = ref(1)
const size = ref(10)
const total = ref(0)

const loadList = async () => {
 try{
    const res = await ApiCommentAll({
        current:current.value,
        size:size.value
    })
    if(res.data.code == 200){
    commentList.value = res.data.data
    total.value = res.data.total
}
 }catch(error){
    ElMessage.error('评论列表加载失败')
 }
}

const handleDelete = (id) => {
    ElMessageBox.confirm('确定删除这条评论？', '提示', {
        type: 'warning'
    }).then(async () => {
        try{
            const res =await ApiCommentDelete(id)
            if (res.data.code === 200) {
            ElMessage.success('删除成功')
            
            const isLastItemOnPage = commentList.value.length === 1
            if(isLastItemOnPage && current.value >1 ){
                current.value -=1
            }


            loadList()
        }
    }catch(error){
        ElMessage.error('删除失败')
    }
    })
}

onMounted(() => {
    loadList()
})
</script>

<style>
.pagination-box {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}
</style>
