from django.contrib import admin

from apps.message_templates.models import MessageTemplate


# Register your models here.

@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ["user", "organization", "template_text", "created_at", "updated_at"]
    search_fields = ["user", "organization", "template_text"]
    list_filter = ["user", "organization", "created_at", "updated_at"]
    list_per_page = 20
    list_max_show_all = 200
    list_editable = ["template_text"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        (None, {
            "fields": ("user", "organization", "template_text")
        }),
        ("Date Information", {
            "fields": ("created_at", "updated_at"),
        })
    )
    actions = ["delete_selected"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
