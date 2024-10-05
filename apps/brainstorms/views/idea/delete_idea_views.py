#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: delete_idea_views.py
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
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.brainstorms.models import BrainstormingIdea
from apps.user_permissions.utils import PermissionNames


class DeleteIdeaView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        idea_id = self.kwargs.get('idea_id')
        idea = get_object_or_404(BrainstormingIdea, id=idea_id, created_by_user=request.user)

        ##############################
        # PERMISSION CHECK FOR - DELETE_BRAINSTORMING_IDEAS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_BRAINSTORMING_IDEAS):
            messages.error(self.request, "You do not have permission to delete ideas.")
            return redirect('brainstorms:detail_session', session_id=idea.brainstorming_session.id)
        ##############################

        session_id = idea.brainstorming_session.id
        idea.delete()

        messages.success(request, f'Idea "{idea.idea_title}" has been deleted successfully.')
        return redirect('brainstorms:detail_session', session_id=session_id)
