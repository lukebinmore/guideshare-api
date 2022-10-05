from django.contrib import admin
from .models import Post, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "category",
        "post_likes",
        "post_dislikes",
    )
    list_filter = (
        "owner",
        "category",
        "wip",
        "created_at",
        "updated_at",
    )
    search_fields = ("__all__",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title",)
