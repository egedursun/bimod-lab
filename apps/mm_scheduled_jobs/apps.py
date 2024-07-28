from django.apps import AppConfig


class MmScheduledJobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.mm_scheduled_jobs'

    def ready(self):
        import apps.mm_scheduled_jobs.signals
