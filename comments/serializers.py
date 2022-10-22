from rest_framework import serializers
from .models import Comment
from votes.models import Vote


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
        return self.context["request"].user == obj.owner

    def get_like_id(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            like = Vote.objects.filter(owner=user, comment=obj, vote=0).first()
        return like.id if like else None

    def get_dislike_id(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            dislike = Vote.objects.filter(
                owner=user, comment=obj, vote=1
            ).first()
        return dislike.id if dislike else None

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    class Meta:
        model = Comment
        fields = "__all__"


class CommentDetailSerializer(CommentSerializer):
    post = serializers.ReadOnlyField(source="post.id")
