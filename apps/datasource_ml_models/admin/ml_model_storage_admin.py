from django.contrib import admin

from apps.datasource_ml_models.models import DataSourceMLModelConnection


@admin.register(DataSourceMLModelConnection)
class DataSourceMLModelConnectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'assistant', 'name', 'model_object_category', 'directory_full_path', 'created_at',
                    'updated_at')
    list_filter = ('assistant', 'model_object_category')
    search_fields = ('name', 'directory_full_path')
    ordering = ('-created_at',)
