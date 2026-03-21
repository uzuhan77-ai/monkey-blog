from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Comment
from .. serializers import CommentSerializer

#1、 获取某篇文章的评论列表(GET)
class CommentListView(APIView):
    def get(self,request):
        article_id = request.GET.get('article_id')
        if not article_id:
            return Response({
                "code": 400,
                "message": "缺少文章id",
            },status= 400)


        #过滤出这篇文章的所有评论
        comments = Comment.objects.filter(article_id= article_id)
        serialize = CommentSerializer(comments, many= True)
        return Response({
            "code": 200,
            "message": "获取评论列表成功",
            "data": serialize.data,
        })


#2、 发表评论 (POST) - [重点: 必须登录]
class CommentAddView(APIView):
    # 👇 重点！加上这行，DRF会自动拦截未登录的请求！
    # 这就是和咱们 Day 6 前端 Axios 拦截器“双剑合璧”的后端守卫！
    permission_classes = [IsAuthenticated]


    def  post(self, request):
        article_id = request.data.get('article_id')
        content = request.data.get('content')

        if not article_id or not content:
            return Response({
                "code": 400,
                "message": "参数不完整",
            },status= 400)

        #重点: 加了IsAuthenticated,走到这里的 request.user 绝对是已经完全合法登录的用户
        comment = Comment.objects.create(
            article_id = article_id,
            user = request.user,
            content = content,
        )

        #把刚建好的评论序列话返回给前端，前端可以直接把它塞进列表中展示
        serializer = CommentSerializer(comment)
        return Response({
            "code":200,
            "message": "评论发表成功",
            "data": serializer.data
        })

#     3.后台：获取所有评论列表（POST，带分页）
class AdminCommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        current = int(request.data.get('current',1))
        size = int(request.data.get('size',10))

        #获取所有评论
        queryset = Comment.objects.all()
        total = queryset.count()
        # 场景
        # B：用户点到了第2页(current=2, size=10)
        # start = (2 - 1) * 10 = 10
        # end = 10 + 10 = 20
        start = (current - 1) * size
        end = start + size

        comments = queryset[start:end]
        serialize = CommentSerializer(comments, many= True)

        return Response({
            "code": 200,
            "message": "获取所有评论成功",
            "total": total,
            "data": serialize.data
        })
#4.后台：删除评论（POST）
class AdminCommentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        comment_id = request.data.get('id')
        if not comment_id :
            return Response({
                "code": 400,
                "message":"缺少评论id",
            },status = 400)

        try:
            comment = Comment.objects.get(id = comment_id)
            comment.delete()
            return Response({
                "code": 200,
                "message": "评论删除成功",
            })
        except Comment.DoesNotExist:
            return Response({
                "code": 404,
                "message": "评论不存在"
            },status=404)













