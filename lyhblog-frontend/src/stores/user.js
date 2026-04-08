// 路由守卫 + Pinia 状态管理
import {defineStore} from 'pinia'
export const useUserStore = defineStore('user',{
    state:()=>({
        token:localStorage.getItem('token') || '',
        userInfo:JSON.parse(localStorage.getItem('user_info') || 'null'),
        isAdmin: localStorage.getItem('is_admin') === 'true'
    }),
    actions:{
        setLoginInfo(data){
            this.token = data.token
            this.userInfo ={
                username : data.username
            }
            this.isAdmin = data.is_admin

            localStorage.setItem('token', data.token)
            localStorage.setItem('user_info', JSON.stringify(this.userInfo))
            localStorage.setItem('is_admin', String(data.is_admin))
        },

        // 登出
        logout(){
            this.token = ''
            this.userInfo = null
            this.isAdmin = false

            localStorage.removeItem('token')
            localStorage.removeItem('user_info')
            localStorage.removeItem('is_admin')
        }
    },
    getters: {
        isLogin: state => !!state.token
    }
})