import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'
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
        component: () => import('../views/Login.vue')
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/register.vue')
    },
    // 后台管理的嵌套路由 (需要登录)
    {
        path: '/admin',
        name: 'Admin',
        component: () => import('../views/admin/AdminLayout.vue'),
        meta:{ requiresAuth: true }, //标记需要登录
        redirect: '/admin/article', 
        children: [
            {
                path: 'article', //子路由前面不用加/
                name: 'AdminArticle',
                component: () => import('../views/admin/ArticleManage.vue')

            },
            {
                path: 'comment',
                name: 'AdminComment',
                component: () => import('../views/admin/AdminComment.vue')
            }
        ]
    }





]
const router = createRouter({
    history: createWebHistory(),
    routes
})
// 路由守卫
router.beforeEach((to, from , next) =>{
    // 看访客要去哪里？如果路径是以'/admin' 开头，说明想去后台
    // if (to.path.startsWith('/admin') ){

    //     // 让他把证件掏出来
    //     const token = localStorage.getItem('user_token')
    //     const isAdmin = localStorage.getItem('is_admin')

    //     // 有没有登录？没有登录提到登录
    //     if(!token){
    //         alert('请先登录')
    //         return next('/login')
    //     }
    //     // 是不是管理员？
    //     // 避坑指南：localStorage里存的true会变成字符串'true',所以这里必须和字符串做对比
    //     if(isAdmin !== 'true'){
    //         alert('权限不足')
    //         return next('/')

    //     }

    //     next()

    const useStore = useUserStore()

    // 如果路由需要登录，但用户未登录
    if (to.meta.requiresAuth && !useStore.isLogin){
        next({
            path: '/login',
            query: { redirect: to.fullPath } //记住要去的页面
        })
    }else{
        // 如果不是取后台bao'an不查证
        next()
    }
})

export default router;


