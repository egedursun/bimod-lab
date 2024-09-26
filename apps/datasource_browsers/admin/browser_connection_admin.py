from django.contrib import admin

from apps.datasource_browsers.models import DataSourceBrowserConnection


@admin.register(DataSourceBrowserConnection)
class DataSourceBrowserConnectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'assistant', 'browser_type', 'name', 'description', 'data_selectivity',
                    'whitelisted_extensions', 'blacklisted_extensions', 'created_at', 'updated_at']
    list_filter = ['assistant', 'browser_type', 'data_selectivity']
    search_fields = ['assistant', 'browser_type', 'name', 'description', 'data_selectivity', 'whitelisted_extensions',
                     'blacklisted_extensions', 'created_at', 'updated_at']
    list_per_page = 20
    list_max_show_all = 100
