from rest_framework import serializers
from .models import ContactForm


class ContactFormSerializer(serializers.ModelSerializer):
    def perform_create(self, serializer):
        serializer.save(status=0)

    class Meta:
        model = ContactForm
        fields = "__all__"
