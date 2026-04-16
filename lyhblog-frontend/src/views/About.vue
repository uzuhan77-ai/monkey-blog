<template>
    <div class="about-page">
      <FrontHeader />
  
      <section class="about-hero">
        <div class="hero-main">
          <p class="eyebrow">ABOUT ME</p>
          <h1>关于这个项目，也关于现在的我</h1>
          <p class="hero-desc">
            我现在正通过 `lyhblog` 这个项目，系统地练习 Django + Vue 的前后端分离开发。
            现阶段目标不是假装自己已经是成熟工程师，而是先把一个完整项目真正做完、讲清楚、跑起来。
          </p>
        </div>
  
        <div class="hero-side">
          <p class="eyebrow">CURRENT FOCUS</p>
          <ul class="focus-list">
            <li v-for="item in currentFocus" :key="item">{{ item }}</li>
          </ul>
        </div>
      </section>
  
      <section class="about-section two-column">
        <div class="panel-card">
          <p class="eyebrow">PROFILE</p>
          <h2>当前定位</h2>
          <div class="info-list">
            <div class="info-item" v-for="item in profileInfo" :key="item.label">
              <span>{{ item.label }}</span>
              <strong>{{ item.value }}</strong>
            </div>
          </div>
        </div>
  
        <div class="panel-card">
          <p class="eyebrow">SKILLS</p>
          <h2>当前掌握的技术</h2>
          <div class="tag-wrap">
            <span v-for="item in skills" :key="item" class="skill-tag">{{ item }}</span>
          </div>
        </div>
      </section>
  
      <section class="about-section two-column">
        <div class="panel-card">
          <p class="eyebrow">ROADMAP</p>
          <h2>接下来要补的能力</h2>
          <ul class="plain-list">
            <li v-for="item in nextPlan" :key="item">{{ item }}</li>
          </ul>
        </div>
  
        <div class="panel-card">
          <p class="eyebrow">CONTACT</p>
          <h2>项目信息</h2>
          <ul class="plain-list">
            <li>项目名：lyhblog</li>
            <li>项目形态：前后端分离内容管理系统</li>
            <li>当前方向：先完成 blog，再延伸到 Python 后端 / 爬虫方向</li>
            <li>仓库地址：后续补充到 GitHub</li>
          </ul>
        </div>
      </section>
    </div>
  </template>
  
  <script setup>
  import FrontHeader from '../components/FrontHeader.vue'
  
  const currentFocus = [
    '完成前台结构升级',
    '把项目做成可展示作品',
    '补齐项目文档与部署说明',
    '为后续 Python 后端 / 爬虫方向打基础',
  ]
  
  const profileInfo = [
    { label: '当前阶段', value: '项目学习者' },
    { label: '主线技术栈', value: 'Django + Vue' },
    { label: '当前目标', value: '做完并包装好 lyhblog' },
  ]
  
  const skills = [
    'Python',
    'Django',
    'Django REST Framework',
    'Vue 3',
    'Vue Router',
    'Pinia',
    'Axios',
    'Element Plus',
    'MySQL 基础',
    'Git / GitHub 基础',
  ]
  
  const nextPlan = [
    '继续完善前后台 CRUD 闭环',
    '清理乱码文案和项目表达',
    '补充 README、截图和 API 说明',
    '补充部署故事：Nginx、Docker、云服务器',
    '后续单独做一个小型爬虫 / 数据管理项目',
  ]
  </script>
  
  <style scoped>
  .about-page {
    min-height: 100vh;
    background: linear-gradient(180deg, #f7f5f0 0%, #eef2ea 100%);
    color: #18231d;
  }
  
  .about-hero,
  .about-section {
    max-width: 1180px;
    margin: 0 auto;
    padding: 40px 24px;
  }
  
  .about-hero {
    display: grid;
    grid-template-columns: 1.25fr 0.9fr;
    gap: 24px;
  }
  
  .hero-main,
  .hero-side,
  .panel-card {
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.84);
    border: 1px solid rgba(24, 35, 29, 0.08);
    box-shadow: 0 20px 60px rgba(24, 35, 29, 0.06);
    padding: 32px;
  }
  
  .eyebrow {
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-size: 12px;
    color: #6b796f;
  }
  
  .hero-main h1,
  .panel-card h2 {
    margin: 16px 0 0;
    font-size: 38px;
    line-height: 1.2;
  }
  
  .hero-desc {
    margin-top: 18px;
    color: #4b5851;
    line-height: 1.9;
  }
  
  .focus-list,
  .plain-list {
    margin: 18px 0 0;
    padding-left: 18px;
    line-height: 1.9;
    color: #334139;
  }
  
  .two-column {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 20px;
  }
  
  .info-list {
    margin-top: 18px;
    display: grid;
    gap: 14px;
  }
  
  .info-item {
    padding: 18px;
    border-radius: 18px;
    background: #edf4e9;
  }
  
  .info-item span {
    display: block;
    color: #5e6d64;
    font-size: 13px;
    margin-bottom: 8px;
  }
  
  .info-item strong {
    font-size: 20px;
    color: #173e2f;
  }
  
  .tag-wrap {
    margin-top: 18px;
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
  }
  
  .skill-tag {
    padding: 10px 16px;
    border-radius: 999px;
    background: #dfe8d8;
    color: #234735;
  }
  
  @media (max-width: 1024px) {
    .about-hero,
    .two-column {
      grid-template-columns: 1fr;
    }
  }
  </style>