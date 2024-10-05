#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: create_brainstorming_session_views.py
#  Last Modified: 2024-10-01 14:26:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: create_brainstorming_session_views.py
#  Last Modified: 2024-10-01 01:02:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-10-01 01:02:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.brainstorms.models import BrainstormingSession
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CreateBrainstormingSessionView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        context['organizations'] = Organization.objects.filter(
            users__in=[user]
        )
        context['llm_models'] = LLMCore.objects.filter(
            organization__in=context['organizations']
        )
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - CREATE_BRAINSTORMING_SESSIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CREATE_BRAINSTORMING_SESSIONS):
            messages.error(self.request, "You do not have permission to create brainstorming sessions.")
            return redirect('brainstorms:list_sessions')
        ##############################

        organization_id = request.POST.get('organization')
        llm_model_id = request.POST.get('llm_model')
        session_name = request.POST.get('session_name')
        topic_definition = request.POST.get('topic_definition')
        constraints = request.POST.get('constraints')

        if organization_id and llm_model_id and session_name and topic_definition:
            try:
                organization = Organization.objects.get(id=organization_id)
                llm_model = LLMCore.objects.get(id=llm_model_id)
                session = BrainstormingSession.objects.create(
                    organization=organization,
                    llm_model=llm_model,
                    created_by_user=request.user,
                    session_name=session_name,
                    topic_definition=topic_definition,
                    constraints=constraints
                )
                messages.success(request, "Brainstorming session created successfully!")
                return redirect('brainstorms:list_sessions')
            except Exception as e:
                messages.error(request, f"Error creating brainstorming session: {str(e)}")
        else:
            messages.error(request, "All fields are required.")
        return self.get(request, *args, **kwargs)
