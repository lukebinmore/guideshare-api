from django.contrib import admin
from .models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_filter = (
        "owner",
        "post",
        "comment",
        "vote",
        "created_at",
    )
    search_fields = ("__all__",)