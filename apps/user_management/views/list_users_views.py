#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: list_users_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:10:04
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_management.forms import UserStatusForm
from apps.user_permissions.utils import PermissionNames
from auth.models import Profile
from web_project import TemplateLayout


class ListUsersView(LoginRequiredMixin, TemplateView):
    """
    View to list users associated with the logged-in user's organizations.

    This view displays a paginated list of users who are part of the organizations that the logged-in user belongs to. It also allows for updating user statuses.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the list of users grouped by organization.
        post(self, request, *args, **kwargs): Handles the logic to update the status (active/inactive) of a user.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_USERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_USERS):
            messages.error(self.request, "You do not have permission to list users.")
            return context
        ##############################

        context_user = self.request.user
        organizations = Organization.objects.filter(users__in=[context_user])
        search_query = self.request.GET.get('search', '')
        page_number = self.request.GET.get('page', 1)

        org_users = {}
        for organization in organizations:
            users = organization.users.all()
            if search_query:
                users = users.filter(
                    Q(username__icontains=search_query) | Q(email__icontains=search_query) |
                    Q(profile__first_name__icontains=search_query) | Q(profile__last_name__icontains=search_query)
                )
            paginator = Paginator(users, 10)  # Show 10 users per page
            page_obj = paginator.get_page(page_number)
            user_profiles = [(user, Profile.objects.filter(user=user).first()) for user in page_obj]
            org_users[organization] = {'page_obj': page_obj, 'user_profiles': user_profiles,
                                       'search_query': search_query}
        context['org_users'] = org_users
        context['context_user'] = context_user
        return context

    def post(self, request, *args, **kwargs):
        form = UserStatusForm(request.POST)
        if form.is_valid():
            user_id = request.POST.get('user_id')
            profile = get_object_or_404(Profile, user__id=user_id)
            profile.is_active = form.cleaned_data['is_active']
            profile.save()
            # Update all permissions associated with the user, and set them to whatever is_active is
            user = profile.user
            user_permissions = user.permissions.all()
            for user_permission in user_permissions:
                user_permission.is_active = profile.is_active
                user_permission.save()
            print('[ListUsersView.post] User status updated successfully.')
            messages.success(request, 'User status updated successfully!')
        else:
            messages.error(request, 'Failed to update user status.')
        return redirect('user_management:list')
