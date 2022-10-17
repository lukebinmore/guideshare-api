from rest_framework import serializers
from .models import ContactForm


class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = [
            "title",
            "username",
            "email",
            "first_name",
            "last_name",
            "reason",
            "content",
        ]
