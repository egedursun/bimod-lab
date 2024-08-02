from django.contrib import admin
from .models import ScheduledJob, ScheduledJobInstance


@admin.register(ScheduledJob)
class ScheduledJobAdmin(admin.ModelAdmin):
    list_display = ['name', 'assistant',
                    'current_run_count', 'maximum_runs', 'created_at', 'updated_at', 'created_by_user']
    search_fields = ['name', 'assistant',
                     'current_run_count', 'maximum_runs', 'created_at', 'updated_at', 'created_by_user']
    list_filter = ['name', 'assistant',
                   'current_run_count', 'maximum_runs', 'created_at', 'updated_at', 'created_by_user']


@admin.register(ScheduledJobInstance)
class ScheduledJobInstanceAdmin(admin.ModelAdmin):
    list_display = ['scheduled_job', 'status', 'started_at', 'ended_at']
    search_fields = ['scheduled_job', 'status', 'started_at', 'ended_at']
    list_filter = ['scheduled_job', 'status', 'started_at', 'ended_at']

