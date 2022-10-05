from rest_framework import generics
from rest_framework.response import Response
from .models import Profile
from . import serializers


class ProfileSingle(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProfileSingleSerializer
    queryset = Profile.objects.all()
