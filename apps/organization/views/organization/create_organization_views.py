from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.organization.forms import OrganizationForm
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CreateOrganizationView(TemplateView, LoginRequiredMixin):
    """
    Handles the creation of a new organization within the Bimod.io platform.

    This view displays a form for creating an organization. Upon form submission, it validates the input, checks user permissions, and saves the new organization to the database. If the user lacks the necessary permissions, an error message is displayed.

    Methods:
        get_context_data(self, **kwargs): Adds additional context to the template, including the organization creation form.
        post(self, request, *args, **kwargs): Handles form submission and organization creation, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = OrganizationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = OrganizationForm(request.POST, request.FILES)

        ##############################
        # PERMISSION CHECK FOR - ADD_ORGANIZATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_ORGANIZATIONS):
            messages.error(self.request, "You do not have permission to add organizations.")
            return redirect('organization:list')
        ##############################

        if form.is_valid():
            organization = form.save(commit=False)
            organization.created_by_user = request.user
            organization.save()
            organization.users.clear()
            organization.users.add(request.user)
            return redirect('organization:list')
        else:
            error_messages = form.errors
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['error_messages'] = error_messages
            return self.render_to_response(context)
