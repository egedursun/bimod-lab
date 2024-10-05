#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: detail_brainstorming_session_views.py
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
#  File: detail_brainstorming_session_views.py
#  Last Modified: 2024-10-01 02:20:28
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-10-01 02:20:29
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#
from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.brainstorms.brainstorms_executor import BrainstormsExecutor
from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.brainstorms.models import BrainstormingSession, BrainstormingIdea, BrainstormingLevelSynthesis, \
    BrainstormingCompleteSynthesis
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class BrainstormingSessionDetailView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_BRAINSTORMING_SESSIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_BRAINSTORMING_SESSIONS):
            messages.error(self.request, "You do not have permission to list brainstorming sessions.")
            return context
        ##############################

        session_id = self.kwargs.get('session_id')
        session = get_object_or_404(BrainstormingSession, id=session_id, created_by_user=self.request.user)

        # Retrieve all ideas and group by depth level
        ideas = BrainstormingIdea.objects.filter(brainstorming_session=session).order_by('-depth_level')
        ideas_by_depth = defaultdict(list)
        for idea in ideas:
            ideas_by_depth[idea.depth_level].append(idea)

        # Get syntheses and complete synthesis
        level_syntheses = BrainstormingLevelSynthesis.objects.filter(brainstorming_session=session)
        complete_synthesis = BrainstormingCompleteSynthesis.objects.filter(brainstorming_session=session).first()

        # Calculate max depth level
        max_depth_level = max(ideas_by_depth.keys(), default=1)

        # Pass everything to the template
        context['session'] = session
        context['ideas_by_depth'] = dict(ideas_by_depth)
        context['level_syntheses'] = level_syntheses
        context['complete_synthesis'] = complete_synthesis
        context['max_depth_level'] = max_depth_level

        return context

    def post(self, request, *args, **kwargs):
        # Handle post actions (e.g., create first layer of ideas)
        session_id = self.kwargs.get('session_id')
        session = get_object_or_404(BrainstormingSession, id=session_id, created_by_user=request.user)
        action = request.POST.get('action')

        executor = BrainstormsExecutor(session=session)

        if action == 'create_first_layer':
            executor.produce_ideas(depth_level=1)
            messages.success(request, "First layer of ideas created successfully.")
        elif action == 'create_deeper_layer':
            depth_level = int(request.POST.get('depth_level', 1))
            executor.produce_ideas(depth_level=depth_level)
            messages.success(request, f"Layer {depth_level + 1} of ideas created successfully.")
        elif action == 'generate_level_synthesis':
            depth_level = int(request.POST.get('depth_level', 1))
            executor.generate_level_synthesis(depth_level=depth_level)
            messages.success(request, f"Level synthesis for layer {depth_level} generated successfully.")
        elif action == 'generate_complete_synthesis':
            executor.generate_complete_synthesis()
            messages.success(request, "Complete synthesis generated successfully.")

        return redirect('brainstorms:detail_session', session_id=session.id)
