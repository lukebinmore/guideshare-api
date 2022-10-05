from rest_framework import generics
from django.db.models import Count
from .models import Profile
from . import serializers
from guideshareapi.permissions import IsOwnerOrReadOnly


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProfileDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()


class ProfileList(generics.ListAPIView):
    serializer_class = serializers.ProfileListSerializer

    def get_queryset(self):
        return (
            Profile.objects.exclude(owner=self.request.user)
            .annotate(
                popularity=Count("owner__liked_posts")
                - Count("owner__disliked_posts")
            )
            .order_by("popularity")
        )
