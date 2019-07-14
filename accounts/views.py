from rest_framework import generics
from .serializers import UserSerializer
from .models import User
from rest_framework.renderers import JSONRenderer


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [JSONRenderer]
    queryset = User.objects.all()
    serializer_class = UserSerializer
