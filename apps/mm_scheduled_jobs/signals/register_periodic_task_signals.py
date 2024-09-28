from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask

from apps.mm_scheduled_jobs.models import ScheduledJob
from apps.mm_scheduled_jobs.tasks import add_periodic_task


@receiver(post_save, sender=ScheduledJob)
def register_periodic_task(sender, instance, created, **kwargs):
    # Delete any existing PeriodicTask for this ScheduledJob
    PeriodicTask.objects.filter(name=f'ScheduledJob-{instance.id}').delete()
    # Add a new periodic task for this ScheduledJob
    add_periodic_task(instance)
