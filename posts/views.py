from rest_framework import generics, filters
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Post
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
    ordering_fields = [
        "title",
        "title_length",
        "created_at",
        "likes_count",
        "dislikes_count",
    ]
    filterset_fields = [
        "owner__profile__followers",
        "post_saves",
        "category",
        "wip",
    ]
    search_fields = ["title", "owner__username", "category__title"]

    queryset = Post.objects.annotate(
        likes_count=Count(
            "post_votes", filter=Q(post_votes__vote=0), distinct=True
        ),
        dislikes_count=Count(
            "post_votes", filter=Q(post_votes__vote=1), distinct=True
        ),
        title_length=Count("title"),
    ).order_by("-created_at")


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        likes_count=Count(
            "post_votes", filter=Q(post_votes__vote=0), distinct=True
        ),
        dislikes_count=Count(
            "post_votes", filter=Q(post_votes__vote=1), distinct=True
        ),
        comments_count=Count("post_comments", distinct=True),
    )


class PostCreate(generics.CreateAPIView):
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryList(generics.ListAPIView):
    serializer_class = serializers.CategoryListSerializer
    queryset = Category.objects.all().order_by("title")
    pagination_class = None
