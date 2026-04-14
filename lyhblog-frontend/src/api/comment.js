import request from '../utils/request'


// 获取评论列表
export const ApiCommentList = (articleId) => {
    return request.get('/comment/list/',{
        params: { article_id: articleId }
    })
}

// 发表评论
export const ApiCommentAdd = (data) =>{
    return request.post('/comment/add/', data)
}

// 
export const ApiCommentAll = (params) =>{
    return request.get('/comment/all/',{params})
}


// 删除评论
export const ApiCommentDelete = (id) =>{
    return request.post('/comment/delete/', {id})
}