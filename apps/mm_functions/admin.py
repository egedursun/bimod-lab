from django.contrib import admin

from apps.mm_functions.models import CustomFunction, CustomFunctionReference


# Register your models here.

@admin.register(CustomFunction)
class CustomFunctionAdmin(admin.ModelAdmin):
    list_display = ("name", "is_public", "created_at", "updated_at")
    list_filter = ("is_public",)
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")

    ordering = ("-created_at",)


@admin.register(CustomFunctionReference)
class CustomFunctionReferenceAdmin(admin.ModelAdmin):
    list_display = ("custom_function", "assistant", "created_by_user", "created_at", "updated_at")
    list_filter = ("assistant", "created_by_user")
    search_fields = ("custom_function__name", "assistant__name")
    readonly_fields = ("created_at", "updated_at")

    ordering = ("-created_at",)
