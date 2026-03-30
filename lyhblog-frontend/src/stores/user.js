// 路由守卫 + Pinia 状态管理
import {defineStore} from 'pinia'
export const useUserStore = defineStore('user',{
    state:()=>({
        token:localStorage.getItem('token') || '',
        userInfo:null
    }),
    actions:{
        // 登录
        setToken(token){
            this.token = token
            localStorage.setItem('token',token)
        },

        // 登出
        logout(){
            this.token = ''
            this.userInfo = null
            localStorage.removeItem('token')
        }
    },
    getters: {
        isLogin: state => !!state.token
    }
})