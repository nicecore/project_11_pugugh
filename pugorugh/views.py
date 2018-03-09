from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers



class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class ListDog(APIView):
    def get(self, request, format=None):
        dogs = models.Dog.objects.all()
        serializer = serializers.DogSerializer(dogs, many=True)
        return Response(serializer.data)