from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article
from .serializers import  ArticleSerializer


# Create your views here.
class TestView(APIView):
    def get(self, request):
        return Response({'message':'hello', 'code':200}, status= status.HTTP_200_OK)




# 1. 文章列表接口 (GET)
# generics.ListAPIView 是 DRF 专门用来做列表的通用视图，非常方便
class ArticleListView(generics.ListAPIView):
    queryset= Article.objects.all().order_by('-create_time')
    serializer_class= ArticleSerializer

# 2. 文章详情接口 (GET)
# generics.RetrieveAPIView 是专门用来获取单条数据的
class ArticleDetailView(generics.RetrieveAPIView):
    queryset= Article.objects.all()
    serializer_class = ArticleSerializer