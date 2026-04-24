<template>
  <section class="project-section">
    <div class="project-copy">
      <p class="section-label">PROJECT NOTE</p>
      <h2>现在的重点不是扩功能，而是把博客体验做扎实</h2>
      <p class="project-desc">
        这个项目当前聚焦首页、文章详情、分类标签和后台管理，
        先把它做成一套完整、可展示、可持续迭代的内容系统。
      </p>
    </div>

    <div class="project-grid">
      <article v-for="item in highlights" :key="item.title" class="project-card">
        <h3>{{ item.title }}</h3>
        <p>{{ item.desc }}</p>
      </article>
    </div>
  </section>
</template>

<script setup>
defineProps({
  highlights: {
    type: Array,
    default: () => [],
  },
})
</script>

<style scoped>
.project-section {
  max-width: 1180px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 0.95fr 1.05fr;
  gap: 20px;
  padding: 8px 24px 60px;
}

.section-label {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #7a7366;
}

.project-copy {
  padding: 8px 0;
}

.project-copy h2 {
  margin: 10px 0 0;
  font-size: 34px;
  line-height: 1.25;
}

.project-desc {
  margin: 16px 0 0;
  color: #676153;
  line-height: 1.85;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.project-card {
  border: 1px solid rgba(31, 31, 27, 0.08);
  border-radius: 24px;
  padding: 24px;
  background: rgba(255, 255, 255, 0.68);
  box-shadow: 0 20px 60px rgba(31, 31, 27, 0.06);
  backdrop-filter: blur(14px);
}

.project-card h3 {
  margin: 0 0 12px;
  font-size: 20px;
  line-height: 1.4;
}

.project-card p {
  margin: 0;
  color: #645e52;
  line-height: 1.8;
}

@media (max-width: 1024px) {
  .project-section,
  .project-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .project-section {
    padding-left: 16px;
    padding-right: 16px;
  }
}
</style>
