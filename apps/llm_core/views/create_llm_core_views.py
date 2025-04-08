#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_llm_core_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
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

from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.llm_core.forms import LLMCoreForm
from apps.llm_core.models import LLMCore

from apps.llm_core.utils import (
    LargeLanguageModelProvidersNames,
    GPTModelNamesNames
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)
from config import settings

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class LLMView_Create(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user

        context['user'] = user
        context['organizations'] = user.organizations.all()

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_LLM_CORES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_LLM_CORES
        ):
            messages.error(self.request, "You do not have permission to add LLM Cores.")
            return redirect('llm_core:list')
        ##############################

        form = LLMCoreForm(request.POST, request.FILES)
        user = request.user

        form.instance.created_by_user = user
        form.instance.last_updated_by_user = user
        form.instance.provider = "OA"
        form.instance.model_name = GPTModelNamesNames.O3_MINI
        form.instance.api_key = settings.INTERNAL_OPENAI_API_KEY

        try:
            if form.is_valid():
                form.save()

                org = Organization.objects.get(
                    id=request.POST['organization']
                )

                llm_core = LLMCore.objects.filter(
                    created_by_user=user
                ).latest('created_at')

                org.llm_cores.add(llm_core)

                org.save()

                logger.info(f"LLM Core created: {llm_core.id}")

                return redirect('llm_core:list')

            else:
                error_msgs = form.errors
                context = self.get_context_data(**kwargs)

                context['form'] = form
                context['error_messages'] = error_msgs

                logger.error(f"Error creating LLM Core: {error_msgs}")

                return self.render_to_response(context)

        except Exception as e:
            logger.error(f"Error creating LLM Core: {e}")
            messages.error(request, f"Error creating LLM Core: {e}")

            return redirect('llm_core:create')
