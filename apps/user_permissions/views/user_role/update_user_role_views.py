#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: update_user_role_views.py
#  Last Modified: 2024-09-29 18:48:54
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-29 19:08:29
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.organization.models import Organization
from apps.user_permissions.forms import UserRoleForm
from apps.user_permissions.models import UserRole
from apps.user_permissions.utils import PERMISSION_TYPES
from web_project import TemplateLayout


class UpdateUserRoleView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        role_id = kwargs.get('pk')
        role = get_object_or_404(UserRole, pk=role_id)
        form = UserRoleForm(instance=role)

        organizations = Organization.objects.filter(users__in=[self.request.user])
        available_permissions = PERMISSION_TYPES
        selected_permissions = role.role_permissions

        context['role'] = role
        context['form'] = form
        context['organizations'] = organizations
        context['available_permissions'] = available_permissions
        context['selected_permissions'] = selected_permissions
        return context

    def post(self, request, *args, **kwargs):
        role_id = kwargs.get('pk')  # Fetch pk from kwargs
        role = get_object_or_404(UserRole, pk=role_id)  # Fetch the role object
        form = UserRoleForm(request.POST, instance=role)

        if form.is_valid():
            role = form.save(commit=False)
            role.organization = form.cleaned_data['organization']
            role.role_name = form.cleaned_data['role_name']

            # Update permissions
            selected_permissions = form.cleaned_data.get('role_permissions')  # Get cleaned permissions data
            role.role_permissions = selected_permissions  # Assign the cleaned permissions to the role
            role.save()

            messages.success(request, f'Role "{role.role_name}" updated successfully.')
            return redirect('user_permissions:list_user_roles')
        else:
            print(form.errors)  # Debugging: Print form errors to see why it fails
            messages.error(request, 'Error updating the role.')
            return self.render_to_response(self.get_context_data(**kwargs))
