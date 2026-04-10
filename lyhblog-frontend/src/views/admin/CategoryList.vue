<template>
    <div class="category-page">
        <div class="toolbar">
            <el-input
                v-model="form.name"
                placeholder="请输入分类名称"
                style="width: 240px"
            />
            <el-button type="primary" @click="handleSubmit">
                {{ form.id ? '保存修改' : '新增分类' }}
            </el-button>
            <el-button v-if="form.id" @click="resetForm">取消编辑</el-button>
        </div>

        <el-table :data="categoryList" border>
            <el-table-column prop="id" label="ID" width="80px" />
            <el-table-column prop="name" label="分类名称" />
            <el-table-column label="操作" width="180">
                <template #default="{row}">
                    <el-button type="primary" text @click="handleEdit(row)">编辑</el-button>
                    <el-button type="danger" text @click="handleDelete(row.id)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {
    ApiCategoryList,
    ApiCategoryAdd,
    ApiCategoryUpdate,
    ApiCategoryDelete
} from '../../api/category'

const categoryList = ref([])

const form = ref({
    id:null,
    name: ''
})
const loadList = async() =>{
    try{
        const res = await ApiCategoryList()
        if(res.data.code == 200){
            categoryList.value = res.data.data
        }
    }catch(error){
        ElMessage.error('分类列表加载失败')
    }
}
const resetForm = () =>{
    form.value ={
        id:null,
        name:''
    }
}
const handleEdit = (row) =>{
    form.value={
        id:row.id,
        name:row.name
    }
}
const handleSubmit = async () =>{
    if(!form.value.name.trim()){
        ElMessage.warning('分类名称不能为空')
        return
    }
    try{
        const res = form.value.id
        ? await ApiCategoryUpdate(form.value)
        : await ApiCategoryAdd(form.value)
        
        if(res.data.code == 200){
            ElMessage.success(form.value.id ? '分类修改成功' : '分类新增成功')
            resetForm()
            loadList()
        }
    }catch(error){
        ElMessage.error(error.response?.data?.message || '操作失败')
    }
}
const handleDelete = (id) =>{
    ElMessageBox.confirm('确定删除这个分类?', '提示', {
        type:'warning'
    })
    .then(async() =>{
        try{
            const res = await ApiCategoryDelete(id)
            if(res.data.code == 200){
                ElMessage.success('分类删除成功')
                loadList()
            }
        }catch(error){
            ElMessage.error(error.response?.data?.message || '删除失败')
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
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}


</style>