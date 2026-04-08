from ctypes.wintypes import tagRECT

from rest_framework import serializers
from .models import Article, Category, Tag, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many= True,read_only=True)
    create_time= serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True
    )

    class Meta:
        model= Article
        # 这里定义你想传给前端哪些字段
        # 如果你的模型字段名和这里不一样，请核对 models.py
        fields = ['id', 'title', 'summary', 'content', 'create_time', 'tags', 'category']


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only= True)
    create_time = serializers.DateTimeField(format = "%Y-%m-%d %H:%M:%S", read_only= True)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'create_time', 'article', 'username']
