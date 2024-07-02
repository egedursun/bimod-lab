from django.contrib import admin

from apps.user_permissions.models import UserPermission


@admin.register(UserPermission)
class UserPermissionsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "permission_type",
        "created_at",
    )
    list_filter = ("user", "permission_type", "created_at")
    search_fields = ("user", "permission_type")
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    list_per_page = 20
    list_max_show_all = 100
    list_editable = []
    list_display_links = ["user"]
    list_select_related = False
    list_display_links_details = False
