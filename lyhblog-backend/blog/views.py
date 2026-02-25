from django.shortcuts import render, get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article
from .serializers import  ArticleSerializer


# Create your views here.
class TestView(APIView):
    def get(self, request):
        return Response({'message':'hello', 'code':200}, status= status.HTTP_200_OK)




# 1. 文章列表接口 (post)
class ArticleListView(APIView):
    def post(self, request):
        #1 查询数据库
        articles= Article.objects.all().order_by('-create_time')
        #2  序列化
        serializer = ArticleSerializer(articles, many= True)
        #3  返回数据
        return Response({
            "code": 200,
            "data": serializer.data,
            "message": "成功获取文章列表"
        })


# 2. 文章详情接口 (GET)
class ArticleDetailView(APIView):
    def get(self, request):
        #1. 获取参数
        article_id= request.GET.get('id')

        if not article_id:
            return Response({
                "code": 400,
                "message": "缺少文章ID参数"
            },status= 400)
        #2. 查询数据库
        try:
            article= Article.objects.get(id= article_id)
        except Article.DoesNotExist:
            return Response({
                "code": 404,
                "message": "hello，文章不存在"
            },status=404)

        # 4. 如果找到了，就正常翻译成JSON并返回
        serializer= ArticleSerializer(article)
        return Response({
            "code": 200,
            "data": serializer.data,
            "message": "成功获取文章详情"
        })


