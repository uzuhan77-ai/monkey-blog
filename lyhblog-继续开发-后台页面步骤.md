# lyhblog 继续开发步骤：后台页面

> 这份文档只针对你当前项目的下一步开发。
> 目标不是重写项目，而是把已经能打开的后台页面，继续写到“真正可用”。

---

## 一、当前重点

先做这两个页面：

- `lyhblog-frontend/src/views/admin/ArticleEdit.vue`
- `lyhblog-frontend/src/views/admin/CommentList.vue`

推荐顺序：

1. 先做 `ArticleEdit.vue`
2. 再做 `CommentList.vue`

原因：

- `ArticleEdit.vue` 更适合练“表单 + 接口 + 回显 + 保存”整条链路
- `CommentList.vue` 主要是列表和删除，复杂度更低

---

## 二、先做 ArticleEdit.vue

文件位置：

- `lyhblog-frontend/src/views/admin/ArticleEdit.vue`
- `lyhblog-frontend/src/api/article.js`
- `lyhblog-backend/blog/urls.py`

你的目标是让这两个地址可用：

- `/admin/article/add`
- `/admin/article/edit/:id`

---

## 三、ArticleEdit 第 1 步：先检查接口层

先打开：

- `lyhblog-frontend/src/api/article.js`

先看这几个接口是否存在、是否可用：

- `ApiArticleAdd`
- `ApiArticleUpdate`
- `ApiCategoryList`
- `ApiTagList`
- `ApiArticleDetail`

你要检查的点：

- 路径是否和后端一致
- 请求方式是否正确
- 参数是不是统一传 `data`
- 有没有明显拼写错误

这一阶段先不要动删除接口，它和当前任务无关。

---

## 四、ArticleEdit 第 2 步：先跑通“新增文章”

先不要急着做编辑回显。

你在 `ArticleEdit.vue` 里先只完成这两部分：

### 1. loadData

先做：

- 加载分类列表
- 加载标签列表

目的：

- 让分类下拉框有数据
- 让标签多选框有数据

你现在应该重点检查：

- `categories` 有没有拿到后端数据
- `tags` 有没有拿到后端数据

### 2. handleSubmit

先只写新增逻辑：

- 当 `isEdit` 为 `false`
- 调用新增文章接口
- 成功后跳回 `/admin/article`

这一阶段不要把新增和编辑混着写，先把新增跑通。

---

## 五、ArticleEdit 第 3 步：再做“编辑文章回显”

当新增能用后，再继续做编辑。

你现在项目里已经有文章详情接口，可以先复用：

- `ApiArticleDetail`

你要做的事情：

1. 从 `route.params.id` 取文章 id
2. 请求文章详情
3. 把返回的数据填回表单

至少要回填这些字段：

- `title`
- `category_id`
- `tags`
- `summary`
- `content`

这里最容易出错的是标签：

- 表单里一般绑定的是标签 id 数组
- 但后端返回的可能是标签对象数组

如果你拿到的是对象数组，你要自己转成：

- `[1, 2, 3]`

而不是直接把对象数组塞进去。

---

## 六、ArticleEdit 第 4 步：最后做“编辑保存”

当回显已经正常后，再补 `handleSubmit` 的另一半：

- 当 `isEdit` 为 `true`
- 调用更新接口
- 成功后跳回 `/admin/article`

这一步你要特别注意：

- 更新接口需要带文章 id
- 不要只传表单字段，不传 id

---

## 七、ArticleEdit 最容易踩的坑

- `isEdit` 是 `computed`，判断时要注意取值方式
- 编辑页 id 来自 `route.params.id`，不是 `route.query.id`
- `category_id` 绑定的是分类 id，不是分类对象
- `tags` 绑定的是 id 数组，不是标签对象数组
- 新增和编辑最好写成两个分支，不要一开始揉成一坨

---

## 八、ArticleEdit 验收标准

你自己按这个顺序验收：

1. 打开 `/admin/article/add`
2. 分类下拉能显示
3. 标签下拉能显示
4. 输入标题和内容后能提交
5. 提交成功后能回到文章列表
6. 打开 `/admin/article/edit/1`
7. 能看到旧文章数据
8. 修改后能保存成功

---

## 九、再做 CommentList.vue

文件位置：

- `lyhblog-frontend/src/views/admin/CommentList.vue`
- `lyhblog-frontend/src/api/comment.js`
- `lyhblog-backend/blog/views/comment.py`
- `lyhblog-backend/blog/urls.py`

这个页面的目标很简单：

- 能显示所有评论
- 能删除评论

---

## 十、CommentList 第 1 步：先跑通评论列表

你先确认这件事：

- 前端请求地址
- 后端路由地址

要完全对应。

你需要检查：

- 前端请求的是不是 `/comment/all/`
- 后端有没有这个接口
- 这个接口是不是要求管理员权限

这里你要记住：

- 页面能打开，不代表接口一定能返回数据
- 如果后端接口加了管理员权限，普通登录用户可能会拿到 `403`

---

## 十一、CommentList 第 2 步：再做删除功能

先不要一开始就写删除。

先确认列表能显示后，再去做删除按钮。

你需要检查：

- 前端删除接口路径
- 后端删除接口路径

如果前后端路径不一致，现象通常是：

- 列表能显示
- 但点击删除就报错

---

## 十二、CommentList 最容易踩的坑

- 模板里绑定的变量名和脚本里的变量名不一致
- `onMounted` 调用了不存在的方法
- 前端接口路径和后端 `urls.py` 对不上
- 请求被 `401` 或 `403` 拦住，但你误以为是页面坏了

---

## 十三、CommentList 验收标准

1. 打开 `/admin/comment`
2. 页面能正常显示表格
3. 评论数据能加载出来
4. 删除按钮可以点击
5. 删除成功后列表自动刷新

---

## 十四、如果页面“打不开”，按这个顺序查

不要一上来就怀疑 Vue 出大问题，先按顺序排：

### 第 1 层：查路由

看：

- 子路由有没有真正挂到 `/admin` 下
- 路由对象里是不是写了正确的 `component`
- `Layout.vue` 里有没有 `<router-view />`

### 第 2 层：查登录守卫

看：

- 有没有被自动跳去 `/login`
- 本地有没有 token

### 第 3 层：查接口

打开浏览器 Network，看请求返回的是：

- `200`
- `401`
- `403`
- `404`
- `500`

### 第 4 层：查组件本身

看：

- 变量名对不对
- 方法名对不对
- 生命周期里调用的方法存不存在

---

## 十五、你接下来怎么和我配合

最好的方式不是一句“又不行了”，而是带着结果来：

- `我先写完 ArticleEdit 的新增了，你帮我查`
- `我现在分类能出来，但标签回显不对`
- `CommentList 能显示，但删除按钮报错`

这样我就能直接按你当前卡住的点继续带你，不会重复讲已经会的东西。

---

## 十六、现在就做什么

先只做 `ArticleEdit.vue` 的前两步：

1. 接好分类和标签列表
2. 跑通新增文章

先别同时做编辑回显，也别同时做评论管理。

把新增跑通以后，再继续下一段。
