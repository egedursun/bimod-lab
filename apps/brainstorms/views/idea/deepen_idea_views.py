#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: deepen_idea_views.py
#  Last Modified: 2024-10-08 18:46:36
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-08 18:46:38
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
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps.core.brainstorms.brainstorms_executor import BrainstormsExecutor
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.brainstorms.models import BrainstormingSession, BrainstormingIdea
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class BrainstormingView_IdeaDeepen(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        idea_id = self.kwargs.get('idea_id')
        idea = get_object_or_404(BrainstormingIdea, id=idea_id)
        session = idea.brainstorming_session

        ##############################
        # PERMISSION CHECK FOR - CREATE_BRAINSTORMING_IDEAS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.CREATE_BRAINSTORMING_IDEAS
        ):
            messages.error(self.request, "You do not have permission to create brainstorming ideas.")
            return redirect('brainstorms:detail_session', session_id=session.id)
        ##############################

        session = get_object_or_404(
            BrainstormingSession,
            id=session.id,
            created_by_user=request.user
        )
        xc = BrainstormsExecutor(session=session)
        xc.deepen_thought_over_idea(idea=idea)

        messages.success(request, f'Idea {idea.id} deepened successfully.')
        logger.info(f'Idea {idea.id} deepened successfully.')
        return redirect('brainstorms:detail_session', session_id=session.id)
