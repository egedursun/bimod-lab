from django.contrib import admin

from apps.mm_apis.models import CustomAPIReference


@admin.register(CustomAPIReference)
class CustomAPIReferenceAdmin(admin.ModelAdmin):
    list_display = ["custom_api", "assistant", "api_source", "created_by_user", "created_at", "updated_at"]
    search_fields = ["custom_api__name", "assistant__name", "api_source", "created_by_user__username"]
    list_filter = ["api_source", "created_at", "updated_at"]
    list_per_page = 20
