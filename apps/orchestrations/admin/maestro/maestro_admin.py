from django.contrib import admin

from apps.orchestrations.models import Maestro


@admin.register(Maestro)
class MaestroAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'llm_model', 'created_by_user', 'last_updated_by_user', 'created_at',
                    'updated_at']
    search_fields = ['name', 'organization', 'llm_model', 'created_by_user', 'last_updated_by_user']
    list_filter = ['organization', 'llm_model', 'created_by_user', 'last_updated_by_user', 'created_at', 'updated_at']
