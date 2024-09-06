from django.contrib import admin

from apps.data_security.models import NERIntegration


@admin.register(NERIntegration)
class NERIntegrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'language', 'created_by_user', 'created_at', 'updated_at')
    list_filter = ('organization', 'language', 'created_by_user')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
