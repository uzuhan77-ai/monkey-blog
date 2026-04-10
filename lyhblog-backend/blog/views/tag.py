from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Tag
from ..serializers import TagSerializer

class TagListView(APIView):
    def get(self,request):
        tags=Tag.objects.all().order_by('-id')
        serializer =TagSerializer(tags, many=True)
        return Response({
            "code":200,
            "message": "获取列表标签成功",
            "data":serializer.data
        })

class TagAddView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self,request):
        name = (request.data.get('name') or '').strip()

        if not name:
            return Response({
                "code": 400,
                "message": "标签名称不能为空"
            },status= 400)

        if Tag.objects.filter(name=name).exists():
            return Response({
                "code": 400,
                "message": "标签已存在"
            },status=400)

        tag = Tag.objects.create(name=name)
        return Response({
            "code": 200,
            "message":"标签新增成功",
            "data":TagSerializer(tag).data
        })

class TagUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self,request):
        tag_id = request.data.get('id')
        name = (request.data.get('name') or '').strip()

        if not tag_id:
            return Response({
                "code": 400,
                "message": "缺少标签 id"
            }, status=400)

        if not name:
            return Response({
                "code": 400,
                "message": "标签名称不能为空"
            }, status=400)

        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return Response({
                "code": 404,
                "message": "标签不存在"
            }, status=404)

        if Tag.objects.filter(name=name).exclude(id=tag_id).exists():
            return Response({
                "code":400,
                "message":"标签已存在"
            })

        tag.name=name
        tag.save()

        return Response({
            "code":200,
            "message":"标签修改成功",
            "data":TagSerializer(tag).data
        })

class TagDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self,request):
        tag_id = request.data.get('id')

        if not tag_id:
            return Response({
                "code":400,
                "message": "缺少标签ID"
            },status=400)

        try:
            tag = Tag.objects.get(id = tag_id)
        except Tag.DoesNotExist:
            return Response({
                "code": 404,
                "message": "标签不存在"
            },status=400)

        tag.delete()
        return Response({
            "code": 200,
            "message": "标签删除成功"
        })