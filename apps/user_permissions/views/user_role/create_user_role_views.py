#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_user_role_views.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.organization.models import Organization

from apps.user_permissions.forms import (
    UserRoleForm
)

from apps.user_permissions.utils import (
    PERMISSION_TYPES,
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class PermissionView_UserRoleCreate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        form = UserRoleForm()

        orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        available_permissions = PERMISSION_TYPES

        context['form'] = form
        context['organizations'] = orgs
        context['available_permissions'] = available_permissions

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - CREATE_USER_ROLES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.CREATE_USER_ROLES
        ):
            messages.error(self.request, "You do not have permission to add a user role.")

            return redirect('user_permissions:list_user_roles')
        ##############################

        form = UserRoleForm(request.POST)
        if form.is_valid():
            role = form.save(
                commit=False
            )

            role.created_by_user = request.user
            selected_permissions = request.POST.getlist('role_permissions')
            role.role_permissions = selected_permissions

            role.save()

            logger.info(f"User role created by User: {self.request.user.id}.")
            messages.success(request, f'Role "{role.role_name}" created successfully.')

            return redirect('user_permissions:list_user_roles')

        else:
            logger.error(f"Error creating the role. Form errors: {form.errors}")
            messages.error(request, 'Error creating the role.')

            return redirect('user_permissions:add_user_role')
