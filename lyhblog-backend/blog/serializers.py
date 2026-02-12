from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    # 格式化时间，让前端直接显示 2026-02-12 12:00:00 这种格式
    create_time= serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only= True)

    class Meta:
        model= Article
        # 这里定义你想传给前端哪些字段
        # 如果你的模型字段名和这里不一样，请核对 models.py
        fields = ['id', 'title', 'summary', 'content', 'create_time']