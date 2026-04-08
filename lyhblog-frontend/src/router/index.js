import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
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
        component: () => import('../views/admin/Layout.vue'),
        meta: { requiresAuth: true, requiresAdmin: true },
        redirect: '/admin/article', 
        children: [
            {
                path: 'article', //子路由前面不用加/    
                name: 'AdminArticle',
                component: () => import('../views/admin/ArticleList.vue')

            },
            {
                path: 'article/add',
                name: 'AdminArticleAdd',
                component: () => import('../views/admin/ArticleEdit.vue')
            },
            {
                path: 'article/edit/:id',
                name: 'AdminArticleEdit',
                component: () => import('../views/admin/ArticleEdit.vue')
            },
            {
                path: 'comment',
                name: 'AdminComment',
                component: () => import('../views/admin/CommentList.vue')
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
    const userStore = useUserStore()

    const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
    const requiresAdmin = to.matched.some((record) => record.meta.requiresAdmin)

    if(requiresAuth && !userStore.isLogin){
        next({
            path: '/login',
            query: {redirect: to.fullPath}
        })
        return
    }
    
    if(requiresAdmin && !userStore.isAdmin){
        ElMessage.error('没有后台权限')
        next('/')
        return
    }
    next()
})

export default router;


