<template>
    <div class="tag-page">
        <div class="toolbar">
            <el-input
                v-model="form.name"
                placeholder="请输入标签名称"
                style="width: 240px"
            />
            <el-button type="primary" @click="handleSubmit">
                {{ form.id ? '保存修改':'新增标签' }}
            </el-button>
            <el-button v-if="form.id" @click="resetForm">取消编辑</el-button>
        </div>

        <el-table :data="tagList" border>
            <el-table-column prop="id" label="ID" width="80px"/>
            <el-table-column prop="name" label="标签名称" />
            <el-table-column label="操作" width="180px">
                <template #default="{row}">
                    <el-button type="primary" text @click="handleEdit(row)">编辑</el-button>
                    <el-button type="danger" text @click="handleDelete(row.id)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>



<script setup>
import {ref,onMounted} from 'vue'
import {ElMessage,ElMessageBox} from 'element-plus'
import {
    ApiTagList,
    ApiTagAdd,
    ApiTagUpdate,
    ApiTagDelete
} from '../../api/tag'


const tagList=ref([])
const form=ref({
    id:null,
    name:''
})
const loadList = async() =>{
    try{
        const res = await ApiTagList()
        if(res.data.code == 200){
            tagList.value=res.data.data
        }
    }catch(error){
        ElMessage.error('标签列表加载失败')
    }
}
const resetForm = () =>{
    form.value={
        id:null,
        name:''
    }
}
const handleEdit =(row) =>{
    form.value={
        id:row.id,
        name:row.name
    }
}
const handleSubmit = async() =>{
    if(!form.value.name.trim()){
        ElMessage.warning('标签名称不能为空')
        return
    }

    try{
        const res = form.value.id
        ? await ApiTagUpdate(form.value)
        : await ApiTagAdd({name: form.value.name})

        if(res.data.code ==200){
            ElMessage.success(form.value.id ? '标签修改成功' : '标签新增成功')
            resetForm()
            await loadList()
        }
    }catch(error){
        ElMessage.error(error?.response?.data?.message || '操作失败')
    }
}
const handleDelete =(id) =>{
    ElMessageBox.confirm('确定删除这个标签' ,'提示',{
        type: 'warning'
    })
    .then(async() =>{
        try{
            const res = await ApiTagDelete(id)
            if(res.data.code == 200){
                ElMessage.success('标签删除成功')
                loadList()
            }
        }catch(error){
            ElMessage.error(error?.response?.data?.message || '删除失败')
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