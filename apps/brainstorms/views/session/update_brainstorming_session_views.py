#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: update_brainstorming_session_views.py
#  Last Modified: 2024-10-05 01:39:47
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

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.brainstorms.models import BrainstormingSession
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class UpdateBrainstormingSessionView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        session_id = self.kwargs.get('session_id')
        session = get_object_or_404(BrainstormingSession, id=session_id, created_by_user=self.request.user)

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['session'] = session
        context['organizations'] = Organization.objects.filter(
            users__in=[self.request.user]
        )
        context['llm_models'] = LLMCore.objects.filter(
            organization__in=context['organizations']
        )
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_BRAINSTORMING_SESSIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_BRAINSTORMING_SESSIONS):
            messages.error(self.request, "You do not have permission to update brainstorming sessions.")
            return redirect('brainstorms:list_sessions')
        ##############################

        session_id = self.kwargs.get('session_id')
        session = get_object_or_404(BrainstormingSession, id=session_id, created_by_user=request.user)

        organization_id = request.POST.get('organization')
        llm_model_id = request.POST.get('llm_model')
        session_name = request.POST.get('session_name')
        topic_definition = request.POST.get('topic_definition')
        constraints = request.POST.get('constraints')

        if organization_id and llm_model_id and session_name and topic_definition:
            try:
                organization = Organization.objects.get(id=organization_id)
                llm_model = LLMCore.objects.get(id=llm_model_id)

                session.organization = organization
                session.llm_model = llm_model
                session.session_name = session_name
                session.topic_definition = topic_definition
                session.constraints = constraints
                session.save()

                messages.success(request, "Brainstorming session updated successfully!")
                return redirect('brainstorms:list_sessions')
            except Exception as e:
                messages.error(request, f"Error updating brainstorming session: {str(e)}")
        else:
            messages.error(request, "All fields are required.")
        return self.get(request, *args, **kwargs)
