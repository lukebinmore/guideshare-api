from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from guideshareapi.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Comment
from . import serializers


# This class is a list view of all comments, and it allows you to create new
# comments
class CommentList(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["post"]
    # Annotating the queryset with the number of likes and dislikes.
    queryset = Comment.objects.annotate(
        likes_count=Count(
            "comment_votes", filter=Q(comment_votes__vote=0), distinct=True
        ),
        dislikes_count=Count(
            "comment_votes", filter=Q(comment_votes__vote=1), distinct=True
        ),
    ).order_by("-created_at")

    def perform_create(self, serializer):
        """
        The function is called when a POST request is made to the view.

        The function takes the serializer as an argument.

        The function saves the serializer and sets the owner field to the
        current user

        :param serializer: The serializer instance that should be saved
        """
        serializer.save(owner=self.request.user)


# This class is a generic view that allows us to retrieve, update, and delete a
# specific comment
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
