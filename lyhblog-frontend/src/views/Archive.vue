<template>
    <div class="archive-page">
        <!--顶部导航-->
        <FrontHeader />

        <!--主题-->
        <main class="archive-shell">
            <!--左侧栏-->
            <FrontSidebar 
                :category-list="categoryList"
                :tag-list="tagList"
                :category-id="categoryId"
                :tag-id="tagId"
                @select-category="handleCategoryClick"
                @select-tag="handleTagClick"
            />

            <!--右侧文章列表-->
            <section class="archive-card">
                <div v-for="group in archiveGroups" :key="group.year">
                    <!--年份行-->
                    <div>{{ group.year }}</div>
                    
                    <!--文章列表-->
                    <article
                        v-for="article in group.articles" 
                        :key="article.id"
                        @click="goToDetail(article.id)">
                        <!--日期-->
                        <div class="archive-date">{{ formatTime(article.create_time) }}</div>

                        <!--标题-->
                        <div class="archive-title">{{ article.title }}</div>

                        <!--标签-->
                        <div class="archive-tags">
                            <span v-for="tag in article.tags" 
                                :key="tag.id"
                                >
                                #{{ tag.name }}
                            </span>
                        </div>
                    </article>
                </div>
            </section>
        </main>
    </div>

</template>

<script setup>
import {computed , onMounted, ref} from 'vue'
import { useRouter } from 'vue-router'
import FrontHeader from '../components/FrontHeader.vue'
import FrontSidebar from '../components/FrontSidebar.vue'
import { ApiCategoryList } from '../api/category'
import { ApiTagList } from '../api/tag'
import { ApiArticleList } from '../api/article'


const router = useRouter()
const categoryList = ref([]) //分类列表
const tagList = ref([]) //标签列表
const articleList = ref([]) //文章列表

const categoryId = ref(null) //当前选中的分类id
const tagId = ref(null) //当前选中的标签id
const loading = ref(false)

const getYear = (value) =>{
    return String(value || '').slice(0,4) 
}

const formatTime = (value) => {
    return String(value || '').slice(5,10)
}

const archiveGroups = computed(() => {
  const map = new Map()

  articleList.value.forEach((article) => {
    const year = getYear(article.create_time)
    if (!map.has(year)) map.set(year, [])
    map.get(year).push(article)
  })

  return Array.from(map.entries())
    .sort(([a], [b]) => Number(b) - Number(a))
    .map(([year, articles]) => ({ year, articles }))
})

// 获取文章列表
const getArticleList = async () => {
  loading.value = true
  try {
    const res = await ApiArticleList({
      current: 1,
      size: 1000,
      category_id: categoryId.value,
      tag_id: tagId.value,
    })
    articleList.value = res.data.data || []
  } catch (error) {
    console.error('加载失败', error)
  } finally {
    loading.value = false   // 加载完成后应该是？
  }
}

// 获取侧边栏数据
const getSidebarData = async () => {
  const categoryRes = await ApiCategoryList()
  const tagRes = await ApiTagList()
  categoryList.value = categoryRes.data.data || []
  tagList.value = tagRes.data.data || []
}

// 点击分类
const handleCategoryClick = (id) => {
  categoryId.value = categoryId.value === id ? null : id  // 如果点的是当前选中的，就取消；否则选中
  tagId.value = null       // 清空标签选中
  getArticleList()
}

// 点击标签
const handleTagClick = (id) => {
  tagId.value = tagId.value === id ? null : id  // 如果点的是当前选中的，就取消；否则选中
  categoryId.value = null
  getArticleList()
}

// 跳转文章详情
const goToDetail = (id) => {
  router.push({
    path: '/article',
    query: { id },
  })
}

onMounted(() => {
    getSidebarData()
    getArticleList()
})
</script>

<style scoped>
.archive-page {
  min-height: 100vh;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.78), rgba(246, 250, 255, 0.52)),
    #f6f8fb;
  color: #1f2430;
}

.archive-shell {
  width: min(1168px, calc(100% - 48px));
  margin: 0 auto;
  padding: 28px 0 64px;
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr);
  align-items: start;
  gap: 16px;
}

.archive-card {
  min-height: 520px;
  padding: 24px 32px 30px;
  border: 1px solid rgba(31, 36, 48, 0.06);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 2px 12px rgba(15, 23, 42, 0.035);
  backdrop-filter: blur(16px);
}

