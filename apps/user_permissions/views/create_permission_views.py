from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission
from apps.user_permissions.utils import PERMISSION_TYPES, PermissionNames, get_permissions_grouped
from web_project import TemplateLayout


class AddPermissionsView(LoginRequiredMixin, TemplateView):
    """
    View to handle adding permissions to users.

    This view allows administrators to assign specific permissions to users within an organization. The permissions
    are grouped by categories like 'Organization Permissions', 'LLM Core Permissions', etc.

    Methods: get_context_data(self, **kwargs): Prepares the context with organizations, users, and grouped
    permissions. If an organization and/or user is selected, it filters the context accordingly. post(self, request,
    *args, **kwargs): Handles the logic to assign selected permissions to a user. get_permissions_grouped(self):
    Returns a dictionary of permissions grouped by categories.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        context['users'] = []
        context['permissions'] = get_permissions_grouped()
        if 'organization' in self.request.GET:
            organization_id = self.request.GET.get('organization')
            organization = get_object_or_404(Organization, id=organization_id)
            context['selected_organization'] = organization
            context['users'] = organization.users.all()
        if 'user' in self.request.GET:
            user_id = self.request.GET.get('user')
            user = get_object_or_404(User, id=user_id)
            context['selected_user'] = user
            context['existing_permissions'] = list(user.permissions.values_list('permission_type', flat=True))
            context['available_permissions'] = [
                perm for perm in PERMISSION_TYPES if perm[0] not in context['existing_permissions']
            ]
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - MODIFY_USER_PERMISSIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.MODIFY_USER_PERMISSIONS):
            messages.error(self.request, "You do not have permission to add/modify permissions.")
            return redirect('user_permissions:list_permissions')
        ##############################

        organization_id = request.POST.get('organization')
        user_id = request.POST.get('user')
        selected_permissions = request.POST.getlist('permissions')
        if organization_id and user_id and selected_permissions:
            user = get_object_or_404(User, id=user_id)
            for perm in selected_permissions:
                UserPermission.objects.get_or_create(user=user, permission_type=perm)
            return redirect('user_permissions:list_permissions')
        context = self.get_context_data(**kwargs)
        context['error_messages'] = "All fields are required."
        return render(request, self.template_name, context)
