from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from .serializers import UserSerializer
from .models import User
from rest_framework.renderers import JSONRenderer


# class UserView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_description="description")
    def post(self, request):
        pass


# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     renderer_classes = [JSONRenderer]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
