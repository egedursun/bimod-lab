#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: create_orchestration_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:07:12
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
from apps.assistants.models import Assistant
from apps.llm_core.models import LLMCore
from apps.orchestrations.forms import MaestroForm
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CreateOrchestrationView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of a new orchestration within the Bimod platform.
    """
    template_name = 'orchestrations/create_orchestration.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = MaestroForm()
        context['organizations'] = Organization.objects.filter(users=self.request.user)
        context['llm_models'] = LLMCore.objects.filter(organization__in=context['organizations'])
        context['assistants'] = Assistant.objects.filter(organization__in=context['organizations'])
        return context

    def post(self, request, *args, **kwargs):
        form = MaestroForm(request.POST, request.FILES)

        ##############################
        # PERMISSION CHECK FOR - ADD_ORCHESTRATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_ORCHESTRATIONS):
            messages.error(self.request, "You do not have permission to create orchestrations.")
            return redirect('orchestrations:list')
        ##############################

        if form.is_valid():
            maestro = form.save(commit=False)
            maestro.created_by_user = request.user
            maestro.last_updated_by_user = request.user
            maestro.save()

            # Save workers
            workers = request.POST.getlist('workers')
            maestro.workers.set(workers)

            return redirect('orchestrations:list')
        else:
            error_messages = form.errors
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['error_messages'] = error_messages
            return self.render_to_response(context)
