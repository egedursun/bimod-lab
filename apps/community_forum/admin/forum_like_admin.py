from apps.community_forum.models import ForumLike
from django.contrib import admin


@admin.register(ForumLike)
class ForumLikeAdmin(admin.ModelAdmin):
    list_display = (
        "user", "created_at"
    )
    search_fields = ("comment",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)
