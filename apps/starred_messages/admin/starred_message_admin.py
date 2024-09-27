from django.contrib import admin

from apps.starred_messages.models import StarredMessage


@admin.register(StarredMessage)
class StarredMessageAdmin(admin.ModelAdmin):
    list_display = ["user", "organization", "assistant", "chat", "chat_message", "starred_at", "message_text"]
    list_filter = ["user", "organization", "assistant", "chat", "chat_message", "starred_at", "message_text"]
    search_fields = ["user", "organization", "assistant", "chat", "chat_message", "starred_at", "message_text"]
    list_per_page = 20
    ordering = ["-starred_at"]
    readonly_fields = ["starred_at"]
    fieldsets = [
        (
        None, {"fields": ["user", "organization", "assistant", "chat", "chat_message", "starred_at", "message_text"]}),
    ]
    add_fieldsets = [
        (
        None, {"fields": ["user", "organization", "assistant", "chat", "chat_message", "starred_at", "message_text"]}),
    ]
