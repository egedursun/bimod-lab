#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_configuration_views.py
#  Last Modified: 2024-11-14 22:31:35
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 18:53:12
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

from apps.assistants.utils import AGENT_SPEECH_LANGUAGES
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from apps.voidforger.models import VoidForger
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class VoidForgerView_Configuration(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        config, created = VoidForger.objects.get_or_create(
            user=self.request.user
        )

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        llm_models = LLMCore.objects.filter(
            organization__in=user_orgs
        )

        if not llm_models or len(llm_models) == 0:
            messages.error(
                self.request,
                "You do not have an LLM model to use, to use VoidForger chat, please create an LLM model."
            )
            return context

        if config.llm_model is None:
            config.llm_model = llm_models[0]
            config.save()

        # Updatable data selections
        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        llm_cores = LLMCore.objects.filter(organization__in=user_orgs)

        # Calculate lifetime
        remaining_lifetime_cycles = (
            config.auto_run_max_lifetime_cycles - config.auto_run_current_cycle
        )

        remaining_lifetime_pct = (
            (
                remaining_lifetime_cycles / config.auto_run_max_lifetime_cycles
            ) * 100
        )

        context['config'] = config
        context['user_orgs'] = user_orgs
        context['llm_cores'] = llm_cores
        context['AGENT_SPEECH_LANGUAGES'] = AGENT_SPEECH_LANGUAGES
        context['remaining_lifetime_cycles'] = remaining_lifetime_cycles
        context['remaining_lifetime_pct'] = remaining_lifetime_pct
        return context

    def post(self, request, *args, **kwargs):
        # Update VoidForger configurations here.

        ##############################
        # PERMISSION CHECK FOR - UPDATE_VOIDFORGER_CONFIGURATIONS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_VOIDFORGER_CONFIGURATIONS
        ):
            messages.error(self.request, "You do not have permission to update VoidForger configurations.")
            return redirect('voidforger:configuration')
        ##############################

        config: VoidForger = VoidForger.objects.filter(user=request.user).first()

        if config:
            try:
                llm_model_id = request.POST.getlist('llm_model_id')
                llm_model = LLMCore.objects.filter(id__in=llm_model_id).first()

                additional_instructions = request.POST.get('additional_instructions')
                tone = request.POST.get('tone')
                response_language = request.POST.get('response_language')
                maximum_actions_per_cycle = request.POST.get('maximum_actions_per_cycle')
                auto_run_max_lifetime_cycles = request.POST.get('auto_run_max_lifetime_cycles')
                auto_run_trigger_interval_minutes = request.POST.get('auto_run_trigger_interval_minutes')

                if int(auto_run_trigger_interval_minutes) < 15:
                    messages.error(request, "Auto Run Trigger Interval Minutes must be at least 15 minutes.")
                    return redirect("voidforger:configuration")

                short_term_memory_max_messages = request.POST.get('short_term_memory_max_messages')

                if response_language not in [x for x, y in AGENT_SPEECH_LANGUAGES]:
                    response_language = "auto"

                config.llm_model = llm_model
                config.additional_instructions = additional_instructions
                config.tone = tone
                config.response_language = response_language
                config.maximum_actions_per_cycle = maximum_actions_per_cycle
                config.auto_run_max_lifetime_cycles = auto_run_max_lifetime_cycles
                config.auto_run_trigger_interval_minutes = auto_run_trigger_interval_minutes
                config.short_term_memory_max_messages = short_term_memory_max_messages

                config.save()

            except Exception as e:
                logger.error(f"Error while updating VoidForger configuration: {e}")
                messages.error(request, "Error while updating VoidForger configuration.")
                return redirect("voidforger:configuration")

        messages.success(request, "VoidForger Configuration updated successfully.")
        return redirect("voidforger:configuration")
