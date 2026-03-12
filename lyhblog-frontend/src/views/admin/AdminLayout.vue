<template>
    <el-container style="height: 100vh;">
        <!-- 左侧菜单栏 -->
         <el-aside width="200px" style="background-color: #204156;">
            <div style="color: white; text-align:center; padding: 20px 0;font-size: 20px;">
                后台管理系统
            </div>

            <el-menu
                :default-active="$route.path"
                router
                background-color="#204156"
                text-color="#bfcbd9"    
                active-text-color="#409EFF"
            >
                <el-menu-item index="/admin/article">
                    文章管理
                </el-menu-item>
                <el-menu-item index="/admin/comment" disabled>
                    评论管理
                </el-menu-item>
                <el-menu-item index="/">
                    返回前台
                </el-menu-item>
            </el-menu>
         </el-aside>

        <!-- 右侧 -->
         <el-container>
            <!-- 顶部 -->
             <el-header style="background:#fff;">
                <h3>欢迎来到后台</h3>
             </el-header>

            <!-- 内容 -->
             <el-main style="background:#f0f2f5;">
                <router-view></router-view>
             </el-main>
         </el-container>

    </el-container>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

</script>


<style >
body {
    margin: 0;
}
</style>