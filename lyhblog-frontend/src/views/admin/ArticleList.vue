<template>
    <div class="article-list">
        <div class="toolbar">
            <el-button type="primary" @click="goAdd">新增文章</el-button>
        </div>
    </div>

    <el-table :data="articleList" border>
        <el-table-column prop="id" label="ID" width="80"/>
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="category.name" label="分类" width="120" />
        <el-table-column prop="create_time" label="创建时间" width="180" />
        <el-table-column label="操作" width="180">
            <template #default="{row}">
                <el-button type="primary" text @click="goEdit(row.id)">编辑</el-button>
                <el-button type="primary" text @click="handleDelete(row.id)">删除</el-button>
            </template>
        </el-table-column>
    </el-table>

    <el-pagination
        v-model:current-page="current"
        :page-size="size"
        :total="total"
        @current-change="loadList"
        style="margin-top: 20px"
    />

</template>
<script setup>
import {ref,onMounted} from 'vue'
import {useRouter} from 'vue-router'
import {ApiArticleDelete, ApiArticleList} from '../../api/article'
import {ElMessage, ElMessageBox} from 'element-plus'

const router= useRouter()
const articleList= ref([])
const current = ref(1)
const size = ref(10)
const total = ref(0)

const loadList = async() =>{
    const res = await ApiArticleList({current: current.value, size: size.value})
    if(res.data.code == 200){
        articleList.value = res.data.data
        total.value = res.data.total
    }
}

const goAdd = () =>{
    router.push('/admin/article/add')
}

const goEdit = (id) =>{
    router.push(`/admin/article/edit/${id}`)
}


const handleDelete = (id) =>{
    ElMessageBox.confirm('确定删除这篇文章?', '提示',{
        type: 'warning'
    })
    .then(async() =>{
        try{
            const res = await ApiArticleDelete(id)

            if(res.data.code == 200){
                ElMessage.success('删除成功')
                await loadList()
            }
        }catch(error){
            ElMessage.error('删除失败')
        }
    })
    .catch(() =>{})
}

onMounted(() =>{
    loadList()
})
</script>

<style scoped>
.toolbar {
  margin-bottom: 20px;
}
</style>
