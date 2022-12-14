from django.contrib import admin
from .models import Vote


# Registering the model Vote to the admin site.
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "post",
        "comment",
        "vote",
        "created_at",
    )
    list_filter = (
        "owner",
        "post",
        "comment",
        "vote",
        "created_at",
    )
    search_fields = ("__all__",)
