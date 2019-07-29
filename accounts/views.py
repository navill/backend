from django.shortcuts import render
from rest_framework import generics

from .models import User
from .serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import *


# Create your views here.


# class UserView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (AllowAny,)


# class SomeView(SomeGenericView): # 회원가입 등등 인증 없이도 동작하도록 설정할 떄 해당 위치에 아래 코드 삽입
#     permission_classes = (AllowAny,)


# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     renderer_classes = [JSONRenderer]  # 이 코드는 http://127.0.0.1:8000/user/?format=json 주소에 format 인자를 추가해 결정
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (AllowAny,)


class UserUpdate(generics.UpdateAPIView):
    """
    UserUpdate

    계정을 수정합니다.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UserDelete(generics.DestroyAPIView):
    """
    UserDelete

    계정을 삭제합니다.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )


# class UserListAPI(generics.ListAPIView):  # user list 값 받기?
#     queryset = get_user_model().objects.all()
#     serializer_class = UserListSerializer
#     # filterset_fields = ('id',)  # 필터 기능을 동작시키고 싶으면 해당 코드 이 위치에 작성
#     permission_classes = (AllowAny,)
#
#     # 본인에 관한 정보만 노출되도록 설정코드작성 - 관리자는 전체목록 확인 가능
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         if not self.request.user.is_staff:
#             queryset = queryset.filter(pk=self.request.user.id)
#         return queryset


class UserCreateAPI(generics.CreateAPIView):  # user create 값 받기?
    """
    UserCreateAPI

    계정을 생성합니다.
    """
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

