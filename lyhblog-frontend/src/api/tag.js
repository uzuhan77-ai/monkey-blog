import request from '../utils/request'




export const ApiTagList = () =>{
    return request.get('/tag/list/')
}
export const ApiTagAdd = (data) =>{
    return request.post('/tag/add/',data)
}
export const ApiTagUpdate = (data) =>{
    return request.post('/tag/update/',data)
}
export const ApiTagDelete = (id) =>{
    return request.post('/tag/delete/', {id})
}