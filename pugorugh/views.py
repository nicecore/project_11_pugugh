from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
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


class RetrieveUpdateUserPref(generics.RetrieveUpdateAPIView):
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            user=self.request.user)

    def put(self, request, *args, **kwargs):
        user_pref = self.get_object()
        pref_serializer = serializers.UserPrefSerializer(user_pref, request.data)
        if pref_serializer.is_valid():
            print(request.data)
            pref_serializer.save()
            return Response(pref_serializer.data)
        print(pref_serializer.errors)
        return Response(pref_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
