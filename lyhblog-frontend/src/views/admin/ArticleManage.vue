<template>
    <div>
        <div style="display: flex; justify-content:space-between;align-items:center;">
            <h2>文章管理</h2>
        </div>
        <el-button type="primary" @click="openAddDialog">发布新文章</el-button>
        <el-table :data = "articleList" border>
            <el-table-column prop="id" label="ID" width="60"/>
            <el-table-column prop="title" label="标题" width="160" />
            <el-table-column label="分类" width="160">
                <template #default="scope">
                    <span v-if="scope.row.category">
                        {{ scope.row.category.name }}
                    </span>
                    <span v-else>
                        未定义
                    </span>
                </template>
            </el-table-column>

            <el-table-column prop="create_time" label="创建时间" width="180"/>

            
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button size="small" @click="openEditDialog(scope.row)">编辑</el-button>
                    <el-button 
                        size="small"
                        type="danger"
                        @click="handleDelete(scope.row.id)"
                    >删除
                    </el-button>
                </template>
            </el-table-column>

        </el-table>

        <el-pagination
            layout="total, prev, pager, next"
            :total="total"
            :page-size="size"
            v-model:current-page="current"
            @current-change="handlePageChange"
        />

    </div>

    <el-dialog
        :title="isEdit ?'编辑文章' : '发布新文章'"
        v-model="dialogVisable"
        width="60%"
    >
        <el-form-item label="标题">
            <el-input v-model="formData.title"></el-input>

            <el-input label="分类">
                <el-select v-model="formData.category_id" style="width: 100%;">
                    <el-option
                        v-for="cat in categoryList" 
                        :key="cat.id"
                        :label="cat.name"
                        :value="cat.id"
                        />
                </el-select>
            </el-input>
        </el-form-item>
    
        <el-form-item label="正文">
            <el-input type="textarea" row="8" v-model="formData.content"></el-input>
        </el-form-item>

        <template #footer>
            <el-button @click="dialogVisable= false">取消</el-button>
            <el-button type="primary" @click="saveArticle">保存</el-button>
        </template>
    </el-dialog>
</template>

<script setup>
import { ref,onMounted } from 'vue'
import { ApiArticleList, ApiArticleAdd, ApiArticleDelete, ApiArticleUpdate, ApiCategoryList } from '../../api/article'
// 文章列表
const articleList = ref([])
//  分页
const total = ref(0)   //总条数
const current = ref(1) //当前页
const size = ref(10) //每页条数
// 分类列表
const categoryList = ref([]) //分类下拉数据

const dialogVisable = ref(false)
const isEdit = ref(false)

const formData = ref({
    id: null,
    title: '',
    category_id: null,
    content: '',
})


const getArticleList = async () => {
    try {

        const res = await ApiArticleList({
            current: current.value,
            size: size.value,
        })
        if (res.data.code == 200){
            articleList.value = res.data.data
            total.value = res.data.total
        }
    }catch(error){
        console.error(error)
    }
}

const getCategoryList = async () => {
    try {
        const res = await ApiCategoryList()
        if (res.data.code == 200){
            categoryList.value = res.data.data
        }
    }catch(error){
            console.error(error)
        }
}

const handleDelete = async (id) => {
    const confirmDelete = confirm('确认要删除这篇文章吗？')
    if (!confirmDelete) 
        return 
    try {
        const res = await ApiArticleDelete({
            id: id
        })
        if (res.data.code == 200){
            alert('删除成功')
            getArticleList()
        }
    }catch(error){
        console.error(error)
    }
}

const saveArticle =async () => {
    if(!formData.value.title || !formData.value.content)
        return alert('标题和内容不能为空')
    try{
        let res= null
        
        //判断新增还是编辑
        if(isEdit.value){
            res = await ApiArticleUpdate(formData.value)
        } else{
            res = await ApiArticleAdd(formData.value)
        }
        if(res.data.code == 200){
            alert('保存成功')
            dialogVisable.value = false
            getArticleList()
        }
    }catch (error){
        console.error(error)
    }
}

onMounted( () => {
    getArticleList()
    getCategoryList()
})


const handlePageChange = (newPage) => {
    current.value = newPage
    getArticleList()
}


const openEditDialog = (row) => {
    isEdit.value= true
    formData.value = false

    formData.value={
        id: null,
        title: row.title,
        category_id: row.category_id ? row.category_id : null,
        content: row.content
    }
    dialogVisable.value= true
}

const openAddDialog = () =>{
    isEdit.value=false
    //清空表单
    formData.value= {
        id: null,
        title: '',
        category_id: null,
        content:''
    }
    dialogVisable.value= true
}

</script>