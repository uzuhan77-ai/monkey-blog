# lyhblog 继续开发：后台评论分页与优化

## 目标

把后台评论管理页从“加载全部评论”改成“分页加载评论”，并保证删除评论后页面刷新正常。

完成后效果：

1. 后台评论列表支持分页
2. 支持切换页码
3. 删除评论后自动刷新当前页
4. 如果当前页删到只剩最后一条，自动退回上一页

---

## 为什么现在做这个功能

你现在前台分类、标签、文章详情、后台分类、后台标签这些已经基本有了。  
下一步最适合补的是后台管理体验。

评论分页比这些功能更适合现在做：

1. 改动范围小
2. 前后端都容易理解
3. 很适合练分页接口和前端分页组件
4. 做完以后后台就更完整了

---

## 计划

### 计划 1：后端评论列表接口支持分页

接口：

`/api/comment/all/`

支持参数：

1. `current`
2. `size`

返回：

1. 当前页评论数据
2. 总数 `total`
3. 当前页码 `current`
4. 每页条数 `size`

### 计划 2：前端评论 API 支持分页参数

前端请求 `/comment/all/` 时，把分页参数带上。

### 计划 3：后台评论管理页接入分页器

页面底部加 `el-pagination`。

### 计划 4：删除评论后处理页码

如果当前页删到最后一条，并且不是第一页，就自动回到上一页。

---

## 需要改动的文件

1. `lyhblog-backend/blog/views/comment.py`
2. `lyhblog-frontend/src/api/comment.js`
3. `lyhblog-frontend/src/views/admin/CommentList.vue`

---

## 一、后端代码

文件：`lyhblog-backend/blog/views/comment.py`

找到 `CommentAllView`，替换成下面这版：

```python
class CommentAllView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            current = max(int(request.GET.get('current', 1)), 1)
            size = max(int(request.GET.get('size', 10)), 1)
        except (TypeError, ValueError):
            return Response({
                'code': 400,
                'message': '分页参数错误'
            }, status=400)

        queryset = Comment.objects.all().order_by('-create_time')
        total = queryset.count()
        start = (current - 1) * size
        end = start + size

        comments = queryset[start:end]
        serializer = CommentSerializer(comments, many=True)
        return Response({
            'code': 200,
            'data': serializer.data,
            'total': total,
            'current': current,
            'size': size
        })
```

### 这段代码在做什么

1. 从请求里拿 `current` 和 `size`
2. 防止分页参数不是数字
3. 查询全部评论并按时间倒序
4. 只切出当前页的数据
5. 把列表和总数一起返回给前端

---

## 二、前端 API 代码

文件：`lyhblog-frontend/src/api/comment.js`

把这段：

```javascript
export const ApiCommentAll = () =>{
    return request.get('/comment/all/')
}
```

改成：

```javascript
export const ApiCommentAll = (params) => {
    return request.get('/comment/all/', { params })
}
```

### 这段代码在做什么

这样你就可以传：

```javascript
ApiCommentAll({
  current: 1,
  size: 10
})
```

后台就能按页返回数据。

---

## 三、后台评论页完整代码

文件：`lyhblog-frontend/src/views/admin/CommentList.vue`

把这个文件改成下面这版：

```vue
<template>
    <div class="comment-list">
        <el-table :data="commentList" border>
            <el-table-column prop="id" label="ID" width="80px" />
            <el-table-column prop="username" label="用户" width="120" />
            <el-table-column prop="content" label="评论内容" />
            <el-table-column prop="create_time" label="时间" width="180" />
            <el-table-column label="操作" width="100">
                <template #default="{ row }">
                    <el-button type="danger" text @click="handleDelete(row.id)">
                        删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>

        <div class="pagination-box">
            <el-pagination
                background
                layout="total, prev, pager, next"
                :total="total"
                :page-size="size"
                v-model:current-page="current"
                @current-change="loadList"
            />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ApiCommentDelete, ApiCommentAll } from '../../api/comment'
import { ElMessage, ElMessageBox } from 'element-plus'

const commentList = ref([])
const current = ref(1)
const size = ref(10)
const total = ref(0)

const loadList = async () => {
    try {
        const res = await ApiCommentAll({
            current: current.value,
            size: size.value
        })
        if (res.data.code == 200) {
            commentList.value = res.data.data
            total.value = res.data.total
        }
    } catch (error) {
        ElMessage.error('评论列表加载失败')
    }
}

const handleDelete = (id) => {
    ElMessageBox.confirm('确定删除这条评论？', '提示', {
        type: 'warning'
    }).then(async () => {
        try {
            const res = await ApiCommentDelete(id)
            if (res.data.code === 200) {
                ElMessage.success('删除成功')

                const isLastItemOnPage = commentList.value.length === 1
                if (isLastItemOnPage && current.value > 1) {
                    current.value -= 1
                }

                loadList()
            }
        } catch (error) {
            ElMessage.error('删除失败')
        }
    })
}

onMounted(() => {
    loadList()
})
</script>

<style scoped>
.pagination-box {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}
</style>
```

---

## 四、实现逻辑解释

### 为什么要加 `current`、`size`、`total`

因为分页器至少需要这三个东西：

1. 当前页 `current`
2. 每页条数 `size`
3. 总条数 `total`

前端分页器才能知道总共有几页。

### 为什么删除后要判断是不是最后一条

比如：

1. 你现在在第 3 页
2. 第 3 页只有 1 条评论
3. 你删掉它以后，第 3 页就空了

这时候如果不回退到第 2 页，用户会看到空页，体验不好。

所以这里加了：

```javascript
const isLastItemOnPage = commentList.value.length === 1
if (isLastItemOnPage && current.value > 1) {
    current.value -= 1
}
```

---

## 五、自测步骤

改完后按下面顺序测试。

### 基础测试

1. 打开后台评论管理页
2. 看评论是否正常显示
3. 底部是否出现分页器

### 分页测试

1. 点击第 2 页
2. 再点击上一页
3. 看评论是否跟着变化

### 删除测试

1. 删除任意一条评论
2. 看是否自动刷新

### 最后一条测试

1. 找一个只有 1 条记录的最后页
2. 删除这条记录
3. 页面是否自动退回上一页

---

## 六、命令检查

后端检查：

```powershell
cd D:\Monkey-blog\lyhblog-backend
venv\Scripts\python.exe manage.py check
```

前端构建：

```powershell
cd D:\Monkey-blog\lyhblog-frontend
npm.cmd run build
```

---

## 七、做完这个之后建议的下一步

我建议你继续按这个顺序做：

1. 后台评论分页
2. 后台文章列表删除和提示优化
3. 前台筛选逻辑整理
4. 环境变量改造
5. Ubuntu 部署
6. 阿里云部署

---

## 结论

这个功能不大，但很适合你现在做。  
它能让你把“后台管理页”从能用，推进到更完整一点。

而且分页这块是你以后做文章列表、评论列表、后台管理都会一直复用的思路。
