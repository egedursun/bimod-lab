from django.contrib import admin

from apps.leanmod.models import ExpertNetworkAssistantReference


@admin.register(ExpertNetworkAssistantReference)
class ExpertNetworkAssistantReferenceAdmin(admin.ModelAdmin):
    list_display = (
        "network", "assistant", "context_instructions", "created_by_user", "last_updated_by_user", "created_at",
        "updated_at")
    list_filter = (
        "network", "assistant", "context_instructions", "created_by_user", "last_updated_by_user", "created_at",
        "updated_at")
    search_fields = (
        "network", "assistant", "context_instructions", "created_by_user", "last_updated_by_user", "created_at",
        "updated_at")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
