from rest_framework import serializers
from .models import Profile


# Serializer for profile details
class ProfileDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    post_count = serializers.ReadOnlyField(default=0)
    following_count = serializers.ReadOnlyField(default=0)
    followers_count = serializers.ReadOnlyField(default=0)

    def get_is_owner(self, obj):
        """
        If the user is the owner of the object, return True, else return False

        :param obj: The object that is being serialized
        :return: The owner of the object
        """
        request = self.context["request"]
        return obj.owner == request.user

    def validate_picture(self, value):
        """
        If the image is larger than 5MB or the image is larger than 4096px X
        4096px, then raise a validation error

        :param value: The image file that was uploaded
        :return: The value of the image.
        """
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


# Serializer for a list of profiles
class ProfileListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    post_count = serializers.ReadOnlyField(default=0)

    class Meta:
        model = Profile
        fields = (
            "id",
            "owner",
            "post_count",
            "picture",
            "created_at",
        )


# Serializer for a users saved posts and followed profiles
class SavedFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["saved_posts", "following"]
