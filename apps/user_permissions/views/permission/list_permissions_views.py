#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: list_permissions_views.py
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
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ListPermissionsView(LoginRequiredMixin, TemplateView):
    """
    View to list and manage user permissions within organizations.

    This view displays a list of permissions assigned to users in each organization that the logged-in user is
    associated with. It also allows for updating and deleting these permissions.

    Methods: get_context_data(self, **kwargs): Prepares the context with organizations, users, and their associated
    permissions. post(self, request, *args, **kwargs): Handles the logic to update or delete permissions for a user.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_USER_PERMISSIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_USER_PERMISSIONS):
            messages.error(self.request, "You do not have permission to view user permissions.")
            return context
        ##############################

        user = self.request.user
        organizations = Organization.objects.filter(users__in=[user])
        org_users_permissions = {
            org: {"users": {user: user.permissions.all() for user in org.users.all()}} for org in organizations
        }
        context['org_users_permissions'] = org_users_permissions
        return context

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - MODIFY_USER_PERMISSIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.MODIFY_USER_PERMISSIONS):
            messages.error(self.request, "You do not have permission to add/modify permissions.")
            return redirect('user_permissions:list_permissions')
        ##############################

        user = get_object_or_404(User, id=user_id)
        permissions_data = request.POST.getlist('permissions')
        delete_requests = request.POST.getlist('delete_requests')
        # Process active/deactivate toggles
        for permission in user.permissions.all():
            if str(permission.id) in permissions_data and not permission.is_active:
                permission.is_active = True
                permission.save()
            elif str(permission.id) not in permissions_data and permission.is_active:
                permission.is_active = False
                permission.save()
        # Process delete requests
        deletion_names = []
        for permission_id in delete_requests:
            permission = get_object_or_404(UserPermission, id=permission_id)
            deletion_names.append(permission.get_permission_type_code())
            permission.delete()
        print('[ListPermissionsView.post] Permissions updated successfully.')
        messages.success(request, 'Permissions updated successfully!')

        # if the user is superuser, add back the permissions to modify and list permissions
        modify_permissions = PermissionNames.MODIFY_USER_PERMISSIONS
        list_permissions = PermissionNames.LIST_USER_PERMISSIONS

        if user.is_superuser:
            UserPermission.objects.get_or_create(user=user, permission_type=modify_permissions)
            UserPermission.objects.get_or_create(user=user, permission_type=list_permissions)
            # set the permissions to be active
            modify_object = UserPermission.objects.get(user=user, permission_type=modify_permissions)
            list_object = UserPermission.objects.get(user=user, permission_type=list_permissions)

            if (not modify_object.is_active or not list_object.is_active or modify_permissions in deletion_names
                or list_permissions in deletion_names):
                # provide information to the user
                messages.warning(request, 'You have removed your permission rights as an administrator, '
                                          'which would have prevented you from granting them back to yourself. '
                                          'We have automatically granted these permissions back to your account.')

            modify_object.is_active = True
            list_object.is_active = True
            modify_object.save()
            list_object.save()

        # Update only the relevant part of the page.
        return render(request, self.template_name, self.get_context_data(**kwargs))
