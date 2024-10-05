#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: delete_user_role_views.py
#  Last Modified: 2024-09-29 22:36:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:42
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: delete_user_role_views.py
#  Last Modified: 2024-09-29 18:45:18
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-29 18:48:11
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.user_permissions.models import UserRole
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DeleteUserRoleView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        role_id = kwargs.get("pk")
        role = get_object_or_404(UserRole, pk=role_id, organization__users__in=[self.request.user])

        context.update({"role": role})
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_USER_ROLES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_USER_ROLES):
            messages.error(self.request, "You do not have permission to delete a user role.")
            return redirect('user_permissions:list_user_roles')
        ##############################

        role_id = kwargs.get("pk")
        role = get_object_or_404(UserRole, pk=role_id, created_by_user=request.user)

        # Delete the role
        role.delete()
        messages.success(request, f'The role "{role.role_name}" has been deleted successfully.')
        return redirect('user_permissions:list_user_roles')
