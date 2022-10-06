from django.db import IntegrityError
from rest_framework import serializers
from .models import Vote


class VoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Vote
        fields = ["id", "owner", "post", "comment", "vote"]
    
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': "Duplicate entry"
            })
