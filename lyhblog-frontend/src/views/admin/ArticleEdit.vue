<template>
    <div class="article-edit">
        <div class="page-header">
            <h2>{{ isEdit ? '编辑文章' : '新增文章' }}</h2>
            <el-button type="primary" plain @click="aiDrawerVisable=true">
                AI 助手
            </el-button>
        </div>

        <el-form :model="form" label-width="80px">
            <el-form-item label="标题">
                <el-input v-model="form.title" placeholder="请输入标题"/>
            </el-form-item>

            <el-form-item label="分类">
                <el-select v-model="form.category_id" placeholder="请选择分类">
                    <el-option
                        v-for="cat in categories"
                        :key="cat.id"
                        :label="cat.name"
                        :value="cat.id"
                    />
                </el-select>
            </el-form-item>

            <el-form-item label="标签">
                <el-select v-model="form.tags" multiple placeholder="请选择标签">
                    <el-option
                        v-for="tag in tags"
                        :key="tag.id"
                        :label="tag.name"
                        :value="tag.id"
                    />
                </el-select>
            </el-form-item>

            <el-form-item label="摘要">
                <el-input v-model="form.summary" type="textarea" :rows="4" />
            </el-form-item>

            <el-form-item label="内容">
                <el-input v-model="form.content" type="textarea" :rows="10" />
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="handleSubmit">保存</el-button>
                <el-button @click="goBack">取消</el-button>
            </el-form-item>
        </el-form>

        <AIAssistantDrawer
            v-model="aiDrawerVisable"
            :article-form="form"
            @apply="handleApplyAiResult"
        />
    </div>
</template>
<script setup>
import {ref, onMounted, computed} from 'vue'
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import {ApiArticleAdd, ApiArticleDetail, ApiArticleUpdate, ApiCategoryList, ApiTagList} from '../../api/article'
import AIAssistantDrawer from '../../components/admin/AIAssistantDrawer.vue';


const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)
const aiDrawerVisable = ref(false)

const form = ref({
    title:'',
    category_id:null,
    tags: [],
    summary:'',
    content:''
})
const categories = ref([])
const tags = ref([])

const loadOptions = async() =>{
    try{
        const [categoryRes, tagRes] =await Promise.all([
            ApiCategoryList(),
            ApiTagList()
        ])

        if(categoryRes.data.code ==200){
            categories.value = categoryRes.data.data
        }
        if(tagRes.data.code == 200){
            tags.value = tagRes.data.data
        }
    }catch(error) {
        ElMessage.error('分类或标签加载失败')
    }
}

const loadArticleDetail = async ()=>{
    if(!isEdit.value) return 
    try{
        const res = await ApiArticleDetail(route.params.id)
        if(res.data.code == 200){
            const article = res.data.data

            form.value = {
                title: article.title || '',
                category_id : article.category?.id || null,
                tags: article.tags ? article.tags.map((item) =>item.id) : [],
                summary: article.summary || '',
                content: article.content || '',
            }
        }
    }catch(error){
        ElMessage.error('文章详情加载失败')
    }
}

const handleApplyAiResult =(payload) =>{
    if (typeof payload.title === "string") {
    form.value.title = payload.title;
  }
  if (typeof payload.summary === "string") {
    form.value.summary = payload.summary;
  }
  if (payload.category_id !== undefined && payload.category_id !== null) {
    form.value.category_id = payload.category_id;
  }
  if (Array.isArray(payload.matched_tag_ids) && payload.matched_tag_ids.length) {
    form.value.tags = [...new Set(payload.matched_tag_ids)];
  }
  if (typeof payload.content === "string" && payload.content.trim()) {
    form.value.content = payload.content;
  }

  ElMessage.success("AI 建议已应用到表单");
}

const handleSubmit = async() =>{
    if(!form.value.title || !form.value.content){
        ElMessage.warning('标题和内容不能为空')
        return
    }

    try{
        if(isEdit.value){
            const res = await ApiArticleUpdate({
                id : route.params.id,
                ...form.value
            })
            if(res.data.code == 200){
                ElMessage.success('文章修改成功')
                router.push('/admin/article')
            }
        }else{
            const res = await ApiArticleAdd(form.value)

            if(res.data.code == 200){
                ElMessage.success('文章新增成功')
                router.push('/admin/article')
            }
        }
    }catch(error){
        ElMessage.error(isEdit.value ? '文章修改失败' :'文章新增失败')
    }
}

const goBack = () =>{
    router.back()
}

onMounted(async ()=>{
    await loadOptions()
    await loadArticleDetail()
})


</script>