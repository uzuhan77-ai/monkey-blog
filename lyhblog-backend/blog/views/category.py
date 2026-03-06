from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Category
from .. serializers import CategorySerializer

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many= True)
        return Response({
            "code": 200,
            "data": serializer.data,
            "message": "获取分类列表数据"
        })
