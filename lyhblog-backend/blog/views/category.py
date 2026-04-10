from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..models import Category
from .. serializers import CategorySerializer

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all().order_by('id')
        serializer = CategorySerializer(categories, many= True)
        return Response({
            "code": 200,
            "data": serializer.data,
            "message": "获取分类列表数据"
        })


class CategoryAddView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self,request):
        name = (request.data.get('name') or '').strip()

        if not name:
            return Response({
                "code": 400,
                "message": "分类名称不能为空",
            },status=400)

        if Category.objects.filter(name=name).exists():
            return Response({
                "code": 400,
                "message": "分类已存在"
            }, status=400)

        category = Category.objects.create(name=name)
        return Response({
            "code": 200,
            "message": "分类新增成功",
            "data": CategorySerializer(category).data
        })



class CategoryUpdateView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]

    def post(self,request):
        category_id = request.data.get('id')
        name = (request.data.get('name') or '').strip()

        if not category_id:
            return Response({
                "code": 400,
                "message": "缺少分类 id"
            }, status=400)

        if not name:
            return Response({
                "code": 400,
                "message": "分类名称不能为空"
            }, status=400)

        try:
            category = Category.objects.get(id=category_id)

        except Category.DoesNotExist:
            return Response({
                "code": 404,
                "message": "分类不存在"
            }, status=404)


        if Category.objects.filter(name=name).exclude(id=category_id).exists():
            return Response({
                "code": 400,
                "message": "分类名称已存在"
            }, status=400)
        category.name=name
        category.save()

        return Response({
            "code":200,
            "message":"分类修改成功",
            "data":CategorySerializer(category).data
        })


class CategoryDeleteView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]

    def post(self,request):
        category_id = request.data.get('id')

        if not category_id:
            return Response({
                "code": 400,
                "message": "缺少分类 id"
            }, status=400)


        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({
                "code": 404,
                "message": "分类不存在"
            }, status=404)

        category.delete()

        return Response({
            "code": 200,
            "message": "分类删除成功"
        })


