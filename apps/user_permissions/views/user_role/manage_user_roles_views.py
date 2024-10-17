#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: manage_user_roles_views.py
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_permissions.models import UserRole, UserPermission
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class PermissionView_UserRoleManage(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.prefetch_related('users')
        context['roles'] = UserRole.objects.filter(organization__users__in=[self.request.user])
        return context

    def _update_user_permissions(self, user, role, add=True):
        for perm_code in role.role_permissions:
            if add:
                try:
                    user_permission, created = UserPermission.objects.get_or_create(
                        user=user,
                        permission_type=perm_code
                    )
                except IntegrityError as e:
                    messages.error(self.request, f"Error adding permission '{perm_code}' for user {user.username}")
            else:
                try:
                    user_permission = UserPermission.objects.get(user=user, permission_type=perm_code)
                    user_permission.delete()
                except UserPermission.DoesNotExist:
                    pass

    def _remove_user_role(self, user, role):
        self._update_user_permissions(user, role, add=False)
        if role in user.roles.all():
            user.roles.remove(role)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_USER_ROLES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_USER_ROLES):
            messages.error(self.request, "You do not have permission to update user roles.")
            return redirect('user_permissions:list_user_roles')
        ##############################

        user_id = request.POST.get('user_id')
        role_id = request.POST.get('role_id')
        user = get_object_or_404(User, pk=user_id)
        role = get_object_or_404(UserRole, pk=role_id)
        if "add_user_to_role" in request.POST:
            self._update_user_permissions(user, role, add=True)
            if role not in user.roles.all():
                user.roles.add(role)
            logger.info(f"User role added by User: {self.request.user.id}.")
            messages.success(request, f"User '{user.username}' successfully assigned to role '{role.role_name}'")
        elif "remove_user_role" in request.POST:
            self._remove_user_role(user, role)
            logger.info(f"User role removed by User: {self.request.user.id}.")
            messages.success(request, f"User '{user.username}' successfully removed from role '{role.role_name}'")
        return redirect('user_permissions:manage_user_roles')
