#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: remove_user_from_all_organizations_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:43
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
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class UserManagementView_UserRemoveFromAll(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = get_object_or_404(User, id=kwargs['pk'])
        context['user_to_remove'] = user
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - REMOVE_USER_FROM_ORGANIZATION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_USER_FROM_ORGANIZATION):
            messages.error(self.request, "You do not have permission to remove users from organizations.")
            return redirect('user_management:list')
        ##############################

        user = get_object_or_404(User, id=kwargs['pk'])

        try:
            orgs = Organization.objects.filter(users__in=[user])
            for org in orgs:
                org.users.remove(user)
                org.save()
        except Exception as e:
            logger.error(f"User removal from organizations failed. Error: {e}")
            messages.error(request, 'User removal from organizations failed.')
            return redirect('user_management:list')

        logger.info(f"User was removed from all organizations by User: {self.request.user.id}.")
        messages.success(request, f'User removed from all organizations successfully.')
        return redirect('user_management:list')
