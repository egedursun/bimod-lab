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
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.mm_triggered_jobs.models import TriggeredJob
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ListTriggeredJobsView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of triggered jobs associated with the user's assistants.

    This view retrieves and displays all triggered jobs that are available to the current user, with support for searching and pagination.

    Methods:
        get_context_data(self, **kwargs): Retrieves the user's accessible triggered jobs and adds them to the context.
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

        search_query = self.request.GET.get('search', '')
        user_organizations = self.request.user.organizations.all()
        organization_assistants = user_organizations.values_list('assistants', flat=True)
        triggered_jobs_list = TriggeredJob.objects.filter(trigger_assistant__in=organization_assistants)

        if search_query:
            triggered_jobs_list = triggered_jobs_list.filter(
                Q(name__icontains=search_query) | Q(task_description__icontains=search_query)
            )
        paginator = Paginator(triggered_jobs_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['triggered_jobs'] = page_obj.object_list
        context['total_triggered_jobs'] = TriggeredJob.objects.count()
        context['search_query'] = search_query
        return context
