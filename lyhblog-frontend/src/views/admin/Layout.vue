<template>
    <el-container class="admin-layout">
        <el-aside width="200px">
            <div class="logo">后台</div>
            <el-menu
                :default-active="activeMenu"
                router
            >

                <el-menu-item index="/admin/article">
                    <span>文章管理</span>
                </el-menu-item>
                <el-menu-item index="/admin/comment">
                    <span>评论管理</span>
                </el-menu-item>
            </el-menu>
        </el-aside>

        <el-container>
            <el-header>
                <div class="header-right">
                    <span>{{ userStore.userInfo?.username || '管理员' }}</span>
                    <el-button type="danger" text @click="handleLogout"> 退出</el-button>
                </div>  
            </el-header>
            
            <el-main>
                <router-view />
            </el-main>
        </el-container>
    </el-container>


</template>

<script setup>
import {computed} from 'vue'
import {useRoute,useRouter} from 'vue-router'
import {useUserStore} from '../../stores/user'
import {ElMessageBox} from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

const handleLogout = () => {
    ElMessageBox.confirm('确定退出登录？','提示', {
        confirmButtonText:'确定',
        cancelButtonText:'取消',
        type:'warning'
    }).then(() =>{
        userStore.logout()
        router.push('/login')
    })
}
</script>

<style scoped>
.admin-layout {
  height: 100vh;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  color: #409eff;
  border-bottom: 1px solid #eee;
}

.el-aside {
  background: #fff;
  border-right: 1px solid #eee;
}

.el-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  border-bottom: 1px solid #eee;
  background: #fff;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.el-main {
  background: #f5f7fa;
}


</style>