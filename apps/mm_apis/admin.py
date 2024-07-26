from django.contrib import admin
from .models import CustomAPIReference, CustomAPI


# Register your models here.

@admin.register(CustomAPIReference)
class CustomAPIReferenceAdmin(admin.ModelAdmin):
    list_display = ["custom_api", "assistant", "api_source", "created_by_user", "created_at", "updated_at"]
    search_fields = ["custom_api__name", "assistant__name", "api_source", "created_by_user__username"]
    list_filter = ["api_source", "created_at", "updated_at"]
    list_per_page = 20


@admin.register(CustomAPI)
class CustomAPIAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "categories", "created_by_user", "created_at", "updated_at"]
    search_fields = ["name", "description", "categories", "created_by_user__username"]
    list_filter = ["categories", "created_at", "updated_at"]
    list_per_page = 20
