<template>
    <header class="front-header">
        <div class="header-inner">
            <router-link to="/" class="brand">
                <span class="brand-mark">⌂LYH</span>
                <div class="brand-text">
                    <strong>lyhblog</strong>
                    <span>Django+ three.js</span>
                </div>
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
    background: rgba(250, 248, 243, 0.78);
    border-bottom: 1px solid rgba(31, 33, 29, 0.06);
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
  gap: 12px;
  text-decoration: none;
  color: #17211b;
}

.brand-mark {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: rgba(59, 130, 246, 0.12);
    color: #2f8df4;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    letter-spacing: 0;
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.brand-text strong {
  font-size: 16px;
}

.brand-text span {
  font-size: 12px;
  color: #5d6b63;
}

.brand-text strong {
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
  background: #1f4d3b;
  color: #fff;
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
  color: #1f4d3b;
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

  .nav-link:hover,
  .nav-link.active {
    background: rgba(59, 130, 246, 0.12);
    color: #2f8df4;
  }
}

</style>