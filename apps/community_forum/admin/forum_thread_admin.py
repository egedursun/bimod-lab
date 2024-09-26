from django.contrib import admin

from apps.community_forum.models import ForumThread


@admin.register(ForumThread)
class ForumThreadAdmin(admin.ModelAdmin):
    list_display = (
        "title", "category", "created_by", "created_at", "updated_at", "is_closed",
    )
    search_fields = ("title", "category__name", "created_by__username",)
    list_filter = ("created_at", "updated_at", "is_closed",)
    ordering = ("-created_at",)
