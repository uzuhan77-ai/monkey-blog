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
                <template v-if="userStore.isLogin">
                  <router-link v-if="userStore.isAdmin" to="/admin/article" class="ghost-link">
                    后台
                  </router-link>
                  <span class="login-user">{{ userStore.userInfo?.username || '用户' }}</span>
                  <router-link to="/" class="solid-link" @click="handleLogout">
                    退出
                  </router-link>
                </template> 
                <template v-else>
                  <router-link to="/login" class="ghost-link">登录</router-link>
                  <router-link to="/register" class="solid-link">注册</router-link>
                </template>
            </div>
        </div>
    </header>
</template>

<script setup>
import {useRoute, useRouter} from 'vue-router'
import {ref,watch} from 'vue'
import {ElMessage} from 'element-plus'
import {useUserStore} from '../stores/user'

const route = useRoute()
const router = useRouter()
const searchKeyword = ref('')
const userStore = useUserStore()

const handleHeaderSearch = () => {
  const keyword = searchKeyword.value.trim()
  if (!keyword) return 

  router.push({
    path: '/',
    query: {keyword},
  })
}


const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
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
  z-index: 50;
  padding: 0 24px;
  background: rgba(246, 248, 251, 0.76);
  backdrop-filter: blur(20px);
}

.header-inner {
  max-width: 1168px;
  min-height: 72px;
  margin: 0 auto;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  border: 1px solid rgba(31, 36, 48, 0.055);
  border-top: 0;
  border-radius: 0 0 18px 18px;
  background: rgba(255, 255, 255, 0.93);
  box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
  backdrop-filter: blur(18px);
}

.brand {
  display: flex;
  align-items: center;
  gap: 9px;
  min-height: 52px;
  padding: 0 18px;
  border-radius: 12px;
  text-decoration: none;
  color: #2f8df4;
  white-space: nowrap;
  transition:
    background 0.2s ease,
    transform 0.2s ease;
}

.brand:hover {
  background: rgba(47, 141, 244, 0.08);
  transform: translateY(-1px);
}

.brand:active {
  transform: scale(0.97);
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
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.nav-link {
  min-height: 44px;
  padding: 0 20px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  color: rgba(31, 36, 48, 0.68);
  font-size: 15px;
  font-weight: 700;
  transition:
    background 0.2s ease,
    color 0.2s ease,
    transform 0.2s ease;
}

.nav-link:hover,
.nav-link.active {
  background: rgba(47, 141, 244, 0.1);
  color: #2f8df4;
}

.nav-link:active {
  transform: scale(0.96);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 0 0 auto;
}

.header-search {
  width: 168px;
  height: 44px;
  padding: 0 7px 0 15px;
  display: flex;
  align-items: center;
  gap: 6px;
  border: 1px solid rgba(31, 36, 48, 0.07);
  border-radius: 13px;
  background: rgba(255, 255, 255, 0.7);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.45);
  transition:
    width 0.2s ease,
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    background 0.2s ease;
}

.header-search:focus-within {
  width: 214px;
  border-color: rgba(47, 141, 244, 0.22);
  background: rgba(255, 255, 255, 0.96);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.5),
    0 8px 22px rgba(15, 23, 42, 0.07);
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
  width: 30px;
  height: 30px;
  border: 0;
  border-radius: 10px;
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
.solid-link,
.login-user {
  text-decoration: none;
  min-height: 44px;
  padding: 0 13px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  transition:
    background 0.2s ease,
    color 0.2s ease,
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.ghost-link {
  color: #2f8df4;
}

.ghost-link:hover {
  background: rgba(47, 141, 244, 0.08);
}

.solid-link {
  background: #2f8df4;
  color: #fff;
  box-shadow: 0 8px 18px rgba(47, 141, 244, 0.15);
}

.solid-link:hover {
  background: #257fe3;
  box-shadow: 0 10px 22px rgba(47, 141, 244, 0.2);
}

.login-user {
  max-width: 116px;
  background: rgba(31, 36, 48, 0.045);
  color: rgba(31, 36, 48, 0.62);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  box-shadow: inset 0 0 0 1px rgba(31, 36, 48, 0.04);
}

.ghost-link:active,
.solid-link:active {
  transform: scale(0.96);
}

@media (max-width: 860px) {
  .front-header {
    padding: 0 14px;
  }

  .header-inner {
    flex-direction: column;
    align-items: stretch;
    padding: 12px;
    gap: 10px;
    border-radius: 0 0 18px 18px;
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

  .nav-list {
    flex-wrap: wrap;
  }

  .nav-actions {
    flex-wrap: wrap;
    justify-content: center;
  }

  .login-user {
    max-width: min(100%, 180px);
  }
}

</style>
