from django.contrib import admin

from apps.datasource_media_storages.models import DataSourceMediaStorageItem


@admin.register(DataSourceMediaStorageItem)
class DataSourceMediaStorageItemAdmin(admin.ModelAdmin):
    list_display = ['storage_base', 'media_file_name', 'media_file_size', 'media_file_type', 'full_file_path',
                    'created_at', 'updated_at']
    list_filter = ['storage_base', 'media_file_type', 'media_file_type']
    search_fields = ['storage_base', 'media_file_name', 'full_file_path']

    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

    list_per_page = 20
    list_max_show_all = 100
