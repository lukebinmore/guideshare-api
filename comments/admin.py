from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "post",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "post",
        "created_at",
        "updated_at",
    )
    search_fields = ("__all__",)
