from rest_framework import serializers
from .models import Profile


class ProfileDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context["request"]
        return obj.owner == request.user

    def get_post_count(self, obj):
        return obj.owner.posts.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers_count(self, obj):
        return obj.owner.followers.count()

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 5:
            raise serializers.ValidationError(
                "Image is too large, please choose an image 5MB or smaller."
            )
        if value.width > 4096 or value.height > 4096:
            raise serializers.ValidationError(
                "Image is too large, maxium resolution is 4096px X 4096px."
            )
        return value

    class Meta:
        model = Profile
        fields = "__all__"


class ProfileListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    post_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    followed = serializers.SerializerMethodField()

    def get_post_count(self, obj):
        return obj.owner.posts.count()

    def get_followers_count(self, obj):
        return obj.owner.followers.count()

    def get_followed(self, obj):
        request = self.context["request"]
        return (
            True if obj.owner.followers.filter(owner=request.user) else False
        )

    class Meta:
        model = Profile
        fields = (
            "id",
            "owner",
            "post_count",
            "followers_count",
            "picture",
            "created_at",
            "followed",
        )
