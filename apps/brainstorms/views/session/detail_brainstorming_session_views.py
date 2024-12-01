#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: detail_brainstorming_session_views.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging
from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.brainstorms.utils import BrainstormingActionTypeNames
from apps.core.brainstorms.brainstorms_executor import BrainstormsExecutor
from apps.core.user_permissions.permission_manager import UserPermissionManager

from apps.brainstorms.models import (
    BrainstormingSession,
    BrainstormingIdea,
    BrainstormingLevelSynthesis,
    BrainstormingCompleteSynthesis
)

from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class BrainstormingView_SessionDetail(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_BRAINSTORMING_SESSIONS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_BRAINSTORMING_SESSIONS
        ):
            messages.error(self.request, "You do not have permission to list brainstorming sessions.")
            return context
        ##############################

        ss_id = self.kwargs.get('session_id')
        session = get_object_or_404(
            BrainstormingSession,
            id=ss_id,
            created_by_user=self.request.user
        )

        ideas = BrainstormingIdea.objects.filter(
            brainstorming_session=session
        ).order_by('-depth_level')

        ideas_by_depth = defaultdict(list)

        for idea in ideas:
            ideas_by_depth[idea.depth_level].append(idea)

        level_syntheses = BrainstormingLevelSynthesis.objects.filter(
            brainstorming_session=session
        )

        complete_synthesis = BrainstormingCompleteSynthesis.objects.filter(
            brainstorming_session=session
        ).first()

        max_depth_level = max(ideas_by_depth.keys(), default=1)

        context['session'] = session
        context['ideas_by_depth'] = dict(ideas_by_depth)
        context['level_syntheses'] = level_syntheses
        context['complete_synthesis'] = complete_synthesis
        context['max_depth_level'] = max_depth_level
        return context

    def post(self, request, *args, **kwargs):
        ss_id = self.kwargs.get('session_id')

        session = get_object_or_404(
            BrainstormingSession,
            id=ss_id,
            created_by_user=request.user
        )

        action = request.POST.get('action')
        xc = BrainstormsExecutor(session=session)

        if action == BrainstormingActionTypeNames.CREATE_FIRST_LAYER:
            xc.produce_ideas(depth_level=1)
            messages.success(request, "First layer of ideas created successfully.")

        elif action == BrainstormingActionTypeNames.CREATE_DEEPER_LAYER:
            depth_level = int(request.POST.get('depth_level', 1))
            xc.produce_ideas(depth_level=depth_level)
            messages.success(request, f"Layer {depth_level + 1} of ideas created successfully.")

        elif action == BrainstormingActionTypeNames.GENERATE_LEVEL_SYNTHESIS:
            depth_level = int(request.POST.get('depth_level', 1))
            xc.generate_level_synthesis(depth_level=depth_level)
            messages.success(request, f"Level synthesis for layer {depth_level} generated successfully.")

        elif action == BrainstormingActionTypeNames.GENERATE_COMPLETE_SYNTHESIS:
            xc.generate_complete_synthesis()
            messages.success(request, "Complete synthesis generated successfully.")

        logger.info(f"Action {action} performed successfully. Session ID: {session.id}")
        return redirect('brainstorms:detail_session', session_id=session.id)
