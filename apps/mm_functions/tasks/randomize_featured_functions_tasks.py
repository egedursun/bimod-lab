from celery import shared_task

from apps.mm_functions.models import CustomFunction
from apps.mm_functions.utils import NUMBER_OF_RANDOM_FEATURED_FUNCTIONS


@shared_task
def randomize_featured_functions():
    # first switch all function's is_featured field to false¬
    all_functions = CustomFunction.objects.all()
    for function in all_functions:
        function.is_featured = False
        function.save()
    # then select 5 random functions and set the is_featured field to true
    featured_functions = CustomFunction.objects.order_by('?')[:NUMBER_OF_RANDOM_FEATURED_FUNCTIONS]
    for function in featured_functions:
        function.is_featured = True
        function.save()
