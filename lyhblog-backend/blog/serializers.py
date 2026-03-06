from rest_framework import serializers
from .models import Article, Category, Tag

# 1. 新增：分类序列化器
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# 2. 新增：标签序列化器
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields=['id', 'name']




class ArticleSerializer(serializers.ModelSerializer):
    # 核心：把刚刚写好的分类和标签序列化器嵌套进来
    # read_only=True 表示这俩字段只用来返回给前端展示，不用来接收前端的修改
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many= True,read_only=True)
    # 格式化时间，让前端直接显示 2026-02-12 12:00:00 这种格式
    create_time= serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only= True)

    class Meta:
        model= Article
        # 这里定义你想传给前端哪些字段
        # 如果你的模型字段名和这里不一样，请核对 models.py
        fields = ['id', 'title', 'summary', 'content', 'create_time', 'tags', 'category']