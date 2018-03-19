from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dog, UserPref, UserDog
from . import serializers


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class RetrieveUpdateUserPref(generics.RetrieveUpdateAPIView):
    queryset = UserPref.objects.all()
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


class GetUndecidedDog(generics.RetrieveAPIView):
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        user = self.request.user
        user_pref = UserPref.objects.get(user=user)
        queryset = Dog.objects.filter(
            gender__in=user_pref.gender,
            size__in=user_pref.size.split(','),
            age_group__in=user_pref.age
            ).filter(
                userdog__status='u',
                userdog__user_id=user.id
            ).order_by('pk')
        return queryset

    def get_object(self):
        pk_from_url = self.kwargs.get('pk')
        queryset = self.get_queryset()
        dog = queryset.filter(id__gt=pk_from_url).first()
        if dog is not None:
            return dog
        return queryset.first()

    def get(self, request, pk, format=None):
        dog = self.get_object()
        serializer = serializers.DogSerializer(dog)
        print("Length of queryset: %s " % len(self.get_queryset()))
        print(self.get_queryset())
        print("PK sent to Django: %s " % pk)
        # print("PK of dog sent back: %s " % dog.id)
        print("\n" * 2)
        if not dog:
            raise Http404
        return Response(serializer.data)

class GetLikedDog(generics.RetrieveAPIView):
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        user = self.request.user
        user_pref = UserPref.objects.get(user=user)
        queryset = Dog.objects.filter(
            gender__in=user_pref.gender,
            size__in=user_pref.size.split(','),
            age_group__in=user_pref.age
            ).filter(
                userdog__status='l',
                userdog__user_id=user.id
            ).order_by('pk')
        return queryset

    def get_object(self):
        pk_from_url = self.kwargs.get('pk')
        queryset = self.get_queryset()
        dog = queryset.filter(id__gt=pk_from_url).first()
        if dog is not None:
            return dog
        return queryset.first()

    def get(self, request, pk, format=None):
        dog = self.get_object()
        serializer = serializers.DogSerializer(dog)
        print("Length of queryset: %s " % len(self.get_queryset()))
        print(self.get_queryset())
        print("PK sent to Django: %s " % pk)
        # print("PK of dog sent back: %s " % dog.id)
        print("\n" * 2)
        if not dog:
            raise Http404
        return Response(serializer.data)
    

class GetDislikedDog(generics.RetrieveAPIView):
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        user = self.request.user
        user_pref = UserPref.objects.get(user=user)
        queryset = Dog.objects.filter(
            gender__in=user_pref.gender,
            size__in=user_pref.size.split(','),
            age_group__in=user_pref.age
            ).filter(
                userdog__status='d',
                userdog__user_id=user.id
            ).order_by('pk')
        return queryset

    def get_object(self):
        pk_from_url = self.kwargs.get('pk')
        queryset = self.get_queryset()
        dog = queryset.filter(id__gt=pk_from_url).first()
        if dog is not None:
            return dog
        return queryset.first()

    def get(self, request, pk, format=None):
        dog = self.get_object()
        serializer = serializers.DogSerializer(dog)
        print("Length of queryset: %s " % len(self.get_queryset()))
        print(self.get_queryset())
        print("PK sent to Django: %s " % pk)
        # print("PK of dog sent back: %s " % dog.id)
        print("\n" * 2)
        if not dog:
            raise Http404
        return Response(serializer.data)


class LikeDog(generics.UpdateAPIView):
    queryset = Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        dog = get_object_or_404(Dog, pk=self.kwargs.get('pk'))
        return dog

    def put(self, request, *args, **kwargs):
        dog = self.get_object()
        obj, exists = UserDog.objects.get_or_create(
            user=self.request.user,
            dog=dog,
            defaults={
                'user': self.request.user,
                'dog': dog,
                'status': 'l'
            }
            )
        if obj:
            obj.status = 'l'
            obj.save()
        return Response("Liked!", status=status.HTTP_201_CREATED)

class DislikeDog(generics.UpdateAPIView):
    queryset = Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        dog = get_object_or_404(Dog, pk=self.kwargs.get('pk'))
        return dog

    def put(self, request, *args, **kwargs):
        dog = self.get_object()
        obj, exists = UserDog.objects.get_or_create(
            user=self.request.user,
            dog=dog,
            defaults={
                'user': self.request.user,
                'dog': dog,
                'status': 'd'
            }
            )
        if obj:
            obj.status = 'd'
            obj.save()
        return Response("Disliked!", status=status.HTTP_201_CREATED)


class UndecideDog(generics.UpdateAPIView):
    queryset = Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self):
        dog = get_object_or_404(Dog, pk=self.kwargs.get('pk'))
        return dog

    def put(self, request, *args, **kwargs):
        dog = self.get_object()
        obj, exists = UserDog.objects.get_or_create(
            user=self.request.user,
            dog=dog,
            defaults={
                'user': self.request.user,
                'dog': dog,
                'status': 'u'}
            )
        if obj:
            obj.status = 'u'
            obj.save()
        return Response("Undecided!", status=status.HTTP_201_CREATED)
