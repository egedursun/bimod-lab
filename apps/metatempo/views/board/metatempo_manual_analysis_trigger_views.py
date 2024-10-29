#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metatempo_manual_analysis_trigger_views.py
#  Last Modified: 2024-10-28 20:31:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 20:31:16
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.user_permissions.utils import PermissionNames


class MetaTempoView_TriggerManualAnalysis(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - USE_METAKANBAN_AI
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.USE_METAKANBAN_AI):
            messages.error(self.request, "You do not have permission to trigger manual analysis for a "
                                         "MetaTempo Connection.")
            return redirect('metatempo:main_board', connection_id=connection_id)
        ##############################

        # TODO-EGE: Functional view, this will manually trigger the 'overall analysis' function in the 'executor' in
        #   'core' directory.
        pass

        messages.success(request, f"Manual analysis has been successfully completed for the selected "
                                  f"MetaTempo connection.")
        return redirect('metatempo:main_board', connection_id=connection_id)
