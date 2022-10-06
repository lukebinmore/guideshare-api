from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from .models import Profile
from . import serializers
from guideshareapi.permissions import IsOwnerOrReadOnly


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProfileDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()


class ProfileList(generics.ListAPIView):
    serializer_class = serializers.ProfileListSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["owner__followers", "following"]
    ordering_fields = ["owner", "popularity"]

    def get_queryset(self):
        return (
            Profile.objects.exclude(owner=self.request.user)
            .annotate(
                popularity=Count(
                    "owner__posts__post_votes",
                    filter=Q(owner__posts__post_votes__vote=0),
                )
                - Count(
                    "owner__posts__post_votes",
                    filter=Q(owner__posts__post_votes__vote=1),
                )
            )
            .order_by("owner")
        )
