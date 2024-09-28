from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.support_system.models import SupportTicket
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class SupportTicketListView(LoginRequiredMixin, TemplateView):
    """
    View to display a paginated list of the user's support tickets.

    This view fetches the support tickets associated with the logged-in user and sorts them by status,
    update time, creation time, and priority. The sorted tickets are then paginated and passed to the template.

    Methods:
    - get_context_data: Fetches, sorts, and paginates the user's support tickets, and adds them to the context.
    """

    template_name = 'support_system/list_support_tickets.html'
    paginate_by = 10  # Number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_SUPPORT_TICKETS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_SUPPORT_TICKETS):
            messages.error(self.request, "You do not have permission to view support tickets.")
            return context
        ##############################

        # Fetch the tickets for the user
        queryset = SupportTicket.objects.filter(user=self.request.user)

        # Define custom sorting in Python
        status_priority = {
            'open': 3,
            'in_progress': 2,
            'resolved': 1,
            'closed': 0,
        }

        # Sort the queryset in Python based on the desired order
        sorted_queryset = sorted(
            queryset,
            key=lambda ticket: (
                status_priority.get(ticket.status, 99),  # Custom order for status
                ticket.updated_at,  # Sort by updated_at
                ticket.created_at,  # Sort by created_at
                ticket.priority  # Sort by priority
            ),
            reverse=True  # We want descending order for dates, but status ascending
        )

        # Paginate the sorted queryset
        paginator = Paginator(sorted_queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Add the page object to the context
        context['page_obj'] = page_obj
        return context
