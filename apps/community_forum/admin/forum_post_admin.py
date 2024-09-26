from django.contrib import admin

from apps.community_forum.models import ForumPost


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = (
        "thread", "content", "created_by", "created_at", "updated_at", "is_verified",
    )
    search_fields = ("thread__title", "content", "created_by__username",)
    list_filter = ("created_at", "updated_at", "is_verified",)
    ordering = ("-created_at",)
