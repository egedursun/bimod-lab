#  Copyright Policy & Ownership
#
#  Bimod.io is a product of BMD Holdings. All materials, including but not limited to software, code, documentation,
#  graphics, design elements, and user interfaces provided by Bimod.io are protected by copyright law and international
#  treaties.
#  All content within Bimod.io is the exclusive property of BMD Holdings, unless otherwise stated.
#  Unauthorized use, distribution, or reproduction of any material contained in this software without the express
#  written consent of BMD Holdings is strictly prohibited.
#  Users may not copy, modify, distribute, display, perform, or create derivative works of Bimod.io without prior
#  written permission from BMD Holdings.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.mm_triggered_jobs.models import TriggeredJob, TriggeredJobInstance
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ListTriggeredJobLogsView(LoginRequiredMixin, TemplateView):
    """
    Displays the logs of a specific triggered job.

    This view retrieves and displays all instances of a triggered job, showing the execution logs and statuses. The view supports searching and pagination.

    Methods:
        get_context_data(self, **kwargs): Retrieves the logs of the specified triggered job and adds them to the context.
    """

    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_TRIGGERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_TRIGGERS):
            messages.error(self.request, "You do not have permission to list triggered jobs.")
            return context
        ##############################

        triggered_job_id = self.kwargs.get('pk')
        triggered_job = get_object_or_404(TriggeredJob, id=triggered_job_id)
        context['triggered_job'] = triggered_job
        search_query = self.request.GET.get('search', '')
        job_instances_list = TriggeredJobInstance.objects.filter(triggered_job=triggered_job)
        if search_query:
            job_instances_list = job_instances_list.filter(Q(status__icontains=search_query))

        paginator = Paginator(job_instances_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['triggered_job_instances'] = page_obj.object_list
        context['total_triggered_job_instances'] = job_instances_list.count()
        context['search_query'] = search_query
        return context
