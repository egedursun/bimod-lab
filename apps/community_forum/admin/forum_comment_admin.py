from django.contrib import admin

from apps.community_forum.models import ForumComment


@admin.register(ForumComment)
class ForumCommentAdmin(admin.ModelAdmin):
    list_display = (
        "post", "content", "created_by", "created_at", "updated_at"
    )
    search_fields = ("post__content", "content", "created_by__username",)
    list_filter = ("created_at", "updated_at",)
    ordering = ("-created_at",)
