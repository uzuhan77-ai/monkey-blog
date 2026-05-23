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
    background:
      linear-gradient(180deg, rgba(255, 255, 255, 0.78), rgba(246, 250, 255, 0.5)),
      #f6f8fb;
    color: #1f2430;
  }
  
  .project-hero,
  .project-section {
    max-width: 1168px;
    margin: 0 auto;
    padding: 28px 24px;
  }
  
  .project-hero {
    display: grid;
    grid-template-columns: 1.3fr 0.9fr;
    gap: 16px;
    align-items: stretch;
  }
  
  .hero-card,
  .module-card,
  .panel-card {
    border: 1px solid rgba(31, 36, 48, 0.06);
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.9);
    box-shadow: 0 2px 12px rgba(15, 23, 42, 0.035);
    backdrop-filter: blur(16px);
  }
  
  .intro-card,
  .status-card,
  .panel-card {
    padding: 30px;
  }

  .intro-card {
    position: relative;
    overflow: hidden;
  }

  .intro-card::before {
    content: "";
    position: absolute;
    inset: 0 0 auto;
    height: 4px;
    background: linear-gradient(90deg, #2f8df4, rgba(47, 141, 244, 0.18), transparent);
  }
  
  .eyebrow {
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 12px;
    color: rgba(47, 111, 171, 0.72);
    font-weight: 700;
  }
  
  .intro-card h1 {
    max-width: 720px;
    margin: 14px 0;
    color: rgba(31, 36, 48, 0.94);
    font-size: 38px;
    line-height: 1.22;
    letter-spacing: 0;
    text-wrap: pretty;
  }
  
  .hero-desc {
    margin: 0;
    max-width: 720px;
    color: rgba(31, 36, 48, 0.64);
    line-height: 1.78;
    text-wrap: pretty;
  }
  
  .hero-actions {
    margin-top: 24px;
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
  }

  .hero-actions :deep(.el-button) {
    min-height: 40px;
    padding: 10px 16px;
    border-radius: 999px;
    font-weight: 600;
  }

  .hero-actions :deep(.el-button--primary) {
    border-color: #2f8df4;
    background: #2f8df4;
    box-shadow: 0 8px 18px rgba(47, 141, 244, 0.16);
  }

  .hero-actions :deep(.el-button.is-plain) {
    border-color: rgba(47, 141, 244, 0.16);
    background: rgba(47, 141, 244, 0.06);
    color: #2f8df4;
  }
  
  .status-grid {
    margin-top: 18px;
    display: grid;
    gap: 12px;
  }
  
  .status-item {
    padding: 16px;
    border: 1px solid rgba(31, 36, 48, 0.05);
    border-radius: 14px;
    background: rgba(47, 141, 244, 0.055);
  }
  
  .status-item span {
    display: block;
    margin-bottom: 8px;
    color: rgba(31, 36, 48, 0.52);
    font-size: 13px;
  }
  
  .status-item strong {
    color: rgba(31, 36, 48, 0.88);
    font-size: 18px;
    line-height: 1.35;
  }
  
  .section-head h2,
  .panel-card h2 {
    margin: 10px 0 0;
    color: rgba(31, 36, 48, 0.92);
    font-size: 28px;
    line-height: 1.28;
  }
  
  .tag-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    padding: 24px;
    border: 1px solid rgba(31, 36, 48, 0.06);
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.9);
    box-shadow: 0 2px 12px rgba(15, 23, 42, 0.035);
  }
  
  .stack-tag {
    min-height: 34px;
    padding: 8px 13px;
    border-radius: 999px;
    background: rgba(47, 141, 244, 0.08);
    color: rgba(47, 111, 171, 0.9);
    font-size: 14px;
    font-weight: 600;
  }
  
  .module-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
  }
  
  .module-card {
    padding: 24px;
    transition:
      transform 0.2s ease,
      box-shadow 0.2s ease,
      border-color 0.2s ease,
      background 0.2s ease;
  }

  .module-card:hover {
    transform: translateY(-2px);
    border-color: rgba(47, 141, 244, 0.18);
    background: rgba(255, 255, 255, 0.96);
    box-shadow: 0 12px 28px rgba(15, 23, 42, 0.07);
  }
  
  .module-card h3 {
    position: relative;
    margin: 0 0 12px;
    padding-left: 15px;
    color: rgba(31, 36, 48, 0.92);
    font-size: 21px;
    line-height: 1.34;
  }

  .module-card h3::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0.3em;
    width: 4px;
    height: 1.05em;
    border-radius: 999px;
    background: #2f8df4;
  }
  
  .module-card p {
    margin: 0 0 16px;
    color: rgba(31, 36, 48, 0.62);
    line-height: 1.75;
    text-wrap: pretty;
  }
  
  .module-card ul,
  .plain-list {
    margin: 0;
    padding-left: 18px;
    color: rgba(31, 36, 48, 0.68);
    line-height: 1.85;
  }
  
  .two-column {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
  }

  .panel-card {
    position: relative;
    overflow: hidden;
  }

  .panel-card::before {
    content: "";
    position: absolute;
    inset: 0 0 auto;
    height: 3px;
    background: rgba(47, 141, 244, 0.2);
  }
  
  @media (max-width: 1024px) {
    .project-hero,
    .two-column,
    .module-grid {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 640px) {
    .project-hero,
    .project-section {
      padding: 22px 14px;
    }

    .intro-card,
    .status-card,
    .panel-card {
      padding: 24px 20px;
    }

    .intro-card h1 {
      font-size: 30px;
    }

    .section-head h2,
    .panel-card h2 {
      font-size: 24px;
    }

    .module-card,
    .tag-wrap {
      padding: 20px;
    }
  }
  </style>
