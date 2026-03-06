<template>
    <div>
        <h1>文章列表</h1>
    </div>
    <div v-for="item in articleList" :key="item.id"
        style=" margin-bottom: 30px; border-bottom: 1px dashed #ccc; padding-bottom: 10px;">
        <h2>{{ item.title }}</h2>
        <div>
            <!-- 分类栏 -->
            <span v-if="item.category" style="color:#409Eff; font-weight: bold">
                分类: {{ item.category.name }}
            </span>
            <span v-else>
                分类: 未分类
            </span>
            <!-- 标签栏 -->
            <span v-if="item.tags && item.tags.length >0" style="margin-left:15px; ">
                标签:
                <span v-for="tag in item.tags" :key="tag.id" 
                    style= "margin-left: 5px; background: #f0f9eb; color:#409Efe;
                     padding: 2px 6px; border-radius: 4px; border: 1px solid #e1f3d8;""
                >
                    {{ tag.name }}
                </span>
            </span>
        </div>

        <p>{{ item.create_time }}</p>
        <button @click="goToDetail(item.id)">查看详情</button>
    </div>
    <el-pagination
        background
        layout="total, prev, pager, next"
        :total="total"
        :page-size="size"
        v-model:current-page="current"
        @current-change="handlePageChange"
    
    />
</template>

<script setup>
import { ref,onMounted } from 'vue'
import { ApiArticleList, ApiCategoryList } from '../api/article'
import {useRouter} from 'vue-router'
const router = useRouter()
const articleList = ref([])
const current = ref(1)
const size = ref(1)
const total = ref(0)

const categoryList = ref([]) //分类列表
const activeCategoryId = ref(null) //当前选中的分类
const getArticleList = async () => {
    try{
        const res = await ApiArticleList(
        { current: current.value,
          size: size.value,
          category_id: activeCategoryId.id
        })
        if (res.data.code == 200){
            articleList.value = res.data.data
            total.value = res.data.total
        }
    }
    catch(error){
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

onMounted(async () => {
    getArticleList()
    getCategoryList()
})
const handlePageChange = (newPage) => {
    current.value = newPage //更新当前页码
    getArticleList() //重新获取文章列表
}

const goToDetail = (categoryId) => {
    router.push({
        path: '/article',
        query: { id }
    })
}

</script>