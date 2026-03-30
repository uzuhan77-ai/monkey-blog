import axios from "axios";
import {ElMessage} from "element-plus";
import router from "../router";

const request = axios.create({
    baseURL: "http://127.0.0.1:8000/api",
    timeout: 10000
})


//请求拦截器:自动带上token
request.interceptors.request.use(
    config => {
        const token = localStorage.getItem("token");
        if (token) {
            config.headers.Authorization = `Token ${token}`
        }
        return config
    },
    error => {
        return Promise.reject(error);
    }
)

//响应拦截器：统一处理错误
request.interceptors.response.use(
    response => {
        return response;
    },
    error => {
        if (error.response) {
            switch (error.response.status){
                case 401:
                    ElMessage.error("请先登录")
                    localStorage.removeItem("token")
                    router.push("/login")
                    break;
                case 403:
                    ElMessage.error("没有权限")
                    break;
                case 404:
                    ElMessage.error("请求的资源不存在")
                    break;
                case 500:
                    ElMessage.error("服务器错误")
                    break;
                default:
                    ElMessage.error("请求失败")
                    break;
            }
        }else{
                ElMessage.error("网络错误")
            }
            return Promise.reject(error)
    }
)


export default request;