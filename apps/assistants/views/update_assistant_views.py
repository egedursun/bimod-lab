#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant, ASSISTANT_RESPONSE_LANGUAGES, CONTEXT_OVERFLOW_STRATEGY, VECTORIZERS
from apps.assistants.utils import ContextOverflowStrategyNames, VectorizerNames, MULTI_STEP_REASONING_CAPABILITY_CHOICE
from apps.data_security.models import NERIntegration
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class UpdateAssistantView(LoginRequiredMixin, TemplateView):
    """
    Handles updating an existing assistant's details.

    This view allows users with the appropriate permissions to modify an assistant's attributes, including its name, description, instructions, and more. It also handles the logic for updating the assistant's glossary, context overflow strategy, and other configurations.

    Methods:
        get_context_data(self, **kwargs): Retrieves the current assistant's details and adds them to the context, along with other relevant data.
        post(self, request, *args, **kwargs): Handles form submission for updating the assistant, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        assistant_id = self.kwargs.get('pk')
        assistant = get_object_or_404(Assistant, id=assistant_id)
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        context['llm_models'] = LLMCore.objects.filter(organization__in=context['organizations'])
        context['assistant'] = assistant
        context['response_languages'] = ASSISTANT_RESPONSE_LANGUAGES
        context['context_overflow_strategies'] = CONTEXT_OVERFLOW_STRATEGY
        context['reasoning_capability_choices'] = MULTI_STEP_REASONING_CAPABILITY_CHOICE
        context['vectorizers'] = VECTORIZERS
        context["assistant_current_strategy"] = ContextOverflowStrategyNames.as_dict()[
            assistant.context_overflow_strategy]
        context["assistant_current_vectorizer"] = VectorizerNames.as_dict()[
            assistant.vectorizer_name] if assistant.vectorizer_name else None
        context["ner_integrations"] = NERIntegration.objects.filter(
            organization__in=context['organizations']
        )
        return context

    def post(self, request, *args, **kwargs):
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - UPDATE_ASSISTANTS
        if not UserPermissionManager.is_authorized(user=context_user, operation=PermissionNames.UPDATE_ASSISTANTS):
            messages.error(self.request, "You do not have permission to update assistants.")
            return redirect('assistants:list')
        ##############################

        assistant_id = self.kwargs.get('pk')
        assistant = get_object_or_404(Assistant, id=assistant_id)
        assistant.name = request.POST.get('name')
        assistant.description = request.POST.get('description')
        assistant.instructions = request.POST.get('instructions')
        assistant.audience = request.POST.get('audience')
        assistant.max_retry_count = request.POST.get('max_retry_count')
        assistant.tool_max_attempts_per_instance = request.POST.get('tool_max_attempts_per_instance')
        assistant.tool_max_chains = request.POST.get('tool_max_chains')

        ner_integration_id = None
        if ("ner_integration" in request.POST and request.POST.get('ner_integration')
            and request.POST.get('ner_integration') != "None"
            and request.POST.get('ner_integration') != ""):
            ner_integration_id = request.POST.get('ner_integration')

        if ner_integration_id:
            assistant.ner_integration = NERIntegration.objects.get(id=ner_integration_id)
        else:
            assistant.ner_integration = None

        terms = request.POST.getlist('terms[]')
        definitions = request.POST.getlist('definitions[]')
        updated_glossary = {}
        for term, definition in zip(terms, definitions):
            updated_glossary[term] = definition
        assistant.glossary = updated_glossary

        assistant.context_overflow_strategy = request.POST.get('context_overflow_strategy')
        assistant.max_context_messages = request.POST.get('max_context_messages')
        vectorizer_name = None
        vectorizer_api_key = None
        if assistant.context_overflow_strategy == ContextOverflowStrategyNames.FORGET:
            pass
        elif assistant.context_overflow_strategy == ContextOverflowStrategyNames.STOP:
            pass
        elif assistant.context_overflow_strategy == ContextOverflowStrategyNames.VECTORIZE:
            vectorizer_name = request.POST.get('vectorizer_name')
            vectorizer_api_key = request.POST.get('vectorizer_api_key')

        assistant.vectorizer_name = vectorizer_name
        assistant.vectorizer_api_key = vectorizer_api_key

        assistant.tone = request.POST.get('tone')
        assistant.llm_model_id = request.POST.get('llm_model')
        assistant.response_template = request.POST.get('response_template')
        assistant.response_language = request.POST.get('response_language')
        assistant.time_awareness = request.POST.get('time_awareness') == 'on'
        assistant.place_awareness = request.POST.get('place_awareness') == 'on'
        assistant.image_generation_capability = request.POST.get('image_generation_capability') == 'on'
        assistant.multi_step_reasoning_capability_choice = request.POST.get('multi_step_reasoning_capability_choice')
        assistant.last_updated_by_user = request.user
        if 'assistant_image' in request.FILES:
            assistant.assistant_image = request.FILES['assistant_image']
        assistant.save()

        return redirect('assistants:update', pk=assistant.id)
