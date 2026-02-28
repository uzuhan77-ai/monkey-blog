from django.urls import path

from .views import TestView, ArticleListView, ArticleDetailView, LoginView, RegisterView

urlpatterns = [
    # 访问路径: /api/test/
    path('test/', TestView.as_view(), name= 'test'),
    path('article/listArticle/', ArticleListView.as_view(), name='article-list'),
    path('article/getArticleById/', ArticleDetailView.as_view(), name= 'article-detail'),
    path('appone/login/', LoginView.as_view(), name='login'),
    path('appone/register/', RegisterView.as_view(), name='register')

]