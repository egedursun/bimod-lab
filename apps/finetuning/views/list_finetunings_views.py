#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_finetunings_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
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
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.finetuning.forms import FineTunedModelConnectionForm
from apps.finetuning.models import FineTunedModelConnection
from apps.finetuning.utils import FineTuningModelProvidersNames, FineTunedModelTypesNames
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class FineTuningView_List(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_FINETUNING_MODEL
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_FINETUNING_MODEL):
            messages.error(self.request, "You do not have permission to list Finetuning Model.")
            return context
        ##############################

        orgs = Organization.objects.filter(users__in=[self.request.user])
        data = []
        for organization in orgs:
            cs = FineTunedModelConnection.objects.filter(organization=organization, created_by_user=self.request.user)
            data.append({'organization': organization, 'connections': cs})

        context['data'] = data
        context['form'] = FineTunedModelConnectionForm()
        context['organizations'] = orgs
        context['providers'] = FineTuningModelProvidersNames.as_list()
        context['model_types'] = FineTunedModelTypesNames.as_list()
        logger.info(f"Finetuning Models were listed by User: {self.request.user.id}.")
        return context

    def post(self, request, *args, **kwargs):
        form = FineTunedModelConnectionForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.created_by_user = request.user
            c.save()
            return redirect('finetuning:list')
        context = self.get_context_data(**kwargs)
        context['form'] = form
        logger.error(f"Finetuning Model was not added by User: {request.user.id}.")
        return self.render_to_response(context)
