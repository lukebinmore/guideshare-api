from rest_framework import serializers
from .models import Profile


class ProfileDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    post_count = serializers.ReadOnlyField(default=0)
    following_count = serializers.ReadOnlyField(default=0)
    followers_count = serializers.ReadOnlyField(default=0)

    def get_is_owner(self, obj):
        request = self.context["request"]
        return obj.owner == request.user

    def validate_picture(self, value):
        if value.size > 1024 * 1024 * 5:
            raise serializers.ValidationError(
                "Image is too large, please choose an image 5MB or smaller."
            )
        if value.image.width > 4096 or value.image.height > 4096:
            raise serializers.ValidationError(
                "Image is too large, maxium resolution is 4096px X 4096px."
            )
        return value

    class Meta:
        model = Profile
        fields = "__all__"


class ProfileListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    post_count = serializers.ReadOnlyField(default=0)
    followed = serializers.SerializerMethodField()

    def get_followed(self, obj):
        user = self.context["request"].user
        return True if obj.owner.followers.filter(owner=user) else False

    class Meta:
        model = Profile
        fields = (
            "id",
            "owner",
            "post_count",
            "picture",
            "created_at",
            "followed",
        )


class SavedFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["saved_posts", "following"]
