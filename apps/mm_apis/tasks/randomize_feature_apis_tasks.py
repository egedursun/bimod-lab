from celery import shared_task

from apps.mm_apis.models import CustomAPI
from apps.mm_apis.utils import NUMBER_OF_RANDOM_FEATURED_APIS


@shared_task
def randomize_featured_apis():
    # first switch all API's is_featured field to false
    all_apis = CustomAPI.objects.all()
    for api in all_apis:
        api.is_featured = False
        api.save()

    # then select 5 random APIs and set the is_featured field to true
    featured_apis = CustomAPI.objects.order_by('?')[:NUMBER_OF_RANDOM_FEATURED_APIS]
    for api in featured_apis:
        api.is_featured = True
        api.save()
