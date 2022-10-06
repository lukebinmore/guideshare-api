from rest_framework import generics, filters
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post
from . import serializers
from guideshareapi.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated


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

    def get_queryset(self):
        return Post.objects.annotate(
            likes_count=Count(Q(post_votes=0)),
            dislikes_count=Count(Q(post_votes=1))
        )


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()


class PostCreate(generics.CreateAPIView):
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
