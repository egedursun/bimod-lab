from django.contrib import admin

from apps.mm_scheduled_jobs.models import ScheduledJob


@admin.register(ScheduledJob)
class ScheduledJobAdmin(admin.ModelAdmin):
    list_display = ['name', 'assistant',
                    'current_run_count', 'maximum_runs', 'created_at', 'updated_at', 'created_by_user']
    search_fields = ['name', 'assistant',
                     'current_run_count', 'maximum_runs', 'created_at', 'updated_at', 'created_by_user']
    list_filter = ['name', 'assistant',
                   'current_run_count', 'maximum_runs', 'created_at', 'updated_at', 'created_by_user']
