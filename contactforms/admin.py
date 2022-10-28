from django.contrib import admin
from .models import ContactForm


# Registering the model ContactForm to the admin site.
@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = [
        "reason",
        "status",
        "email",
        "created_at",
    ]
    list_filter = [
        "reason",
        "status",
        "created_at",
    ]
    search_fields = ("__all__",)
