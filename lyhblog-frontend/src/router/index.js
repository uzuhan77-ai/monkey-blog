import { createRouter, createWebHistory } from 'vue-router'
const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../views/Home.vue')
    },
    {
        path: '/article',
        name: 'ArticleDetail',
        component: () => import('../views/ArticleDetail.vue')
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/login.vue')
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/register.vue')
    },
    // 后台管理的嵌套路由
    {
        path: '/admin',
        name: 'Admin',
        component: () => import('../views/admin/AdminLayout.vue'),
        redirect: '/admin/article',
        children: [
            {
                path: 'article', //子路由前面不用加/
                name: 'AdminArticle',
                component: () => import('../views/admin/ArticleManage.vue')

            }
        ]
    }





]
    const router = createRouter({
        history: createWebHistory(),
        routes
    })
    export default router;