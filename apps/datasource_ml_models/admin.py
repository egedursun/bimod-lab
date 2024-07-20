from django.contrib import admin
from .models import DataSourceMLModelConnection
from .models import DataSourceMLModelItem


# Register your models here.


@admin.register(DataSourceMLModelConnection)
class DataSourceMLModelConnectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'assistant', 'name', 'model_object_category', 'directory_full_path', 'created_at',
                    'updated_at')
    list_filter = ('assistant', 'model_object_category')
    search_fields = ('name', 'directory_full_path')
    ordering = ('-created_at',)


@admin.register(DataSourceMLModelItem)
class DataSourceMLModelItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'ml_model_base', 'ml_model_name', 'description', 'ml_model_size', 'full_file_path',
                    'created_at', 'updated_at')
    list_filter = ('ml_model_base',)
    search_fields = ('ml_model_name', 'full_file_path')
    ordering = ('-created_at',)
