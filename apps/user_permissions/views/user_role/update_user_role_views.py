#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: update_user_role_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_permissions.forms import UserRoleForm
from apps.user_permissions.models import UserRole
from apps.user_permissions.utils import PERMISSION_TYPES, PermissionNames
from web_project import TemplateLayout


class PermissionView_UserRoleUpdate(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        role_id = kwargs.get('pk')
        role = get_object_or_404(UserRole, pk=role_id)
        form = UserRoleForm(instance=role)
        orgs = Organization.objects.filter(users__in=[self.request.user])
        available_permissions = PERMISSION_TYPES
        selected_permissions = role.role_permissions
        context['role'] = role
        context['form'] = form
        context['organizations'] = orgs
        context['available_permissions'] = available_permissions
        context['selected_permissions'] = selected_permissions
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_USER_ROLES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_USER_ROLES):
            messages.error(self.request, "You do not have permission to update user roles.")
            return redirect('user_permissions:list_user_roles')
        ##############################

        role_id = kwargs.get('pk')
        role = get_object_or_404(UserRole, pk=role_id)
        form = UserRoleForm(request.POST, instance=role)

        if form.is_valid():
            role = form.save(commit=False)
            role.organization = form.cleaned_data['organization']
            role.role_name = form.cleaned_data['role_name']
            selected_permissions = form.cleaned_data.get('role_permissions')
            role.role_permissions = selected_permissions
            role.save()
            messages.success(request, f'Role "{role.role_name}" updated successfully.')
            return redirect('user_permissions:list_user_roles')
        else:
            messages.error(request, 'Error updating the role.')
            return self.render_to_response(self.get_context_data(**kwargs))
