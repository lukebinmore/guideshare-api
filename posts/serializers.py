from rest_framework import serializers
from .models import Post
from votes.models import Vote


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile_id")
    likes_count = serializers.ReadOnlyField(default=0)
    like_id = serializers.SerializerMethodField()
    dislikes_count = serializers.ReadOnlyField(default=0)
    dislike_id = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField(default=0)

    def get_is_owner(self, obj):
        return self.context["request"].user == obj.owner

    def get_like_id(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            like = Vote.objects.filter(owner=user, post=obj, vote=0).first()
        return like.id if like else None

    def get_dislike_id(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            dislike = Vote.objects.filter(owner=user, post=obj, vote=1).first()
        return dislike.id if dislike else None

    def validate_cover_image(self, value):
        if value.size > 1024 * 1024 * 5:
            raise serializers.ValidationError(
                "Image is too large, please choose an image 5MB or smaller."
            )
        if value.width > 4096 or value.height > 2048:
            raise serializers.ValidationError(
                "Image is too large, maxium resolution is 4096px X 2048px."
            )
        return value

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    class Meta:
        model = Post
        fields = "__all__"


class PostListSerializer(serializers.ModelSerializer):
    likes_count = serializers.ReadOnlyField(default=0)
    dislikes_count = serializers.ReadOnlyField(default=0)
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "category",
            "cover_image",
            "likes_count",
            "dislikes_count",
            "profile_id",
        ]
