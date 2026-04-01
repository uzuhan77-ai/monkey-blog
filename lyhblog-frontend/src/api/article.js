import request from '../utils/request'




// 1. 获取文章列表 (改为 POST 请求，接收 data 参数，去掉末尾斜杠)
export function ApiArticleList(data) {
    return request.post('/article/listArticle/',data)
}

export function ApiArticleDetail(id) {
    return request.get('/article/getArticleById/', { params: { id } })
}

export function ApiArticleAdd(data) {
    return request.post('/article/add/',data)
}

export function ApiArticleDelete(data) {
    return request.post('/article/delete/',data)
}

export function ApiArticleUpdate(data) {
    return request.post('/article/update/',data)
}

export function ApiLogin(data) {
    return request.post('/user/login/',data)
}

export function ApiRegister(data) {
    return request.post('/user/register/',data)
}

export function ApiCategoryList () {
    return request.get('/category/listCategory/')
}
