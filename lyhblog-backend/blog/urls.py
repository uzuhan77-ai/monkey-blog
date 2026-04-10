from django.urls import path

from .views import (TestView, ArticleListView, ArticleDetailView,ArticleAddView, ArticleDeleteView, ArticleUpdateView,
                    LoginView, RegisterView
                    )
from .views.category import CategoryListView, CategoryAddView, CategoryUpdateView, CategoryDeleteView

from .views.comment import CommentListView, CommentAddView,CommentDeleteView,CommentAllView
from .views.tag import TagListView, TagAddView, TagUpdateView, TagDeleteView



urlpatterns = [
    # 访问路径: /api/test/
    path('test/', TestView.as_view(), name= 'test'),

    path('user/login/', LoginView.as_view(), name='login'),
    path('user/register/', RegisterView.as_view(), name='register'),

    path('article/listArticle/', ArticleListView.as_view(), name='article-list'),
    path('article/getArticleById/', ArticleDetailView.as_view(), name= 'article-detail'),
    path('article/add/', ArticleAddView.as_view(), name= 'article-add'),
    path('article/delete/', ArticleDeleteView.as_view(), name=' article-delete'),
    path('article/update/', ArticleUpdateView.as_view(), name=' article-update'),

    path('category/list/', CategoryListView.as_view()),
    path('category/add/', CategoryAddView.as_view()),
    path('category/update/', CategoryUpdateView.as_view()),
    path('category/delete/', CategoryDeleteView.as_view()),

    path('tag/list/', TagListView.as_view()),
    path('tag/add/', TagAddView.as_view()),
    path('tag/update/',TagUpdateView.as_view()),
    path('tag/delete/',TagDeleteView.as_view()),


    path('comment/list/', CommentListView.as_view()),
    path('comment/add/', CommentAddView.as_view()),
    path('comment/delete/',CommentDeleteView.as_view()),
    path('comment/all/',CommentAllView.as_view())

]