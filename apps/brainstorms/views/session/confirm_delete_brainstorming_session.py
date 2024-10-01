#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: confirm_delete_brainstorming_session.py
#  Last Modified: 2024-10-01 01:02:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-10-01 01:02:45
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
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.brainstorms.models import BrainstormingSession
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DeleteBrainstormingSessionView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        session_id = self.kwargs.get('session_id')
        session = get_object_or_404(BrainstormingSession, id=session_id, created_by_user=self.request.user)

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['session'] = session
        return context

    def post(self, request, *args, **kwargs):
        session_id = self.kwargs.get('session_id')
        session = get_object_or_404(BrainstormingSession, id=session_id, created_by_user=request.user)

        ##############################
        # PERMISSION CHECK FOR - DELETE_BRAINSTORMING_SESSIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_BRAINSTORMING_SESSIONS):
            messages.error(self.request, "You do not have permission to delete brainstorming sessions.")
            return redirect('brainstorms:list_sessions')
        ##############################

        try:
            session_name = session.session_name
            session.delete()  # Delete the brainstorming session from the system
            messages.success(request, f'The session "{session_name}" was deleted successfully.')
        except Exception as e:
            messages.error(request, f"Error deleting session: {str(e)}")
            return self.get(request, *args, **kwargs)

        return redirect('brainstorms:list_sessions')
