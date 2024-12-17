#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: connect_user_to_organization_views.py
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class UserManagementView_ConnectUser(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        context_sub_users = context_user.profile.sub_users.all()

        context['users'] = context_sub_users

        context['organizations'] = Organization.objects.filter(
            users__in=[self.request.user]
        )

        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - CONNECT_USER_TO_ORGANIZATION
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.CONNECT_USER_TO_ORGANIZATION
        ):
            messages.error(self.request, "You do not have permission to connect users to organizations.")
            return redirect('user_management:list')
        ##############################

        user = request.POST.get('user')
        org_id = request.POST.get('organization')
        try:
            user = User.objects.get(
                id=user
            )

            org = Organization.objects.get(
                id=org_id
            )

            if user in org.users.all():
                messages.error(request, 'User is already a member of this organization.')

            else:
                org.users.add(user)

                logger.info(f"User: {user.id} was added to Organization: {org.id} by User: {context_user.id}.")
                messages.success(request, 'User added to organization successfully!')

        except User.DoesNotExist:
            logger.error(f"User does not exist. User ID: {user}")
            messages.error(request, 'User does not exist.')

        except Organization.DoesNotExist:
            logger.error(f"Organization does not exist. Organization ID: {org_id}")
            messages.error(request, 'Organization does not exist.')

        except Exception as e:
            logger.error(f"Error adding user to organization: {str(e)}")
            messages.error(request, f'Error adding user to organization: {str(e)}')

        return redirect('user_management:add_user_to_organization')
