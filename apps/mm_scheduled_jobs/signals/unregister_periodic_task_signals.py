from django.db.models.signals import post_delete
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask

from apps.mm_scheduled_jobs.models import ScheduledJob


@receiver(post_delete, sender=ScheduledJob)
def unregister_periodic_task(sender, instance, **kwargs):
    # Delete any existing PeriodicTask for this ScheduledJob
    PeriodicTask.objects.filter(name=f'ScheduledJob-{instance.id}').delete()
