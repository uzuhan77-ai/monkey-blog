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