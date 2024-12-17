#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_orchestration_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
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

from django.shortcuts import (
    get_object_or_404,
    redirect
)

from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.assistants.models import Assistant
from apps.llm_core.models import LLMCore

from apps.orchestrations.forms import (
    MaestroForm
)

from apps.orchestrations.models import Maestro
from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class OrchestrationView_Update(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        orchestration = get_object_or_404(
            Maestro,
            pk=kwargs['pk']
        )

        context['form'] = MaestroForm(
            instance=orchestration
        )

        context['orchestration'] = orchestration

        context['organizations'] = Organization.objects.filter(
            users=self.request.user
        )

        context['llm_models'] = LLMCore.objects.filter(
            organization__in=context['organizations']
        )

        context['assistants'] = Assistant.objects.filter(
            organization__in=context['organizations']
        )

        context['selected_workers'] = orchestration.workers.all().values_list(
            'id',
            flat=True
        )

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_ORCHESTRATIONS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_ORCHESTRATIONS
        ):
            messages.error(self.request, "You do not have permission to update orchestrations.")

            return redirect('orchestrations:list')
        ##############################

        orchestration = get_object_or_404(
            Maestro,
            pk=kwargs['pk']
        )

        form = MaestroForm(
            request.POST,
            request.FILES,
            instance=orchestration
        )

        if form.is_valid():
            updated_orchestration = form.save(
                commit=False
            )

            updated_orchestration.last_updated_by_user = request.user

            updated_orchestration.save()

            workers = request.POST.getlist('workers')

            updated_orchestration.workers.set(
                workers
            )

            logger.info(f"Orchestration was updated by User: {self.request.user.id}.")

            return redirect(
                'orchestrations:update',
                pk=kwargs['pk']
            )

        else:
            context = self.get_context_data(**kwargs)

            context['form'] = form
            context['error_messages'] = form.errors

            logger.error(f"Orchestration update failed by User: {self.request.user.id}.")

            return self.render_to_response(context)
