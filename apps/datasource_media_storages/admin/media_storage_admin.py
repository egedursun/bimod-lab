from django.contrib import admin

from apps.datasource_media_storages.models import DataSourceMediaStorageConnection


@admin.register(DataSourceMediaStorageConnection)
class DataSourceMediaStorageConnectionAdmin(admin.ModelAdmin):
    list_display = ['assistant', 'name', 'media_category', 'directory_full_path', 'directory_schema', 'created_at',
                    'updated_at']
    list_filter = ['assistant', 'media_category']
    search_fields = ['assistant', 'name', 'directory_full_path']

    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

    list_per_page = 20
    list_max_show_all = 100
