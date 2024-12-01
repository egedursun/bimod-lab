#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_assistant_views.py
#  Last Modified: 2024-10-05 12:51:58
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
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant, AGENT_SPEECH_LANGUAGES, CONTEXT_MANAGEMENT_STRATEGY
from apps.assistants.utils import ContextManagementStrategyNames, MULTI_STEP_REASONING_CAPABILITY_CHOICE
from apps.data_security.models import NERIntegration
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.projects.models import ProjectItem
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class AssistantView_Update(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        agent_id = self.kwargs.get('pk')
        agent = get_object_or_404(Assistant, id=agent_id)

        context['organizations'] = Organization.objects.filter(
            users__in=[self.request.user]
        )
        context['llm_models'] = LLMCore.objects.filter(
            organization__in=context['organizations']
        )

        context['assistant'] = agent
        context['response_languages'] = AGENT_SPEECH_LANGUAGES
        context['context_overflow_strategies'] = CONTEXT_MANAGEMENT_STRATEGY
        context['reasoning_capability_choices'] = MULTI_STEP_REASONING_CAPABILITY_CHOICE
        context["assistant_current_strategy"] = ContextManagementStrategyNames.as_dict()[
            agent.context_overflow_strategy]

        context["ner_integrations"] = NERIntegration.objects.filter(organization__in=context['organizations'])
        context["projects"] = ProjectItem.objects.filter(organization__in=context['organizations'])
        return context

    def post(self, request, *args, **kwargs):
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - UPDATE_ASSISTANTS
        if not UserPermissionManager.is_authorized(
            user=context_user,
            operation=PermissionNames.UPDATE_ASSISTANTS
        ):
            messages.error(self.request, "You do not have permission to update assistants.")
            return redirect('assistants:list')
        ##############################

        agent_id = self.kwargs.get('pk')
        try:
            agent = get_object_or_404(Assistant, id=agent_id)
            agent.name = request.POST.get('name')
            agent.description = request.POST.get('description')
            agent.instructions = request.POST.get('instructions')
            agent.audience = request.POST.get('audience')
            agent.max_retry_count = request.POST.get('max_retry_count')
            agent.tool_max_attempts_per_instance = request.POST.get('tool_max_attempts_per_instance')
            agent.tool_max_chains = request.POST.get('tool_max_chains')

            ner_id = None

            if ("ner_integration" in request.POST and request.POST.get('ner_integration')
                and request.POST.get('ner_integration') != "None"
                and request.POST.get('ner_integration') != ""):
                ner_id = request.POST.get('ner_integration')
                logger.info(f"NER Integration is defined for this agent. NER ID: {ner_id}")

            if ner_id:
                agent.ner_integration = NERIntegration.objects.get(id=ner_id)

            else:
                agent.ner_integration = None

            terms = request.POST.getlist('terms[]')
            definitions = request.POST.getlist('definitions[]')
            updated_technical_dict = {}

            for term, definition in zip(terms, definitions):
                updated_technical_dict[term] = definition

            agent.glossary = updated_technical_dict
            agent.context_overflow_strategy = request.POST.get('context_overflow_strategy')
            agent.max_context_messages = request.POST.get('max_context_messages')

            if agent.context_overflow_strategy == ContextManagementStrategyNames.FORGET:
                pass

            elif agent.context_overflow_strategy == ContextManagementStrategyNames.STOP:
                pass

            elif agent.context_overflow_strategy == ContextManagementStrategyNames.VECTORIZE:
                pass

            agent.tone = request.POST.get('tone')
            agent.llm_model_id = request.POST.get('llm_model')
            agent.response_template = request.POST.get('response_template')
            agent.response_language = request.POST.get('response_language')
            agent.time_awareness = request.POST.get('time_awareness') == 'on'
            agent.place_awareness = request.POST.get('place_awareness') == 'on'

            agent.image_generation_capability = request.POST.get('image_generation_capability') == 'on'
            agent.multi_step_reasoning_capability_choice = request.POST.get('multi_step_reasoning_capability_choice')
            agent.last_updated_by_user = request.user

            if 'assistant_image' in request.FILES:
                agent.assistant_image = request.FILES['assistant_image']

            agent.save()

            project_items = request.POST.getlist('project_items[]')
            agent.project_items.set(project_items)
            agent.save()

        except Exception as e:
            logger.error(f"Error while updating the agent information: {e}")
            messages.error(request, "Agent information is required.")
            return redirect('assistants:update', pk=agent_id)

        logger.info(f"Assistant has been updated. ")
        return redirect('assistants:update', pk=agent_id)
