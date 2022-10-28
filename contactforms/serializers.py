from rest_framework import serializers
from .models import ContactForm


# Serializer for contact forms
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
