#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: perform_complete_synthesis_views.py
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
#  File: perform_complete_synthesis_views.py
#  Last Modified: 2024-10-01 01:03:42
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-10-01 02:28:08
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
from django.views import View

from apps._services.brainstorms.brainstorms_executor import BrainstormsExecutor
from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.brainstorms.models import BrainstormingSession
from apps.user_permissions.utils import PermissionNames


class CreateCompleteSynthesisView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        session_id = self.kwargs.get('session_id')
        session = get_object_or_404(BrainstormingSession, id=session_id, created_by_user=request.user)

        ##############################
        # PERMISSION CHECK FOR - CREATE_BRAINSTORMING_SYNTHESES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CREATE_BRAINSTORMING_SYNTHESES):
            messages.error(self.request, "You do not have permission to create brainstorming syntheses.")
            return redirect('brainstorms:detail_session', session_id=session.id)
        ##############################

        executor = BrainstormsExecutor(session=session)
        executor.generate_complete_synthesis()

        messages.success(request, 'Complete synthesis for the entire session generated successfully.')
        return redirect('brainstorms:detail_session', session_id=session.id)
