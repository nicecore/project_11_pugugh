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


class ListDog(APIView):
    def get(self, request, format=None):
        dogs = Dog.objects.all()
        serializer = serializers.DogSerializer(dogs, many=True)
        return Response(serializer.data)


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




class GetADog(generics.RetrieveAPIView):

    queryset = Dog.objects.all()
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        user_pref = UserPref.objects.get(user=self.request.user)
        queryset = Dog.objects.filter(
            gender__in=user_pref.gender,
            size__in=user_pref.size
        ).exclude(
            Q(user_dog__status='l') | Q(user_dog__status='d')
        ).order_by('pk')
        return queryset

    def get_object(self):
        # Get a dog object -- but where does the pk in kwargs come from???
        dog_id = self.kwargs.get('pk')
        if not self.get_queryset():
            raise Http404
        dog = self.get_queryset().filter(id__gt=dog_id).first()
        if dog is not None:
            return dog
        else:
            return self.get_queryset().first()

    def get(self, request, pk, format=None):
        dog = self.get_object()
        serializer = serializers.DogSerializer(dog)
        return Response(serializer.data)









# class GetNextUndecidedDog(APIView):

#     def get_queryset(self):
#         """Return a queryset of only the dogs
#         that match the user's preferences.
#         """

#         # Get the user from the request
#         user = self.request.user

#         # Get the user's preferences
#         prefs = get_object_or_404(UserPref, user=user)

#         # Define the queryset filtered by user preferences (except age range - still need to do)
#         # and by UserDog status and UserDog User
#         dogs = Dog.objects.filter(
#             gender__in=user_prefs.gender,
#             size__in=user_prefs.size,
#             userdog__status='u',
#             userdog__user=user
#         )
#         return dogs

#     def get_object(self):
#         # Get the dogs queryset from get_queryset() above

#         dogs = self.get_queryset()

#         # Return the first object in the queryset
#         dog = dogs.first()
#         return dog

#     def get(self, request, pk, format=None):
#         next_dog = self.get_object()
#         serializer = serializers.DogSerializer(next_dog)
#         return Response(serializer.data)














