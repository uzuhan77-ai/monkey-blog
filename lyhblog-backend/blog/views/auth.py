# 这里只保留登录和测试需要的 import
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# 测试接口
class TestView(APIView):
    def get(self, request):
        return Response({'message': 'hello', 'code': 200}, status=status.HTTP_200_OK)


# 登录接口
class LoginView(APIView):
    def post(self, request):
        account = request.data.get('account')
        password = request.data.get('password')

        if not account or not password:
            return Response({"code": 400, "message": "账号和密码不能为空"}, status=400)

        user = authenticate(username= account,password= password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "code": 200,
                "message": "登录成功!",
                "token": token.key
            })



        return Response({"code": 400, "message": "账号或密码错误"}, status=400)



class RegisterView(APIView):
    def post(self, request):
        account= request.data.get('account')
        password= request.data.get('password')
        if not account or not password:
            return Response({
                "code": 400,
                "message": "账号和密码不能为空",
            },status=400)

        if User.objects.filter(username= account).exists():
            return Response({
                "code": 400,
                "message": "用户名已存在"
            },status=400)

        user= User.objects.create_user(username= account,password= password)

        return Response({
            "code":200,
            "message": "登录成功"
        })