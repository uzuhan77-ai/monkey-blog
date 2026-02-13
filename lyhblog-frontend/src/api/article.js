import axios from 'axios'
import constant from '../utils/constant'



export function ApiArticleList() {
    return axios.get(constant.baseURL + '/article/listArticle/')
}

export function ApiArticleDetail(id) {
    return axios.get(constant.baseURL + '/article/detail/${id}/')
}