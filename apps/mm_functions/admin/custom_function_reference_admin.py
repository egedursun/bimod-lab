from django.contrib import admin

from apps.mm_functions.models import CustomFunctionReference


@admin.register(CustomFunctionReference)
class CustomFunctionReferenceAdmin(admin.ModelAdmin):
    list_display = ("custom_function", "assistant", "created_by_user", "created_at", "updated_at")
    list_filter = ("assistant", "created_by_user")
    search_fields = ("custom_function__name", "assistant__name")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
