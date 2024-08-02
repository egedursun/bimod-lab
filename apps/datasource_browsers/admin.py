from django.contrib import admin
from .models import DataSourceBrowserConnection, DataSourceBrowserBrowsingLog


# Register your models here.


@admin.register(DataSourceBrowserConnection)
class DataSourceBrowserConnectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'assistant', 'browser_type', 'name', 'description', 'data_selectivity',
                    'whitelisted_extensions', 'blacklisted_extensions', 'created_at', 'updated_at']
    list_filter = ['assistant', 'browser_type', 'data_selectivity']
    search_fields = ['assistant', 'browser_type', 'name', 'description', 'data_selectivity', 'whitelisted_extensions',
                     'blacklisted_extensions', 'created_at', 'updated_at']
    list_per_page = 20
    list_max_show_all = 100


@admin.register(DataSourceBrowserBrowsingLog)
class DataSourceBrowserBrowsingLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'connection', 'action', 'created_at']
    list_filter = ['connection', 'action', 'created_at']
    search_fields = ['connection', 'action', 'html_content', 'log_content', 'created_at']
    list_per_page = 20
    list_max_show_all = 100
