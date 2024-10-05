#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: remove_user_from_organization_views.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class RemoveUserFromOrganizationView(TemplateView, LoginRequiredMixin):
    """
    View to remove a user from a specific organization.

    This view allows administrators to remove a user from a particular organization. The user will no longer be associated with that organization.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with details of the user and organization to confirm the removal.
        post(self, request, *args, **kwargs): Handles the logic to remove the user from the specified organization.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = get_object_or_404(User, id=kwargs['pk'])
        organization = get_object_or_404(Organization, id=kwargs['org_id'])
        context['user_to_remove'] = user
        context['organization'] = organization
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
        organization = get_object_or_404(Organization, id=kwargs['org_id'])
        organization.users.remove(user)
        organization.save()
        print('[RemoveUserFromOrganizationView.post] User removed from organization successfully.')
        messages.success(request, f'User removed from {organization.name} successfully.')
        return redirect('user_management:list')
