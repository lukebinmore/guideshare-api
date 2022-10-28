from django.db import IntegrityError
from rest_framework import serializers
from .models import Vote


# Serializer for votes
class VoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Vote
        fields = ["id", "owner", "post", "comment", "vote"]

    def create(self, validated_data):
        """
        If the super() method raises an IntegrityError, then raise a
        ValidationError

        :param validated_data: The data that has been validated and is ready
        to be saved
        :return: The super().create(validated_data) is returning the instance
        of the model.
        """
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"detail": "Duplicate entry"})
