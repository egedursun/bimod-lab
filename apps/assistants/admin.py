import os
import random

from django.contrib import admin

from apps.assistants.models import Assistant
from django.contrib.admin.actions import delete_selected as django_delete_selected


# Register your models here.

@admin.register(Assistant)
class AssistantAdmin(admin.ModelAdmin):
    list_display = (
        "organization", "response_language", "llm_model", "name", "description", "instructions", "audience", "tone",
        "time_awareness", "place_awareness", "tool_max_attempts_per_instance", "tool_max_chains",
        "document_base_directory", "max_retry_count", "created_by_user", "last_updated_by_user", "created_at",
        "updated_at")
    list_filter = (
        "organization", "response_language", "llm_model", "name", "description", "instructions", "audience", "tone",
        "document_base_directory", "time_awareness", "place_awareness", "tool_max_attempts_per_instance",
        "tool_max_chains", "max_retry_count", "created_by_user", "last_updated_by_user", "created_at", "updated_at")
    search_fields = (
        "organization", "response_language", "llm_model", "name", "description", "instructions", "audience", "tone",
        "document_base_directory", "time_awareness", "place_awareness", "tool_max_attempts_per_instance",
        "tool_max_chains", "max_retry_count", "created_by_user", "last_updated_by_user", "created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_display_links = ["organization"]
    list_select_related = False
    list_display_links_details = False

    def save_model(self, request, obj, form, change):
        if obj.document_base_directory is None:
            dir_name = f"media/documents/{str(obj.organization.id)}/{str(obj.llm_model.id)}/{str(obj.id)}_{str(random.randint(1_000_000, 9_999_999))}/"
            obj.document_base_directory = dir_name
            os.system(f"mkdir -p {dir_name}")
            os.system(f"touch {dir_name}/__init__.py")
        super().save_model(request, obj, form, change)

    def delete_selected(self, request, queryset):
        # Remove the document directory
        for obj in queryset:
            if obj.document_base_directory is not None:
                os.system(f"rm -rf {obj.document_base_directory}")
        return django_delete_selected(self, request, queryset)
