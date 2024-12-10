#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: perform_level_synthesis_views.py
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

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import (
    get_object_or_404,
    redirect
)

from django.views import View

from apps.core.brainstorms.brainstorms_executor import (
    BrainstormsExecutor
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.brainstorms.models import BrainstormingSession
from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class BrainstormingView_LevelSynthesis(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        ss_id = self.kwargs.get('session_id')
        depth_level = request.POST.get('depth_level', 1)

        session = get_object_or_404(
            BrainstormingSession,
            id=ss_id,
            created_by_user=request.user
        )

        ##############################
        # PERMISSION CHECK FOR - CREATE_BRAINSTORMING_SYNTHESES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.CREATE_BRAINSTORMING_SYNTHESES
        ):
            messages.error(self.request, "You do not have permission to create brainstorming syntheses.")
            return redirect('brainstorms:detail_session', session_id=session.id)
        ##############################

        xc = BrainstormsExecutor(session=session)

        xc.generate_level_synthesis(
            depth_level=int(depth_level)
        )

        messages.success(request, f'Level synthesis for level {depth_level} generated successfully.')
        logger.info(f'Level synthesis for level {depth_level} generated successfully. Session ID: {session.id}')

        return redirect(
            'brainstorms:detail_session',
            session_id=session.id
        )
