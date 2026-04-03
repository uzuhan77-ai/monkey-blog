<template>
    <div class="article-edit">
        <h2>{{ isEdit ? '编辑文章' : '新增文章' }}</h2>

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
                <el-input v-model="form.summary" type="textarea" :rows="3" />
            </el-form-item>

            <el-form-item label="内容">
                <el-input v-model="form.content" type="textarea" :rows="10" />
            </el-form-item>

            <el-form-item>
                <el-button type="primary" @click="handleSubmit">保存</el-button>
                <el-button @click="goBack">取消</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>
<script setup>
import {ref, onMounted, computed} from 'vue'
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)

const form = ref({
    title:'',
    category_id:null,
    tags: [],
    summary:'',
    content:''
})
const categories = ref([])
const tags = ref([])

const loadData = async() =>{
  // 加载分类和标签（需要添加对应接口）
  // 如果是编辑，加载文章数据
}

const handleSubmit = async() =>{
    if(!form.value.title || !form.value.content){
        ElMessage.warning('标题和内容不能为空')
        return
    }
      // 调用新增或编辑接口
      ElMessage.success('保存成功')
      router.push('/admin/article')
}

const goBack = () =>{
    router.back()
}

onMounted(() =>{
    loadData()
})


</script>