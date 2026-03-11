// 统一管理所有 axios 请求
import axios from 'axios'
import constant from './constant'
import router from '../router'

// 1. 创建一个专属的 axios 实例
const request = axios.create({
    baseURL: constant.baseURL,
    timeout: 5000,
})
// 2. 请求拦截器：发请求之前执行
request.interceptors.request.use(
    config =>{
        const token = localStorage.getItem('user_token')
        if(token){
            // 请求头最终变成：Authorization: Bearer xxxxxxx
            config.headers['Authorization'] = `Bearer ${token}`
        }
        return config
    }, error =>{
        // 请求配置出错时抛出异常
        return Promise.reject(error)
    })

// 3. 响应拦截器：后端返回数据后执行
request.interceptors.response.use(
    response =>{
        // 请求成功,直接把数据原样放行
        return response
    }, error =>{
        // 如果请求报错，看看是不是 401 （未授权/TOKEN过期）
        if (error.response && error.response.status === 401){
            console.log("身份验证失败，请重新登录")
            // 清楚本地失效的 TOKEN
            localStorage.removeItem('user_token')
            // 跳回登录
            router.push('/login')
        }
        return Promise.reject(error)
    }
)

export default request

