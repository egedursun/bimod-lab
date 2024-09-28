from django.contrib import admin

from apps.mm_functions.models import CustomFunction


@admin.register(CustomFunction)
class CustomFunctionAdmin(admin.ModelAdmin):
    list_display = ("name", "is_public", "created_at", "updated_at")
    list_filter = ("is_public",)
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
