#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: create_organization_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
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
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.organization.forms import OrganizationForm
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class OrganizationView_OrganizationCreate(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = OrganizationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = OrganizationForm(request.POST, request.FILES)

        ##############################
        # PERMISSION CHECK FOR - ADD_ORGANIZATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_ORGANIZATIONS):
            messages.error(self.request, "You do not have permission to add organizations.")
            return redirect('organization:list')
        ##############################

        if form.is_valid():
            org = form.save(commit=False)
            org.created_by_user = request.user
            org.save()
            org.users.clear()
            org.users.add(request.user)
            return redirect('organization:list')
        else:
            error_msgs = form.errors
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['error_messages'] = error_msgs
            return self.render_to_response(context)
