from django.contrib import admin

from apps.organization.models import Organization


@admin.register(Organization)
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
