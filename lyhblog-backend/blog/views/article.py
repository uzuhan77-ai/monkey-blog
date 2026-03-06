# 这里只保留文章需要的 import
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Article, Category # 注意这里变成了相对导入 '..'
from ..serializers import ArticleSerializer, CategorySerializer # 注意这里变成了相对导入 '..'






# 1. 文章列表接口 (post)
class ArticleListView(APIView):
    def post(self, request):
        # 1. 从 request.data 获取前端传来的分页参数，如果没有传，默认 current=1, size=10
        # 注意：前端传过来的可能是字符串，需要转成整数 int()
        current = int(request.data.get('current',1))
        size = int(request.data.get('size',10))
        category_id = request.data.get('category_id')
        queryset = Article.objects.all()

        if category_id:
            queryset = queryset.filter(category_id =category_id)

        # 2. 计算切片的起始和结束位置
        start = (current-1) * size
        end = start + size

        # 3. 先查询数据库里一共有多少篇文章（前端分页组件需要这个总数）
        total = queryset.count()

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