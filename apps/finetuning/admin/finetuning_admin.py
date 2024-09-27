from django.contrib import admin

from apps.finetuning.models import FineTunedModelConnection


# Register your models here.

@admin.register(FineTunedModelConnection)
class FineTunedModelConnectionAdmin(admin.ModelAdmin):
    list_display = ('organization', 'nickname', 'model_name', "provider", 'model_type', 'created_at')
    search_fields = ('organization', 'nickname', 'model_name', "provider", 'model_type', 'model_description')
