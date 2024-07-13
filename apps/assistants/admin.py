import os

from django.contrib import admin

from apps.assistants.models import Assistant
from slugify import slugify


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
            dir_name = f"media/documents/{slugify(obj.organization.name)}/{slugify(obj.llm_model.model_name)}/{slugify(obj.name)}/"
            obj.document_base_directory = dir_name
            os.system(f"mkdir -p {dir_name}")
            os.system(f"touch {dir_name}/__init__.py")

        super().save_model(request, obj, form, change)
