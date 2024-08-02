from django.contrib import admin

from .models import LLMCore


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "address", "industry", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "industry", "created_at", "updated_at")
    search_fields = ("name", "email", "phone", "address", "industry")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = ["is_active"]
    list_display_links = ["name"]
    list_select_related = False
    list_display_links_details = False


@admin.register(LLMCore)
class LLMCoreAdmin(admin.ModelAdmin):
    list_display = ("nickname", "provider", "model_name", "temperature", "maximum_tokens", "stop_sequences", "top_p",
                    "frequency_penalty", "presence_penalty", "created_at", "updated_at")
    list_filter = ("provider", "model_name", "temperature", "maximum_tokens", "top_p", "frequency_penalty",
                   "presence_penalty", "created_at", "updated_at")
    search_fields = ("nickname", "provider", "model_name", "temperature", "maximum_tokens", "stop_sequences", "top_p",
                     "frequency_penalty", "presence_penalty")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = ["provider", "model_name", "temperature", "maximum_tokens", "stop_sequences", "top_p",
                     "frequency_penalty", "presence_penalty"]
    list_display_links = ["nickname"]
    list_select_related = False
    list_display_links_details = False
