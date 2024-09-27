from django.contrib import admin

from apps.leanmod.models import ExpertNetwork


@admin.register(ExpertNetwork)
class ExpertNetworkAdmin(admin.ModelAdmin):
    list_display = (
        "organization", "name", "meta_description", "created_by_user", "last_updated_by_user", "created_at",
        "updated_at")
    list_filter = (
        "organization", "name", "meta_description", "created_by_user", "last_updated_by_user", "created_at",
        "updated_at")
    search_fields = (
        "organization", "name", "meta_description", "created_by_user", "last_updated_by_user", "created_at",
        "updated_at")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
