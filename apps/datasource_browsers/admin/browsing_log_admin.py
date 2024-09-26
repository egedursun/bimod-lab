from django.contrib import admin

from apps.datasource_browsers.models import DataSourceBrowserBrowsingLog


@admin.register(DataSourceBrowserBrowsingLog)
class DataSourceBrowserBrowsingLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'connection', 'action', 'created_at']
    list_filter = ['connection', 'action', 'created_at']
    search_fields = ['connection', 'action', 'html_content', 'log_content', 'created_at']
    list_per_page = 20
    list_max_show_all = 100
