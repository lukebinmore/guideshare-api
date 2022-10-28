from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from .models import Profile
from . import serializers
from guideshareapi.permissions import IsOwnerOrReadOnly


# This class is a generic view that allows us to retrieve, update, and delete a
# profile
class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ProfileDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    # Annotating the queryset with the number of posts, following, and
    # followers.
    queryset = Profile.objects.annotate(
        post_count=Count("owner__posts", distinct=True),
        following_count=Count("following", distinct=True),
        followers_count=Count("followers", distinct=True),
    )

    def perform_destroy(self, obj):
        """
        It deletes the object and then sets the user's is_active field to False

        :param obj: The object that is being deleted
        """
        user = self.request.user
        obj.delete()
        user.is_active = False
        user.save()


# This class is a list view that returns a list of profiles, and allows
# filtering by followers, following, ordering by owner, and ordering by
# popularity.
class ProfileList(generics.ListAPIView):
    serializer_class = serializers.ProfileListSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["followers", "following"]
    ordering_fields = ["owner", "popularity"]

    def get_queryset(self):
        """
        Get all the profiles, annotate them with the number of posts they have
        and the popularity of their posts, and order them by popularity
        :return: A queryset of Profile objects, annotated with the number of
        posts and the popularity of the user.
        """
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


# This class will allow us to retrieve and update users saved posts and
# following fields
class SavedFollowing(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.SavedFollowingSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
