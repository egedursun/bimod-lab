import json

from django_celery_beat.models import CrontabSchedule, PeriodicTask


def add_periodic_task(scheduled_job):
    crontab_schedule, created = CrontabSchedule.objects.get_or_create(
        minute=scheduled_job.minute or '*',
        hour=scheduled_job.hour or '*',
        day_of_week=scheduled_job.day_of_week or '*',
        day_of_month=scheduled_job.day_of_month or '*',
        month_of_year=scheduled_job.month_of_year or '*'
    )
    PeriodicTask.objects.create(
        crontab=crontab_schedule,
        name=f'ScheduledJob-{scheduled_job.id}',
        task='apps.mm_scheduled_jobs.tasks.execute_scheduled_job',
        args=json.dumps([scheduled_job.id])
    )
