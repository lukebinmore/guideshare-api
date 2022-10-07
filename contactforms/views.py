from rest_framework import generics
from .models import ContactForm
from . import serializers


class ContactForm(generics.CreateAPIView):
    serializer_class = serializers.ContactFormSerializer
    queryset = ContactForm.objects.all()
