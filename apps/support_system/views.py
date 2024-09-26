"""
This module contains views for the Support System app, including the creation, listing, and detail views for support tickets.
The views ensure that only authenticated users can access and manage their own support tickets.

Views included:
- CreateSupportTicketView: Handles the creation of new support tickets.
- SupportTicketListView: Displays a paginated list of the user's support tickets.
- SupportTicketDetailView: Shows detailed information about a specific support ticket, including the ability to add responses.
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.support_system.forms import SupportTicketForm
from apps.support_system.models import SupportTicket, SupportTicketResponse
from apps.user_permissions.models import PermissionNames
from web_project import TemplateLayout


# Create your views here.

class CreateSupportTicketView(LoginRequiredMixin, TemplateView):
    """
    View to handle the creation of new support tickets.

    This view renders a form for creating a new support ticket. Upon submission, if the form is valid,
    the support ticket is saved and the user is redirected to the ticket list page. If the form is invalid,
    the form is re-rendered with validation errors.

    Methods:
    - get_context_data: Adds the support ticket form to the context.
    - post: Handles the form submission and saves the ticket if valid.
    """

    template_name = 'support_system/create_support_ticket.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = SupportTicketForm()
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - CREATE_SUPPORT_TICKETS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CREATE_SUPPORT_TICKETS):
            messages.error(self.request, "You do not have permission to create support tickets.")
            return redirect('support_system:list')
        ##############################

        form = SupportTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            # Optionally, you can add a success message here
            return redirect('support_system:list')
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)


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


class SupportTicketDetailView(LoginRequiredMixin, TemplateView):
    """
    View to display the details of a specific support ticket.

    This view shows the details of a specific support ticket, including the history of responses associated with it.
    Users can also add new responses to the ticket through this view.

    Methods:
    - get_context_data: Fetches the ticket and its responses, and adds them to the context.
    - post: Handles the submission of a new response to the ticket.
    """

    template_name = 'support_system/support_ticket_detail.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_SUPPORT_TICKETS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_SUPPORT_TICKETS):
            messages.error(self.request, "You do not have permission to view support tickets.")
            return context
        ##############################

        ticket = get_object_or_404(SupportTicket, pk=self.kwargs['pk'], user=self.request.user)
        context['ticket'] = ticket
        context['responses'] = ticket.responses.all().order_by('created_at')
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_SUPPORT_TICKETS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_SUPPORT_TICKETS):
            messages.error(self.request, "You do not have permission to update/modify support tickets.")
            return redirect('support_system:list')
        ##############################

        ticket = get_object_or_404(SupportTicket, pk=self.kwargs['pk'], user=request.user)
        response_text = request.POST.get('response')

        if response_text:
            SupportTicketResponse.objects.create(
                ticket=ticket,
                user=request.user,
                response=response_text
            )

        return redirect('support_system:detail', pk=ticket.pk)
