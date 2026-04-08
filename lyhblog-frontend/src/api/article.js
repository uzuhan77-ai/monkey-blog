import request from '../utils/request'




// 1. 获取文章列表 (改为 POST 请求，接收 data 参数，去掉末尾斜杠)
export function ApiArticleList(data) {
    return request.post('/article/listArticle/',data)
}

export function ApiArticleDetail(id) {
    return request.get('/article/getArticleById/', { params: { id } })
}

// 新增文章
export const ApiArticleAdd = (data) => {
    return request.post('/article/add/', data)
  }
// 删除文章
export const ApiArticleDelete = (id) =>{
    return request.post('/article/delete/',{id})
}
// 更新文章
export const ApiArticleUpdate = (data) => {
    return request.post('/article/update/', data)
  }
// 获取标签列表
export const ApiTagList = () => {
    return request.get('/tag/list/')
  }
// 获取分类列表
export function ApiCategoryList () {
    return request.get('/category/list/')
}

export function ApiLogin(data) {
    return request.post('/user/login/',data)
}

export function ApiRegister(data) {
    return request.post('/user/register/',data)
}
