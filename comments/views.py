from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from guideshareapi.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Comment
from . import serializers


class CommentList(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["post"]
    queryset = Comment.objects.annotate(
        likes_count=Count(
            "comment_votes", filter=Q(comment_votes__vote=0), distinct=True
        ),
        dislikes_count=Count(
            "comment_votes", filter=Q(comment_votes__vote=1), distinct=True
        ),
    ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
