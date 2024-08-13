from django.contrib import admin
from .models import ForumCategory, ForumThread, ForumPost, ForumComment


# Register your models here.

@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name", "slug", "created_at", "updated_at",
    )
    search_fields = ("name", "description", "slug",)
    list_filter = ("created_at", "updated_at",)
    ordering = ("-created_at",)


@admin.register(ForumThread)
class ForumThreadAdmin(admin.ModelAdmin):
    list_display = (
        "title", "category", "created_by", "created_at", "updated_at", "is_closed",
    )
    search_fields = ("title", "category__name", "created_by__username",)
    list_filter = ("created_at", "updated_at", "is_closed",)
    ordering = ("-created_at",)


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = (
        "thread", "content", "created_by", "created_at", "updated_at", "is_verified",
    )
    search_fields = ("thread__title", "content", "created_by__username",)
    list_filter = ("created_at", "updated_at", "is_verified",)
    ordering = ("-created_at",)


@admin.register(ForumComment)
class ForumCommentAdmin(admin.ModelAdmin):
    list_display = (
        "post", "content", "created_by", "created_at", "updated_at"
    )
    search_fields = ("post__content", "content", "created_by__username",)
    list_filter = ("created_at", "updated_at",)
    ordering = ("-created_at",)

