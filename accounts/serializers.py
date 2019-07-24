from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User


class UserSerializer(serializers.ModelSerializer):  # rest_framework list 에 뜨는 정보
    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'password', 'birthDate', 'phoneNumber', 'preferTheater', 'watchedMovie',
                  'wishMovie']


class UserListSerializer(serializers.ModelSerializer):  # 유저 목록 출력을 위한 시리얼 라이저
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'name', 'password', 'birthDate', 'phoneNumber', 'preferTheater', 'watchedMovie',
                  'wishMovie']


# 회원 가입 할 때 필요한 필드들에 관한 시리얼라이저
# 유저 생성 할때 입력받을 필드
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'birthDate', 'phoneNumber', 'preferTheater', 'watchedMovie',
                  'wishMovie']
        # fields = '__all__'

    # password 암호화 = 회원가입 기능 실행 시 리스트 목록에 password 암호화 되어 나타남
    def create(self, validated_data):
        user = get_user_model().objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.is_active = True
        user.save()

        return user

