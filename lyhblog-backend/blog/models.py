
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length= 50 ,verbose_name= "标签名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name= "标签"
        verbose_name_plural= "标签"

class Category(models.Model):
    name = models.CharField(max_length= 50 ,verbose_name= "分类名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name= "分类"
        verbose_name_plural= "分类"



class Article(models.Model):
    #文章标题
    title= models.CharField(max_length=100,verbose_name="标题")
    #文章摘要
    summary= models.TextField(blank=True,verbose_name="摘要")
    #文章内容
    content= models.TextField(verbose_name="内容")
    #创建时间
    create_time= models.DateTimeField(default=timezone.now, verbose_name="创建时间")

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null= True,
        blank= True,
        verbose_name= "分类"
    )

    tags = models.ManyToManyField(
        Tag,
        blank = True,
        verbose_name="标签"
    )

    # 这是为了让后台显示文章标题，而不是 "Article object (1)"
    def __str__(self):
        return self.title

    class Meta:
        verbose_name='文章'
        verbose_name_plural='文章'
        ordering= ['-create_time']



class Comment(models.Model):
    #评论正文
    content = models.TextField(verbose_name= "评论内容")
    #评论时间
    create_time = models.DateTimeField(default= timezone.now, verbose_name="评论时间")

    #关联文章 on_delete = models.CASCADE 表示如果文章被删除，这篇文章的评论也跟着全删除
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name= "所属文章")

    #关联用户 ：记录这条评论是谁发出的
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name= "评论用户")

    def __str__(self):
        # 这样在后台能清晰看到是谁评论
        return f"{self.user.username}  评论了 {self.article.title} "

    class Meta:
        verbose_name= "评论"
        verbose_name_plural= "评论"
        ordering = ['-create_time'] #最新评论排在最前面





