#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: create_permission_views.py
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
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission
from apps.user_permissions.utils import PERMISSION_TYPES, PermissionNames, get_permissions_grouped
from web_project import TemplateLayout


class PermissionView_PermissionCreate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        context['users'] = []
        context['permissions'] = get_permissions_grouped()
        if 'organization' in self.request.GET:
            org_id = self.request.GET.get('organization')
            org = get_object_or_404(Organization, id=org_id)
            context['selected_organization'] = org
            context['users'] = org.users.all()
        if 'user' in self.request.GET:
            user_id = self.request.GET.get('user')
            user = get_object_or_404(User, id=user_id)
            context['selected_user'] = user
            context['existing_permissions'] = list(user.permissions.values_list('permission_type', flat=True))
            context['available_permissions'] = [
                perm for perm in PERMISSION_TYPES if perm[0] not in context['existing_permissions']
            ]
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - MODIFY_USER_PERMISSIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.MODIFY_USER_PERMISSIONS):
            messages.error(self.request, "You do not have permission to add/modify permissions.")
            return redirect('user_permissions:list_permissions')
        ##############################

        org_id = request.POST.get('organization')
        user_id = request.POST.get('user')
        selected_permissions = request.POST.getlist('permissions')
        if org_id and user_id and selected_permissions:
            user = get_object_or_404(User, id=user_id)
            for perm in selected_permissions:
                UserPermission.objects.get_or_create(user=user, permission_type=perm)
            return redirect('user_permissions:list_permissions')
        context = self.get_context_data(**kwargs)
        context['error_messages'] = "All fields are required."
        return render(request, self.template_name, context)
