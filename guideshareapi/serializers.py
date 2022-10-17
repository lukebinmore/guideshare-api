from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class CurrentUserSerializer(UserDetailsSerializer):
    profile_id = serializers.ReadOnlyField(source="profile.id")
    profile_picture = serializers.ReadOnlyField(source="profile.picture.url")
    is_admin = serializers.BooleanField(
        source="is_staff", read_only=True, default=False
    )

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            "profile_id",
            "profile_picture",
            "is_admin",
        )
