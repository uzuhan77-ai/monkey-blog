from django.urls import path
from .views import TestView, ArticleListView, ArticleDetailView

urlpatterns = [
    # 访问路径: /api/test/
    path('test/', TestView.as_view(), name= 'test'),
    path('article/list', ArticleListView.as_view(), name='article-list'),
    path('article/detail/<int:pk>/', ArticleDetailView.as_view(), name= 'article-detail')

]