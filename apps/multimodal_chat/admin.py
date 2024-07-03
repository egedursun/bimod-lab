from django.contrib import admin

from apps.multimodal_chat.models import MultimodalChat, MultimodalChatMessage


# Register your models here.


@admin.register(MultimodalChat)
class MultimodalChatAdmin(admin.ModelAdmin):
    list_display = ['organization', 'assistant', 'user', 'chat_name', 'created_by_user', 'created_at', 'updated_at']
    list_filter = ['organization', 'assistant', 'user', 'created_by_user', 'created_at', 'updated_at']
    search_fields = ['organization', 'assistant', 'user', 'chat_name', 'created_by_user', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_display_links = ["organization"]
    list_select_related = False
    list_display_links_details = False


@admin.register(MultimodalChatMessage)
class MultimodalChatMessageAdmin(admin.ModelAdmin):
    list_display = ['multimodal_chat', 'transaction', 'sender_type', 'sent_at']
    list_filter = ['multimodal_chat', 'transaction', 'sender_type', 'sent_at']
    search_fields = ['multimodal_chat', 'transaction', 'sender_type', 'sent_at']
    readonly_fields = ['sent_at']

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_select_related = False
    list_display_links_details = False
