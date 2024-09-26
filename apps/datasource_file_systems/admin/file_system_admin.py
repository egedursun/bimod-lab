from django.contrib import admin

from apps.datasource_file_systems.models import DataSourceFileSystem


@admin.register(DataSourceFileSystem)
class DataSourceFileSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'os_type', 'host_url', 'port', 'username', 'is_read_only')
    list_filter = ('os_type', 'is_read_only')
    search_fields = ('name', 'host_url', 'username', 'ssh_connection_uri')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    save_on_top = True
