<template>
    <div class="project-page">
      <FrontHeader />
  
      <section class="project-hero">
        <div class="hero-card intro-card">
          <p class="eyebrow">PROJECT OVERVIEW</p>
          <h1>lyhblog 前后端分离内容管理系统</h1>
          <p class="hero-desc">
            这是我当前最重要的个人项目，目标不是只做一个能增删改查的博客，
            而是把它打磨成一个可以展示项目思路、前后端能力和后续成长路线的作品。
          </p>
  
          <div class="hero-actions">
            <el-button type="primary" size="large" @click="router.push('/')">
              查看首页
            </el-button>
            <el-button plain size="large" @click="router.push('/admin/article')">
              查看后台
            </el-button>
          </div>
        </div>
  
        <div class="hero-card status-card">
          <p class="eyebrow">CURRENT STATUS</p>
          <div class="status-grid">
            <div class="status-item" v-for="item in statusItems" :key="item.label">
              <span>{{ item.label }}</span>
              <strong>{{ item.value }}</strong>
            </div>
          </div>
        </div>
      </section>
  
      <section class="project-section">
        <div class="section-head">
          <div>
            <p class="eyebrow">TECH STACK</p>
            <h2>当前技术栈</h2>
          </div>
        </div>
  
        <div class="tag-wrap">
          <span v-for="item in techStack" :key="item" class="stack-tag">
            {{ item }}
          </span>
        </div>
      </section>
  
      <section class="project-section">
        <div class="section-head">
          <div>
            <p class="eyebrow">MODULES</p>
            <h2>项目模块拆分</h2>
          </div>
        </div>
  
        <div class="module-grid">
          <article class="module-card" v-for="item in modules" :key="item.title">
            <h3>{{ item.title }}</h3>
            <p>{{ item.description }}</p>
            <ul>
              <li v-for="point in item.points" :key="point">{{ point }}</li>
            </ul>
          </article>
        </div>
      </section>
  
      <section class="project-section two-column">
        <div class="panel-card">
          <p class="eyebrow">COMPLETED</p>
          <h2>当前已完成</h2>
          <ul class="plain-list">
            <li v-for="item in completedList" :key="item">{{ item }}</li>
          </ul>
        </div>
  
        <div class="panel-card">
          <p class="eyebrow">NEXT STEP</p>
          <h2>下一步计划</h2>
          <ul class="plain-list">
            <li v-for="item in nextSteps" :key="item">{{ item }}</li>
          </ul>
        </div>
      </section>
    </div>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router'
  import FrontHeader from '../components/FrontHeader.vue'
  
  const router = useRouter()
  
  const statusItems = [
    { label: '项目定位', value: '全栈内容管理系统' },
    { label: '当前阶段', value: '前台结构升级中' },
    { label: '核心目标', value: '做成可展示项目' },
  ]
  
  const techStack = [
    'Python',
    'Django',
    'Django REST Framework',
    'Vue 3',
    'Vue Router',
    'Pinia',
    'Axios',
    'Element Plus',
    'MySQL',
  ]
  
  const modules = [
    {
      title: '前台展示模块',
      description: '负责文章列表、文章详情、分类筛选、标签筛选和基础内容浏览。',
      points: ['首页文章列表', '分类标签筛选', '文章详情', '评论展示与提交'],
    },
    {
      title: '用户认证模块',
      description: '负责用户登录、注册、Token 认证和基础访问控制。',
      points: ['登录', '注册', 'Token 保存', '后台路由守卫'],
    },
    {
      title: '后台管理模块',
      description: '负责文章、分类、标签和评论的后台管理。',
      points: ['文章新增编辑删除', '评论列表与删除', '分类管理', '标签管理'],
    },
  ]
  
  const completedList = [
    '前台文章列表页',
    '文章详情页',
    '登录注册页',
    '后台文章管理',
    '后台评论管理',
    '后台分类管理',
    '后台标签管理',
  ]
  
  const nextSteps = [
    '优化前台首页结构和视觉层次',
    '增加项目展示页和关于页',
    '清理乱码文本与文案表达',
    '补充 README 与部署文档',
    '后续增加缓存、搜索、部署方案',
  ]
  </script>
  
  <style scoped>
  .project-page {
    min-height: 100vh;
    background: linear-gradient(180deg, #f7f5f0 0%, #eef2ea 100%);
    color: #18231d;
  }
  
  .project-hero,
  .project-section {
    max-width: 1180px;
    margin: 0 auto;
    padding: 40px 24px;
  }
  
  .project-hero {
    display: grid;
    grid-template-columns: 1.3fr 0.9fr;
    gap: 24px;
  }
  
  .hero-card,
  .module-card,
  .panel-card {
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.84);
    border: 1px solid rgba(24, 35, 29, 0.08);
    box-shadow: 0 20px 60px rgba(24, 35, 29, 0.06);
  }
  
  .intro-card,
  .status-card,
  .panel-card {
    padding: 32px;
  }
  
  .eyebrow {
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-size: 12px;
    color: #6b796f;
  }
  
  .intro-card h1 {
    margin: 16px 0;
    font-size: 40px;
    line-height: 1.2;
  }
  
  .hero-desc {
    margin: 0;
    color: #4b5851;
    line-height: 1.8;
  }
  
  .hero-actions {
    margin-top: 24px;
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
  }
  
  .status-grid {
    margin-top: 18px;
    display: grid;
    gap: 14px;
  }
  
  .status-item {
    padding: 18px;
    border-radius: 18px;
    background: #edf4e9;
  }
  
  .status-item span {
    display: block;
    margin-bottom: 8px;
    color: #5e6d64;
    font-size: 13px;
  }
  
  .status-item strong {
    font-size: 20px;
    color: #173e2f;
  }
  
  .section-head h2,
  .panel-card h2 {
    margin: 12px 0 0;
    font-size: 30px;
  }
  
  .tag-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
  }
  
  .stack-tag {
    padding: 10px 16px;
    border-radius: 999px;
    background: #dfe8d8;
    color: #234735;
  }
  
  .module-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 20px;
  }
  
  .module-card {
    padding: 28px;
  }
  
  .module-card h3 {
    margin-top: 0;
    margin-bottom: 12px;
    font-size: 22px;
  }
  
  .module-card p {
    margin: 0 0 16px;
    color: #526059;
    line-height: 1.8;
  }
  
  .module-card ul,
  .plain-list {
    margin: 0;
    padding-left: 18px;
    color: #334139;
    line-height: 1.9;
  }
  
  .two-column {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 20px;
  }
  
  @media (max-width: 1024px) {
    .project-hero,
    .two-column,
    .module-grid {
      grid-template-columns: 1fr;
    }
  }
  </style>