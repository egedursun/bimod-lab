from django.contrib import admin

from apps.mm_scripts.models import CustomScript, CustomScriptReference


@admin.register(CustomScript)
class CustomScriptAdmin(admin.ModelAdmin):
    list_display = ("name", "is_public", "created_at", "updated_at")
    list_filter = ("is_public",)
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(CustomScriptReference)
class CustomScriptReferenceAdmin(admin.ModelAdmin):
    list_display = ("custom_script", "assistant", "created_by_user", "created_at", "updated_at")
    list_filter = ("assistant", "created_by_user")
    search_fields = ("custom_script__name", "assistant__name")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
