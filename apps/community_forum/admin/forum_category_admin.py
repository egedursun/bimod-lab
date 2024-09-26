from django.contrib import admin

from apps.community_forum.models import ForumCategory


@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name", "slug", "created_at", "updated_at",
    )
    search_fields = ("name", "description", "slug",)
    list_filter = ("created_at", "updated_at",)
    ordering = ("-created_at",)
