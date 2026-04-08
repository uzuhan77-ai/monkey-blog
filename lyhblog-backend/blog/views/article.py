# 这里只保留文章需要的 import
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Article, Category # 注意这里变成了相对导入 '..'
from ..serializers import ArticleSerializer, CategorySerializer # 注意这里变成了相对导入 '..'






# 1. 文章列表接口 (post)
class ArticleListView(APIView):
    def post(self, request):
        current = int(request.data.get('current',1))
        size = int(request.data.get('size',10))
        category_id = request.data.get('category_id')

        queryset = Article.objects.all()
        if category_id:
            queryset = queryset.filter(category_id =category_id)

        total = queryset.count()
        start = (current-1) * size
        end = start + size


        articles = queryset.order_by('-create_time')[start:end]
        serializer = ArticleSerializer(articles, many=True)
        return Response({
            "code": 200,
            "data": serializer.data,
            "total":total,
            "message": "成功获取文章列表",
        })


# 2. 文章详情接口 (GET)
class ArticleDetailView(APIView):
    def get(self, request):
        article_id = request.GET.get('id')
        if not article_id:
            return Response({"code": 400, "message": "缺少文章ID参数"}, status=400)

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({"code": 404, "message": "hello，文章不存在"}, status=404)

        serializer = ArticleSerializer(article)
        return Response({
            "code": 200,
            "data": serializer.data,
            "message": "成功获取文章详情"
        })


#3、 新增文章接口（POST）
class ArticleAddView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]

    def post(self,request):
        title = request.data.get('title')
        content = request.data.get('content')
        summary= request.data.get('summary','')
        category_id = request.data.get('category_id')

        #标签前端传过来的应该是由一个有 id 组成的列表，比如[1,2]
        tags = request.data.get('tags',[])

        if not title or not content:
            return Response({
                "code": 400,
                "message": "标题和内容不能为空"
            },status=400)
        #1、先创建文章基本信息
        article = Article.objects.create(
            title = title,
            content = content,
            summary = summary,
            category_id = category_id
        )
        #2、再绑定多对多的关系的标签
        if tags:
            article.tags.set(tags)

        return Response({
            "code": 200,
            "message": "文章发布成功!"
        })

#4、修改文章接口（POST）
class ArticleUpdateView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]

    def post(self,request):
        article_id = request.data.get('id')
        if not article_id:
            return Response({
                "code": 400,
                "message": "缺少文章id"
            },status=400)

        try:
            article = Article.objects.get(id = article_id)
        except Article.DoesNotExist:
            return Response({
                "code": 404,
                "message": "文章不存"
            },status=404)
        #更新对应字段（如果前端没传某个字段，就保持原有内容不变）
        article.title = request.data.get('title', article.title)
        article.content = request.data.get('content', article.content)
        article.summary = request.data.get('summary', article.summary)
        article.category_id = request.data.get('category_id', article.category_id)
        article.save()

        #更新标签
        tags = request.data.get('tags')
        if tags is not None:#如果前端传了 （空列表），覆盖更新
            article.tags.set(tags)
        return Response({
            "code": 200,
            "message": "文章修改成功!"
        })
#删除文章接口（POST）
class ArticleDeleteView(APIView):
    permission_classes =[IsAuthenticated,IsAdminUser]

    def post(self,request):
        article_id = request.data.get('id')
        if not article_id:
            return Response({
                "code": 400,
                "message": "缺少文章id"
            },status=400)
        try:
            article = Article.objects.get(id=article_id)
            article.delete() #删除
            return Response({
                "code":200,
                "message": "文章删除成功"
            })
        except Article.DoesNotExist:
            return Response({
                "code":404,
                "message":"文章不存在"
            },status=404)
