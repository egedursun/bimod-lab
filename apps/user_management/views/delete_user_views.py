from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class RemoveUserView(LoginRequiredMixin, TemplateView):
    """
    View to delete a user from the system.

    This view allows administrators to permanently delete a user. The user will be removed from all associated organizations before deletion.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with details of the user to confirm the deletion.
        post(self, request, *args, **kwargs): Handles the logic to delete the user and remove them from all organizations.
    """

    template_name = "user_management/users/confirm_remove_user.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = get_object_or_404(User, id=kwargs['pk'])
        context['user_to_delete'] = user
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_USERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_USERS):
            messages.error(self.request, "You do not have permission to delete user accounts.")
            return redirect('user_management:list')
        ##############################

        user = get_object_or_404(User, id=kwargs['pk'])
        # remove the user from all organizations
        organizations = Organization.objects.filter(users__in=[user])
        for organization in organizations:
            organization.users.remove(user)
            organization.save()
        user.delete()
        # remove the user from all organizations
        print('[RemoveUserView.post] User deleted successfully.')
        messages.success(request, 'User deleted successfully.')
        return redirect('user_management:list')
