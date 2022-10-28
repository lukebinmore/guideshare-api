from rest_framework import serializers
from .models import Category, Post
from votes.models import Vote


# Serializer for post details
class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_picture = serializers.ReadOnlyField(
        source="owner.profile.picture.url"
    )
    category_title = serializers.ReadOnlyField(source="category.title")
    likes_count = serializers.ReadOnlyField(default=0)
    like_id = serializers.SerializerMethodField()
    dislikes_count = serializers.ReadOnlyField(default=0)
    dislike_id = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField(default=0)

    def get_is_owner(self, obj):
        """
        If the user making the request is the same as the owner of the object,
        return True. Otherwise, return False

        :param obj: The object that the serializer is being applied to
        :return: The user that is logged in is being compared to the owner of
        the object.
        """
        return self.context["request"].user == obj.owner

    def get_like_id(self, obj):
        """
        If the user is authenticated, return the id of the like if it exists,
        otherwise return None

        :param obj: The object that the serializer is being used to serialize
        :return: The id of the like object if it exists, otherwise None.
        """
        user = self.context["request"].user
        if user.is_authenticated:
            like = Vote.objects.filter(owner=user, post=obj, vote=0).first()
            return like.id if like else None
        return None

    def get_dislike_id(self, obj):
        """
        If the user is authenticated, return the id of the dislike if it
        exists, otherwise return None

        :param obj: The object that the serializer is being used to serialize
        :return: The id of the vote object.
        """
        user = self.context["request"].user
        if user.is_authenticated:
            dislike = Vote.objects.filter(owner=user, post=obj, vote=1).first()
            return dislike.id if dislike else None
        return None

    def validate_cover_image(self, value):
        """
        If the image is larger than 5MB or larger than 4096px X 2048px, raise a
        validation error

        :param value: The image file
        :return: The value is being returned.
        """
        if value.size > 1024 * 1024 * 5:
            raise serializers.ValidationError(
                "Image is too large, please choose an image 5MB or smaller."
            )
        if value.image.width > 4096 or value.image.height > 2048:
            raise serializers.ValidationError(
                "Image is too large, maxium resolution is 4096px X 2048px."
            )
        return value

    def perform_create(self, serializer):
        """
        It sets the owner on save

        :param serializer: The serializer instance that should be saved
        """
        serializer.save(owner=self.request.user)

    class Meta:
        model = Post
        fields = "__all__"


# Serializer for a list of posts
class PostListSerializer(serializers.ModelSerializer):
    likes_count = serializers.ReadOnlyField(default=0)
    dislikes_count = serializers.ReadOnlyField(default=0)
    category_title = serializers.ReadOnlyField(source="category.title")

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "category_title",
            "cover_image",
            "wip",
            "likes_count",
            "dislikes_count",
        ]


# Serializer for a list of categories
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]
