import request from '../utils/request'


export const ApiCategoryList = () =>{
    return request.get('/category/list/')
}
export const ApiCategoryAdd = (data) =>{
    return request.post('/category/add/', data)
}
export const ApiCategoryUpdate = (data) =>{
    return request.post('/category/update/', data)
}
export const ApiCategoryDelete = (id) =>{
    return request.post('/category/delete/',{id})
}