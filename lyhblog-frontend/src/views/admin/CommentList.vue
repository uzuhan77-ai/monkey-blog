<template>
    <div>
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
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ApiCommentDelete } from '../../api/comment'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../../utils/request'

const commentList = ref([])

const loadList = async () => {
    const res = await request.get('/comment/all/')
    if (res.data.code == 200) {
        commentList.value = res.data.data
    }
}

const handleDelete = (id) => {
    ElMessageBox.confirm('确定删除这条评论？', '提示', {
        type: 'warning'
    }).then(async () => {
        await ApiCommentDelete(id)
        ElMessage.success('删除成功')
        loadList()
    })
}

onMounted(() => {
    loadList()
})
</script>
