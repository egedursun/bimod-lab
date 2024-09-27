from django.contrib import admin

from apps.leanmod.models import LeanAssistant


@admin.register(LeanAssistant)
class LeanAssistantAdmin(admin.ModelAdmin):
    list_display = (
        "organization", "llm_model", "name",
        "created_by_user", "last_updated_by_user", "created_at", "updated_at")
    list_filter = (
        "organization", "llm_model", "name",
        "created_by_user", "last_updated_by_user", "created_at", "updated_at")
    search_fields = (
        "organization", "llm_model", "name",
        "created_by_user", "last_updated_by_user", "created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_display_links = ["organization"]
    list_select_related = False
    list_display_links_details = False
