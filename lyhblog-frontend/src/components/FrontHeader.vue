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
                <div class="header-search">
                  <input
                    v-model="searchKeyword"
                    class="header-search-input"
                    placeholder="搜索"
                    @keyup.enter="handleHeaderSearch"
                  />
                  <button 
                    class="header-search-button"
                    type="button"
                    @click="handleHeaderSearch"
                  >
                    ⌕
                  </button>
                </div>
                <router-link to="/login" class="ghost-link">登录</router-link>
                <router-link to="/register" class="solid-link">注册</router-link>
            </div>
        </div>
    </header>
</template>

<script setup>
import {useRoute, useRouter} from 'vue-router'
import {ref,watch} from 'vue'

const route = useRoute()
const router = useRouter()
const searchKeyword = ref('')

const handleHeaderSearch = () => {
  const keyword = searchKeyword.value.trim()
  if (!keyword) return 

  router.push({
    path: '/',
    query: {keyword},
  })
}

watch(
  () => route.query.keyword,
  (value) => {
    searchKeyword.value = value ? String(value) : ''
  },
  { immediate: true }
)

const navItems = [
    {path: '/', label: '首页'},
    {path: '/archive', label: '归档'},
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
  padding: 8px 24px 0;
  background: rgba(246, 248, 251, 0.72);
  backdrop-filter: blur(18px);
}

.header-inner {
  max-width: 1168px;
  margin: 0 auto;
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 22px;
  border: 1px solid rgba(31, 36, 48, 0.055);
  border-radius: 0 0 14px 14px;
  background: rgba(255, 255, 255, 0.88);
  box-shadow: 0 8px 26px rgba(15, 23, 42, 0.045);
  backdrop-filter: blur(18px);
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: #2f8df4;
  white-space: nowrap;
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
  padding: 9px 14px;
  border-radius: 999px;
  text-decoration: none;
  color: rgba(31, 36, 48, 0.72);
  font-size: 15px;
  font-weight: 600;
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
  gap: 10px;
}

.header-search {
  width: 164px;
  height: 38px;
  padding: 0 6px 0 14px;
  display: flex;
  align-items: center;
  gap: 6px;
  border: 1px solid rgba(31, 36, 48, 0.07);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.76);
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.035);
  transition:
    width 0.2s ease,
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    background 0.2s ease;
}

.header-search:focus-within {
  width: 224px;
  border-color: rgba(47, 141, 244, 0.22);
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
}

.header-search-input {
  min-width: 0;
  flex: 1;
  border: 0;
  outline: 0;
  background: transparent;
  color: rgba(31, 36, 48, 0.86);
  font-size: 14px;
}

.header-search-input::placeholder {
  color: rgba(31, 36, 48, 0.36);
}

.header-search-button {
  width: 28px;
  height: 28px;
  border: 0;
  border-radius: 999px;
  display: grid;
  place-items: center;
  background: transparent;
  color: #2f8df4;
  font-size: 18px;
  line-height: 1;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease;
}

.header-search-button:hover {
  background: rgba(47, 141, 244, 0.1);
}

.header-search-button:active {
  transform: scale(0.94);
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
  padding: 9px 14px;
  border-radius: 999px;
  background: #2f8df4;
  color: #fff;
  box-shadow: 0 8px 18px rgba(47, 141, 244, 0.16);
}

@media (max-width: 860px) {
  .front-header {
    padding: 8px 14px 0;
  }

  .header-inner {
    flex-direction: column;
    align-items: stretch;
    padding: 14px;
    border-radius: 0 0 16px 16px;
  }

  .brand,
  .nav-list,
  .nav-actions {
    justify-content: center;
  }

  .header-search,
  .header-search:focus-within {
    width: min(100%, 320px);
  }
}

</style>
