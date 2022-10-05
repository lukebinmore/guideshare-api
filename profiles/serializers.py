from rest_framework import serializers
from .models import Profile


class ProfileDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    is_owner = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return obj.owner == request.user

    def get_post_count(self, obj):
        return 0

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers_count(self, obj):
        return obj.owner.followers.count()

    class Meta:
        model = Profile
        fields = "__all__"
