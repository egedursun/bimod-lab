#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: list_finetunings_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:54:01
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.finetuning.forms import FineTunedModelConnectionForm
from apps.finetuning.models import FineTunedModelConnection
from apps.finetuning.utils import FineTuningModelProvidersNames, FineTunedModelTypesNames
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class FineTunedModelConnectionsListView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_FINETUNING_MODEL
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_FINETUNING_MODEL):
            messages.error(self.request, "You do not have permission to list Finetuning Model.")
            return context
        ##############################

        # Fetch organizations associated with the user
        organizations = Organization.objects.filter(users__in=[self.request.user])
        data = []

        for organization in organizations:
            # Fetch fine-tuned model connections for each organization
            connections = FineTunedModelConnection.objects.filter(
                organization=organization,
                created_by_user=self.request.user
            )
            data.append({'organization': organization, 'connections': connections})

        context['data'] = data
        # Add form-related context
        context['form'] = FineTunedModelConnectionForm()
        context['organizations'] = organizations
        context['providers'] = FineTuningModelProvidersNames.as_list()
        context['model_types'] = FineTunedModelTypesNames.as_list()
        return context

    def post(self, request, *args, **kwargs):
        form = FineTunedModelConnectionForm(request.POST)
        if form.is_valid():
            connection = form.save(commit=False)
            connection.created_by_user = request.user
            connection.save()
            return redirect('finetuning:list')

        # Re-render the page with form errors
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)
