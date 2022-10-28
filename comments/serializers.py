from rest_framework import serializers
from .models import Comment
from votes.models import Vote


# Serializer for a list of comments
class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="owner.profile.id")
    profile_picture = serializers.ReadOnlyField(
        source="owner.profile.picture.url"
    )
    likes_count = serializers.ReadOnlyField(default=0)
    like_id = serializers.SerializerMethodField()
    dislikes_count = serializers.ReadOnlyField(default=0)
    dislike_id = serializers.SerializerMethodField()

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
            like = Vote.objects.filter(owner=user, comment=obj, vote=0).first()
            return like.id if like else None
        return None

    def get_dislike_id(self, obj):
        """
        If the user is authenticated, return the id of the dislike if it
        exists, otherwise return None

        :param obj: The object that the serializer is being applied to
        :return: The id of the vote object.
        """
        user = self.context["request"].user
        if user.is_authenticated:
            dislike = Vote.objects.filter(
                owner=user, comment=obj, vote=1
            ).first()
            return dislike.id if dislike else None
        return None

    def perform_create(self, serializer):
        """
        It sets the owner on save

        :param serializer: The serializer instance that should be saved
        """
        serializer.save(owner=self.request.user)

    class Meta:
        model = Comment
        fields = "__all__"


# Serializer for comment details
class CommentDetailSerializer(CommentSerializer):
    post = serializers.ReadOnlyField(source="post.id")
