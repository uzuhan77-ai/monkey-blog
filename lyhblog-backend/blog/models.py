

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