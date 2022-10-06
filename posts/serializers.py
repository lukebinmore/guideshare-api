from rest_framework import serializers
from .models import Post
from votes.models import Vote


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    likes_count = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    dislike_id = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.post_votes.filter(vote=0).count()

    def get_like_id(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            like = Vote.objects.filter(owner=user, post=obj, vote=0).first()
        return like.id if like else None

    def get_dislikes_count(self, obj):
        return obj.post_votes.filter(vote=1).count()

    def get_dislike_id(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            dislike = Vote.objects.filter(owner=user, post=obj, vote=1).first()
        return dislike.id if dislike else None

    def get_comments_count(self, obj):
        return obj.post_comments.count()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    class Meta:
        model = Post
        fields = "__all__"


class PostListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Post
        fields = [
            "id",
            "owner",
            "title",
            "category",
            "cover_image",
            "created_at",
        ]
