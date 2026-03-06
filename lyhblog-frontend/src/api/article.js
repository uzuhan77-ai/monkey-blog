import axios from 'axios'
import constant from '../utils/constant'


// 1. 获取文章列表 (改为 POST 请求，接收 data 参数，去掉末尾斜杠)
export function ApiArticleList(data) {
    return axios.post(constant.baseURL + '/article/listArticle/',data)
}

export function ApiArticleDetail(params) {
    return axios.get(constant.baseURL + '/article/getArticleById/',{params: params})
}

export function ApiLogin(data) {
    return axios.post(constant.baseURL + '/user/login/',data)
}

export function ApiRegister(data) {
    return axios.post(constant.baseURL + '/user/register/',data)
}

export function ApiCategoryList () {
    return axios.get(constant.baseURL + '/category/listCategory/')
}