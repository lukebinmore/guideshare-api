from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "first_name",
        "last_name",
        "dob",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "dob",
        "created_at",
        "updated_at",
    )
    search_fields = ("__all__",)
