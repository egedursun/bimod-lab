from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.mm_scheduled_jobs.models import ScheduledJob, ScheduledJobInstance
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ListScheduledJobLogsView(LoginRequiredMixin, TemplateView):
    """
    Displays logs of scheduled job instances.

    This view retrieves and displays all instances of a specific scheduled job, with support for searching and pagination.

    Methods:
        get_context_data(self, **kwargs): Retrieves the logs of the scheduled job instances and adds them to the context.
    """

    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_SCHEDULED_JOBS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_SCHEDULED_JOBS):
            messages.error(self.request, "You do not have permission to list scheduled jobs.")
            return context
        ##############################

        scheduled_job_id = self.kwargs.get('pk')
        scheduled_job = get_object_or_404(ScheduledJob, id=scheduled_job_id)
        context['scheduled_job'] = scheduled_job
        search_query = self.request.GET.get('search', '')
        job_instances_list = ScheduledJobInstance.objects.filter(scheduled_job=scheduled_job)
        if search_query:
            job_instances_list = job_instances_list.filter(Q(status__icontains=search_query))
        paginator = Paginator(job_instances_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['scheduled_job_instances'] = page_obj.object_list
        context['total_scheduled_job_instances'] = job_instances_list.count()
        context['search_query'] = search_query
        return context
