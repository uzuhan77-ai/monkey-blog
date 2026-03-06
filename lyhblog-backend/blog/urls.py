from django.urls import path

from .views import TestView, ArticleListView, ArticleDetailView, LoginView, RegisterView, CategoryListView

urlpatterns = [
    # 访问路径: /api/test/
    path('test/', TestView.as_view(), name= 'test'),
    path('article/listArticle/', ArticleListView.as_view(), name='article-list'),
    path('article/getArticleById/', ArticleDetailView.as_view(), name= 'article-detail'),
    path('user/login/', LoginView.as_view(), name='login'),
    path('user/register/', RegisterView.as_view(), name='register'),
    path('category/listCategory/', CategoryListView.as_view(), name='category-list')

]