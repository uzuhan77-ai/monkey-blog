<template>
  <section class="hero-section">
    <div class="hero-video-panel">
      <div class="hero-media">
        <video
          v-if="!videoError"
          class="hero-video"
          :src="heroVideoSrc"
          autoplay
          muted
          loop
          playsinline
          @error="handleVideoError"
        ></video>

        <div v-else class="hero-video-placeholder">
          <span>这里后续替换为项目录屏视频</span>
        </div>

        <div class="hero-media-mask"></div>
      </div>

      <div class="hero-overlay">
        <p class="hero-label">LYHBLOG / PERSONAL CONTENT SYSTEM</p>
        <h1 class="hero-title">把 blog 做成一个真正可展示的项目</h1>
        <p class="hero-desc">
          用 Django 与 Vue 搭建前后端分离的内容系统，记录学习、沉淀内容，
          也把它当成我的工程作品。
        </p>

        <div class="hero-actions">
          <el-button type="primary" size="large" @click="emit('view-articles')">
            查看文章
          </el-button>
          <el-button plain size="large" @click="emit('view-project')">
            查看项目
          </el-button>
          <el-button text size="large" @click="emit('view-about')">
            关于我
          </el-button>
        </div>

        <div class="hero-status">
          当前阶段：先把博客首页、文章体验和内容结构打磨完整，AI 功能后置。
        </div>
      </div>
    </div>

    <div class="hero-bottom-row">
      <div class="hero-meta-grid">
        <article v-for="item in metrics" :key="item.label" class="meta-card">
          <span class="meta-label">{{ item.label }}</span>
          <strong class="meta-value">{{ item.value }}</strong>
          <p class="meta-desc">{{ item.desc }}</p>
        </article>
      </div>

      <div class="hero-tech-panel">
        <p class="section-label">TECH STACK</p>
        <h2>先把内容系统做完整，再继续打磨展示和部署</h2>
        <p class="tech-desc">
          首页重新定型为视频首屏，下面继续承接搜索、分类、标签和文章列表，
          整体回到一个真正可阅读、可展示的博客项目。
        </p>

        <div class="tech-stack">
          <span v-for="item in techStack" :key="item" class="tech-pill">
            {{ item }}
          </span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  metrics: {
    type: Array,
    default: () => [],
  },
  techStack: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['view-articles', 'view-project', 'view-about'])

const videoError = ref(false)
const heroVideoSrc = '/videos/home-hero.mp4'

const handleVideoError = () => {
  videoError.value = true
}
</script>

<style scoped>
.hero-section {
  max-width: 1180px;
  margin: 0 auto;
  padding: 36px 24px;
}

.hero-video-panel,
.meta-card,
.hero-tech-panel {
  border: 1px solid rgba(31, 31, 27, 0.08);
  background: rgba(255, 255, 255, 0.68);
  box-shadow: 0 20px 60px rgba(31, 31, 27, 0.06);
  backdrop-filter: blur(14px);
}

.hero-video-panel {
  position: relative;
  min-height: 560px;
  overflow: hidden;
  border-radius: 32px;
}

.hero-media,
.hero-video,
.hero-media-mask {
  position: absolute;
  inset: 0;
}

.hero-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-video-placeholder {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  background:
    linear-gradient(
      135deg,
      rgba(119, 117, 106, 0.18),
      rgba(255, 255, 255, 0.12)
    ),
    #d8d2c8;
  color: #5f5a4f;
  font-size: 16px;
  letter-spacing: 0.04em;
}

.hero-media-mask {
  background:
    linear-gradient(
      90deg,
      rgba(21, 20, 18, 0.62) 0%,
      rgba(21, 20, 18, 0.22) 48%,
      rgba(21, 20, 18, 0.08) 100%
    ),
    linear-gradient(
      180deg,
      rgba(21, 20, 18, 0.12) 0%,
      rgba(21, 20, 18, 0.38) 100%
    );
}

.hero-overlay {
  position: relative;
  z-index: 2;
  min-height: 560px;
  max-width: 720px;
  padding: 52px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  color: #f7f2ea;
}

.hero-label,
.section-label {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(247, 242, 234, 0.78);
}

.section-label {
  color: #7a7366;
}

.hero-title {
  margin: 16px 0 18px;
  font-size: 52px;
  line-height: 1.1;
  font-weight: 600;
}

.hero-desc {
  margin: 0;
  max-width: 560px;
  font-size: 16px;
  line-height: 1.9;
  color: rgba(247, 242, 234, 0.88);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 28px;
}

.hero-status {
  margin-top: 22px;
  display: inline-flex;
  width: fit-content;
  max-width: 100%;
  padding: 12px 16px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.14);
  color: rgba(247, 242, 234, 0.92);
  font-size: 14px;
  line-height: 1.6;
}

.hero-bottom-row {
  margin-top: 20px;
  display: grid;
  grid-template-columns: 1.25fr 0.9fr;
  gap: 20px;
}

.hero-meta-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.meta-card,
.hero-tech-panel {
  border-radius: 24px;
  padding: 24px;
}

.meta-label {
  display: block;
  font-size: 13px;
  color: #716b60;
}

.meta-value {
  display: block;
  margin-top: 12px;
  font-size: 34px;
  line-height: 1;
  color: #22201b;
}

.meta-desc {
  margin: 14px 0 0;
  color: #666154;
  line-height: 1.8;
  font-size: 14px;
}

.hero-tech-panel h2 {
  margin: 10px 0 14px;
  font-size: 28px;
  line-height: 1.35;
}

.tech-desc {
  margin: 0;
  color: #625d51;
  line-height: 1.85;
}

.tech-stack {
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tech-pill {
  padding: 8px 14px;
  border-radius: 999px;
  background: rgba(111, 127, 106, 0.12);
  color: #5d6a59;
  font-size: 13px;
}

@media (max-width: 1024px) {
  .hero-bottom-row {
    grid-template-columns: 1fr;
  }

  .hero-meta-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .hero-video-panel,
  .hero-overlay {
    min-height: 500px;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding-left: 16px;
    padding-right: 16px;
  }

  .hero-video-panel,
  .hero-overlay {
    min-height: 440px;
  }

  .hero-overlay {
    padding: 24px;
  }

  .hero-title {
    font-size: 34px;
  }

  .hero-status {
    border-radius: 20px;
  }

  .hero-meta-grid {
    grid-template-columns: 1fr;
  }
}
</style>
