from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from .models import Profile
from . import serializers
from guideshareapi.permissions import IsOwnerOrReadOnly


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProfileDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        post_count=Count("owner__posts", distinct=True),
        following_count=Count("following", distinct=True),
        followers_count=Count("followers", distinct=True),
    )


class ProfileList(generics.ListAPIView):
    serializer_class = serializers.ProfileListSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["followers", "following"]
    ordering_fields = ["owner", "popularity"]

    def get_queryset(self):
        return Profile.objects.annotate(
            post_count=Count("owner__posts", distinct=True),
            popularity=Count(
                "owner__posts__post_votes",
                filter=Q(owner__posts__post_votes__vote=0),
                distinct=True,
            )
            - Count(
                "owner__posts__post_votes",
                filter=Q(owner__posts__post_votes__vote=1),
                distinct=True,
            ),
        ).order_by("popularity")


class SavedFollowing(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.SavedFollowingSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
