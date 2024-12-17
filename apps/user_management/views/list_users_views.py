#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_users_views.py
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

from django.core.paginator import Paginator
from django.db.models import Q

from django.shortcuts import (
    get_object_or_404,
    redirect
)

from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.organization.models import Organization
from apps.user_management.forms import UserStatusForm

from apps.user_permissions.utils import (
    PermissionNames
)

from auth.models import Profile
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class UserManagementView_UserList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_USERS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_USERS
        ):
            messages.error(self.request, "You do not have permission to list users.")
            return context
        ##############################

        context_user = self.request.user

        orgs = Organization.objects.filter(
            users__in=[context_user]
        )

        search_query = self.request.GET.get('search', '')
        page_number = self.request.GET.get('page', 1)

        org_users = {}

        for org in orgs:
            users = org.users.all()
            if search_query:
                users = users.filter(
                    Q(username__icontains=search_query) |
                    Q(email__icontains=search_query) |
                    Q(profile__first_name__icontains=search_query) |
                    Q(profile__last_name__icontains=search_query))

            paginator = Paginator(users, 10)
            page_obj = paginator.get_page(page_number)

            user_profiles = [
                (
                    user,
                    Profile.objects.filter(
                        user=user
                    ).first()
                ) for user in page_obj
            ]

            org_users[org] = {
                'page_obj': page_obj,
                'user_profiles': user_profiles,
                'search_query': search_query
            }

        context['org_users'] = org_users
        context['context_user'] = context_user

        return context

    def post(self, request, *args, **kwargs):
        form = UserStatusForm(request.POST)

        if form.is_valid():
            user_id = request.POST.get('user_id')

            profile = get_object_or_404(
                Profile,
                user__id=user_id
            )

            profile.is_active = form.cleaned_data['is_active']

            profile.save()

            user = profile.user
            user_permissions = user.permissions.all()

            for user_permission in user_permissions:
                user_permission.is_active = profile.is_active

                user_permission.save()

            logger.info(f"User status updated by User: {self.request.user.id}.")
            messages.success(request, 'User status updated successfully!')

        else:
            logger.error(f"Failed to update user status by User: {self.request.user.id}.")
            messages.error(request, 'Failed to update user status.')

        return redirect('user_management:list')
