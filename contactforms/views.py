from rest_framework import generics
from .models import ContactForm
from . import serializers


# A class based view that creates a new contact form.
class ContactForm(generics.CreateAPIView):
    serializer_class = serializers.ContactFormSerializer
    queryset = ContactForm.objects.all()
