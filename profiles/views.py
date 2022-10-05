from rest_framework import generics
from .models import Profile
from . import serializers
from guideshareapi.permissions import IsOwnerOrReadOnly


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProfileDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
