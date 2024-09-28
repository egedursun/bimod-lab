from django.contrib import admin

from apps.datasource_ml_models.models import DataSourceMLModelItem


@admin.register(DataSourceMLModelItem)
class DataSourceMLModelItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'ml_model_base', 'ml_model_name', 'description', 'ml_model_size', 'full_file_path',
                    'created_at', 'updated_at')
    list_filter = ('ml_model_base',)
    search_fields = ('ml_model_name', 'full_file_path')
    ordering = ('-created_at',)
