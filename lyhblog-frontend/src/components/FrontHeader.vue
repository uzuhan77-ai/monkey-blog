<template>
    <header class="front-header">
        <div class="header-inner">
            <router-link to="/" class="brand">
                <span class="brand-mark">⌂</span>
                <strong>LYH Blog</strong>
            </router-link>

            <nav class="nav-list">
                <router-link
                    v-for="item in navItems"
                    :key="item.path"
                    :to="item.path"
                    class="nav-link"
                    :class="{active:isActive(item.path)}"
                >
                    {{ item.label }}
            </router-link>
            </nav>

            <div class="nav-actions">
                <router-link to="/login" class="ghost-link">登录</router-link>
                <router-link to="/register" class="solid-link">注册</router-link>
            </div>
        </div>
    </header>
</template>

<script setup>
import {useRoute} from 'vue-router'

const route = useRoute()

const navItems = [
    {path: '/', label: '首页'},
    {path: '/project', label:'项目'},
    {path:'/about', label:'关于'}
]
const isActive = (path) => route.path === path

</script>

<style scoped>
.front-header {
  position: sticky;
  top: 0;
  z-index: 20;
  backdrop-filter: blur(18px);
  background: rgba(255, 255, 255, 0.78);
  border-bottom: 1px solid rgba(47, 141, 244, 0.08);
}

.header-inner {
  max-width: 1180px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: #2f8df4;
}

.brand-mark {
  width: 30px;
  height: 30px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #2f8df4;
  font-size: 24px;
  font-weight: 800;
  line-height: 1;
}

.brand strong {
  font-size: 16px;
  color: #2f8df4;
}

.nav-list {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-link {
  padding: 10px 14px;
  border-radius: 999px;
  text-decoration: none;
  color: #44524b;
  transition: all 0.2s ease;
}

.nav-link:hover,
.nav-link.active {
  background: rgba(47, 141, 244, 0.12);
  color: #2f8df4;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ghost-link,
.solid-link {
  text-decoration: none;
  font-size: 14px;
}

.ghost-link {
  color: #2f8df4;
}

.solid-link {
  padding: 10px 14px;
  border-radius: 999px;
  background: #2f8df4;
  color: #fff;
}

@media (max-width: 860px) {
  .header-inner {
    flex-direction: column;
    align-items: stretch;
  }

  .brand,
  .nav-list,
  .nav-actions {
    justify-content: center;
  }
}

</style>
