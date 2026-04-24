<template>
  <section id="home-article-section" class="article-section">
    <div class="section-head">
      <div>
        <p class="section-label">ARTICLE LIST</p>
        <h2>最新文章</h2>
      </div>
      <p class="section-tip">
        先把内容系统做完整，再继续打磨项目展示和部署能力。
      </p>
    </div>

    <div class="filter-panel">
      <div class="filter-row">
        <span class="filter-title">搜索</span>
        <el-input
          :model-value="keyword"
          class="search-input"
          clearable
          placeholder="输入标题或内容关键词"
          @update:model-value="emit('update:keyword', $event)"
          @keyup.enter="emit('search')"
        />
        <el-button type="primary" @click="emit('search')">搜索</el-button>
        <el-button @click="emit('reset')">重置</el-button>
      </div>

      <div class="filter-row">
        <span class="filter-title">分类</span>
        <el-button
          :type="activeCategoryId === null ? 'primary' : 'default'"
          size="small"
          @click="emit('select-category', null)"
        >
          全部分类
        </el-button>
        <el-button
          v-for="cat in categoryList"
          :key="cat.id"
          :type="activeCategoryId === cat.id ? 'primary' : 'default'"
          size="small"
          @click="emit('select-category', cat.id)"
        >
          {{ cat.name }}
        </el-button>
      </div>

      <div class="filter-row">
        <span class="filter-title">标签</span>
        <el-button
          :type="activeTagId === null ? 'primary' : 'default'"
          size="small"
          @click="emit('select-tag', null)"
        >
          全部标签
        </el-button>
        <el-button
          v-for="tag in tagList"
          :key="tag.id"
          :type="activeTagId === tag.id ? 'primary' : 'default'"
          size="small"
          @click="emit('select-tag', tag.id)"
        >
          {{ tag.name }}
        </el-button>
      </div>
    </div>

    <el-skeleton v-if="loading" :rows="6" animated />

    <el-empty v-else-if="articleList.length === 0" description="暂无文章" />

    <div v-else class="article-grid">
      <article
        v-for="item in articleList"
        :key="item.id"
        class="article-card"
        @click="emit('view-detail', item.id)"
      >
        <div class="article-top">
          <span class="article-category">
            {{ item.category?.name || '未分类' }}
          </span>
          <span class="article-date">{{ item.create_time }}</span>
        </div>

        <h3 class="article-title">{{ item.title }}</h3>
        <p class="article-summary">{{ getArticleSummary(item) }}</p>

        <div class="tag-list">
          <span v-for="tag in item.tags || []" :key="tag.id" class="tag-item">
            {{ tag.name }}
          </span>
        </div>

        <div class="article-footer">
          <span>点击查看详情</span>
          <span class="arrow">→</span>
        </div>
      </article>
    </div>

    <div class="pagination-box">
      <el-pagination
        background
        layout="total, prev, pager, next"
        :total="total"
        :page-size="size"
        :current-page="current"
        @current-change="emit('change-page', $event)"
      />
    </div>
  </section>
</template>

<script setup>
defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
  keyword: {
    type: String,
    default: '',
  },
  categoryList: {
    type: Array,
    default: () => [],
  },
  tagList: {
    type: Array,
    default: () => [],
  },
  activeCategoryId: {
    type: Number,
    default: null,
  },
  activeTagId: {
    type: Number,
    default: null,
  },
  articleList: {
    type: Array,
    default: () => [],
  },
  total: {
    type: Number,
    default: 0,
  },
  size: {
    type: Number,
    default: 6,
  },
  current: {
    type: Number,
    default: 1,
  },
})

const emit = defineEmits([
  'update:keyword',
  'search',
  'reset',
  'select-category',
  'select-tag',
  'change-page',
  'view-detail',
])

const stripHtml = (text = '') => {
  return String(text).replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim()
}

const getArticleSummary = (item) => {
  if (item.summary) {
    return stripHtml(item.summary).slice(0, 90)
  }

  if (item.content) {
    return stripHtml(item.content).slice(0, 90)
  }

  return '暂无文章摘要'
}
</script>

<style scoped>
.article-section {
  max-width: 1180px;
  margin: 0 auto;
  padding: 36px 24px;
}

.section-label {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #7a7366;
}

.section-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
}

.section-head h2 {
  margin: 10px 0 0;
  font-size: 34px;
  line-height: 1.25;
}

.section-tip {
  margin: 0;
  color: #676153;
  line-height: 1.85;
}

.filter-panel,
.article-card {
  border: 1px solid rgba(31, 31, 27, 0.08);
  background: rgba(255, 255, 255, 0.68);
  box-shadow: 0 20px 60px rgba(31, 31, 27, 0.06);
  backdrop-filter: blur(14px);
}

.filter-panel {
  padding: 24px;
  border-radius: 24px;
  margin-bottom: 24px;
}

.filter-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-row + .filter-row {
  margin-top: 14px;
}

.filter-title {
  min-width: 52px;
  color: #373227;
  font-weight: 600;
}

.search-input {
  width: 320px;
}

.article-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
}

.article-card {
  border-radius: 24px;
  padding: 24px;
  cursor: pointer;
  transition: transform 0.22s ease, box-shadow 0.22s ease;
}

.article-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 24px 60px rgba(31, 31, 27, 0.1);
}

.article-top,
.article-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.article-category {
  color: #5d6a59;
  font-weight: 600;
}

.article-date {
  color: #847d70;
  font-size: 13px;
}

.article-title {
  margin: 18px 0 12px;
  font-size: 22px;
  line-height: 1.45;
  color: #1f1f1b;
}

.article-summary {
  margin: 0;
  min-height: 78px;
  color: #5f5a4f;
  line-height: 1.8;
}

.tag-list {
  margin-top: 18px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(111, 127, 106, 0.1);
  color: #5d6a59;
  font-size: 12px;
}

.article-footer {
  margin-top: 22px;
  color: #5d6a59;
  font-size: 14px;
}

.arrow {
  font-size: 18px;
}

.pagination-box {
  margin-top: 28px;
  display: flex;
  justify-content: center;
}

@media (max-width: 1024px) {
  .article-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .article-section {
    padding-left: 16px;
    padding-right: 16px;
  }

  .article-grid {
    grid-template-columns: 1fr;
  }

  .section-head {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-input {
    width: 100%;
  }
}
</style>
