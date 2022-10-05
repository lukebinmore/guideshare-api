from rest_framework import generics, filters
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post
from . import serializers
from guideshareapi.permissions import IsOwnerOrReadOnly


class PostList(generics.ListAPIView):
    serializer_class = serializers.PostListSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created_at", "likes_count", "dislikes_count"]
    filterset_fields = ["owner__followers", "post_saves"]
    search_fields = ["title", "owner__username", "category__title"]
    queryset = Post.objects.annotate(
        likes_count=Count("likes"), dislikes_count=Count("dislikes")
    )


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
