#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: update_organization_views.py
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
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.organization.forms import OrganizationForm
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class OrganizationUpdateView(TemplateView, LoginRequiredMixin):
    """
    Handles updating an existing organization's details.

    This view allows users with the appropriate permissions to modify an organization's attributes. It also handles the form submission and validation for updating the organization.

    Methods:
        get_context_data(self, **kwargs): Retrieves the current organization's details and adds them to the context, along with the organization update form.
        post(self, request, *args, **kwargs): Handles form submission for updating the organization, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        # retrieve the organization from the ID
        context_user = self.request.user
        organization = Organization.objects.filter(users__in=[context_user], id=kwargs['pk']).first()
        context['organization'] = organization
        context['user'] = context_user
        context['form'] = OrganizationForm(instance=organization)
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - UPDATE_ORGANIZATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_ORGANIZATIONS):
            messages.error(self.request, "You do not have permission to update organizations.")
            return redirect('organization:list')
        ##############################

        organization = get_object_or_404(Organization, users__in=[context_user], id=kwargs['pk'])
        form = OrganizationForm(request.POST, request.FILES, instance=organization)
        if form.is_valid():
            form.save()
            return redirect('organization:list')
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            error_messsages = form.errors
            context['error_messages'] = error_messsages
            return self.render_to_response(context)
