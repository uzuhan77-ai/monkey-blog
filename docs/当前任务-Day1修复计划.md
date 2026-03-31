# 当前任务：Day 1 前端修复

## 任务目标
修复文章列表到详情页的链路，确保从首页点击"查看详情"能正确进入详情页并显示完整内容。

## 需要修复的4个问题

### 1. 路由拼写错误
**问题**：详情页路由定义是 `/articel`，但首页跳转写的是 `/article`
**位置**：`src/router/index.js`
**修复**：将路由路径统一改为 `/article/:id` 或 `/article`

### 2. 列表跳详情代码错误
**问题**：`goToDetail` 函数中 `id` 参数未正确传递
**位置**：`src/views/Home.vue`
**修复**：确保点击事件正确传递文章id，例如：
```javascript
const goToDetail = (id) => {
  router.push(`/article?id=${id}`)
}
```

### 3. 详情页取参不匹配
**问题**：详情页用 `route.params.id` 获取参数，但跳转时用的是 query 方式
**位置**：`src/views/ArticleDetail.vue`
**修复**：改为 `route.query.id` 获取参数，或者改用 params 方式跳转

### 4. 详情页正文未渲染
**问题**：详情页模板中正文区域为空，没有显示 `article.content`
**位置**：`src/views/ArticleDetail.vue`
**修复**：在模板中添加正文显示，例如：
```vue
<div class="content">{{ article.content }}</div>
```

## 验收标准
- [ ] 从首页点击"查看详情"能成功跳转到详情页
- [ ] 详情页URL带有正确的文章id参数（如：`/article?id=1`）
- [ ] 详情页能显示文章标题
- [ ] 详情页能显示发布时间
- [ ] 详情页能显示完整正文内容
- [ ] 浏览器控制台无关键报错

## 涉及文件
1. `lyhblog-frontend/src/router/index.js` - 路由配置
2. `lyhblog-frontend/src/views/Home.vue` - 首页列表
3. `lyhblog-frontend/src/views/ArticleDetail.vue` - 详情页

## 预计时间
2-3小时
