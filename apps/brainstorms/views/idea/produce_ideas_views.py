#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: produce_ideas_views.py
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

from apps._services.brainstorms.brainstorms_executor import BrainstormsExecutor
from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.brainstorms.models import BrainstormingSession
from apps.user_permissions.utils import PermissionNames


class GenerateIdeasView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        session_id = self.kwargs.get('session_id')

        ##############################
        # PERMISSION CHECK FOR - CREATE_BRAINSTORMING_IDEAS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CREATE_BRAINSTORMING_IDEAS):
            messages.error(self.request, "You do not have permission to create brainstorming ideas.")
            return redirect('brainstorms:detail_session', session_id=session_id)
        ##############################

        depth_level = request.POST.get('depth_level', 1)
        session = get_object_or_404(BrainstormingSession, id=session_id, created_by_user=request.user)

        executor = BrainstormsExecutor(session=session)
        executor.produce_ideas(depth_level=int(depth_level))
        messages.success(request, f'Ideas for level {depth_level} generated successfully.')
        return redirect('brainstorms:detail_session', session_id=session.id)
