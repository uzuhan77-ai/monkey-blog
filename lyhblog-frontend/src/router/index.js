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
    }
]
    const router = createRouter({
        history: createWebHistory(),
        routes
    })
    export default router;