from django.contrib import admin

from apps.mm_apis.models import CustomAPI


@admin.register(CustomAPI)
class CustomAPIAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "categories", "created_by_user", "created_at", "updated_at"]
    search_fields = ["name", "description", "categories", "created_by_user__username"]
    list_filter = ["categories", "created_at", "updated_at"]
    list_per_page = 20