.archive-card > div {
  margin-bottom: 18px;
}

.archive-card > div:last-child {
  margin-bottom: 0;
}

.archive-card > div > div:first-child {
  position: relative;
  height: 60px;
  padding-right: calc(90% + 22px);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  color: rgba(31, 36, 48, 0.76);
  font-size: 26px;
  font-weight: 800;
  line-height: 1;
}

.archive-card > div > div:first-child::before {
  content: "";
  position: absolute;
  left: calc(10% + 2px);
  top: 50%;
  width: 12px;
  height: 12px;
  border: 3px solid rgba(47, 141, 244, 0.28);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.96);
  transform: translate(-50%, -50%);
}

.archive-card > div > div:first-child::after {
  content: "文章";
  position: absolute;
  left: calc(20% + 8px);
  top: 50%;
  color: rgba(31, 36, 48, 0.46);
  font-size: 15px;
  font-weight: 600;
  transform: translateY(-50%);
}

.archive-card article {
  position: relative;
  min-height: 40px;
  display: grid;
  grid-template-columns: 10% minmax(0, 1fr) 18%;
  align-items: center;
  gap: 20px;
  border-radius: 10px;
  color: rgba(31, 36, 48, 0.74);
  cursor: pointer;
  transition:
    background 0.2s ease,
    color 0.2s ease;
}

.archive-card article::before {
  content: "";
  position: absolute;
  left: calc(10% + 1px);
  top: 0;
  bottom: 0;
  border-left: 2px dashed rgba(31, 36, 48, 0.1);
}

.archive-card article::after {
  content: "";
  position: absolute;
  left: calc(10% + 1px);
  top: 50%;
  width: 5px;
  height: 5px;
  border: 4px solid rgba(255, 255, 255, 0.96);
  border-radius: 999px;
  background: rgba(47, 141, 244, 0.42);
  box-shadow: 0 0 0 1px rgba(47, 141, 244, 0.08);
  transform: translate(-50%, -50%);
  transition:
    width 0.2s ease,
    height 0.2s ease,
    background 0.2s ease,
    box-shadow 0.2s ease;
}

.archive-card article:hover {
  background: rgba(47, 141, 244, 0.07);
}

.archive-card article:hover::after {
  width: 7px;
  height: 20px;
  background: #2f8df4;
  box-shadow: 0 0 0 1px rgba(47, 141, 244, 0.16);
}

.archive-date {
  padding-right: 16px;
  color: rgba(31, 36, 48, 0.5);
  font-size: 14px;
  font-weight: 600;
  line-height: 1.2;
  text-align: right;
}

.archive-title {
  min-width: 0;
  padding: 0 8px 0 16px;
  color: rgba(31, 36, 48, 0.76);
  font-size: 16px;
  font-weight: 700;
  line-height: 1.35;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition:
    color 0.2s ease,
    transform 0.2s ease;
}

.archive-card article:hover .archive-title {
  color: #2f8df4;
  transform: translateX(4px);
}

.archive-tags {
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 6px;
  overflow: hidden;
  color: rgba(31, 36, 48, 0.32);
  font-size: 13px;
  line-height: 1.2;
  white-space: nowrap;
}

.archive-tags span {
  overflow: hidden;
  text-overflow: ellipsis;
}

@media (max-width: 900px) {
  .archive-shell {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .archive-shell {
    width: min(100% - 28px, 1168px);
    padding-top: 22px;
  }

  .archive-card {
    padding: 20px 16px 24px;
  }

  .archive-card > div > div:first-child {
    height: 52px;
    padding-right: calc(86% + 16px);
    font-size: 24px;
  }

  .archive-card > div > div:first-child::before,
  .archive-card article::before,
  .archive-card article::after {
    left: calc(14% + 1px);
  }

  .archive-card > div > div:first-child::after {
    left: calc(28% + 8px);
  }

  .archive-card article {
    min-height: 44px;
    grid-template-columns: 14% minmax(0, 1fr);
    gap: 16px;
  }

  .archive-date {
    padding-right: 12px;
    font-size: 13px;
  }

  .archive-title {
    padding-left: 14px;
    font-size: 15px;
  }

  .archive-tags {
    display: none;
  }
}
</style>
