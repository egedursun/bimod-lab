from celery import shared_task

from apps.mm_scripts.models import CustomScript

NUMBER_OF_RANDOM_FEATURED_SCRIPTS = 5


@shared_task
def randomize_featured_scripts():
    # first switch all script's is_featured field to false
    all_scripts = CustomScript.objects.all()
    for script in all_scripts:
        script.is_featured = False
        script.save()

    # then select 5 random scripts and set the is_featured field to true
    featured_scripts = CustomScript.objects.order_by('?')[:NUMBER_OF_RANDOM_FEATURED_SCRIPTS]
    for script in featured_scripts:
        script.is_featured = True
        script.save()
