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
                    <el-button type="danger" text @click="handleEdit(row.id)">删除</el-button>
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
    APicategoryUpdate,
    ApicategoryDelete
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
        id:row.id
        name:row.name
    }
}



</script>