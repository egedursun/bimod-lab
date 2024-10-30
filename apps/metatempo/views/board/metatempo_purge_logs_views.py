#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metatempo_purge_logs_views.py
#  Last Modified: 2024-10-28 20:30:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 20:30:32
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
from apps.metatempo.models import MetaTempoMemberLog, MetaTempoMemberLogDaily, MetaTempoProjectOverallLog
from apps.user_permissions.utils import PermissionNames


class MetaTempoView_PurgeLogs(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        connection_id = kwargs.get('connection_id')

        ##############################
        # PERMISSION CHECK FOR - DELETE_METATEMPO_CONNECTION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_METATEMPO_CONNECTION):
            messages.error(self.request, "You do not have permission to delete MetaTempo Connection logs.")
            return redirect('metatempo:main_board', connection_id=connection_id)
        ##############################

        try:
            individual_logs_deleted, _ = MetaTempoMemberLog.objects.filter(
                metatempo_connection_id=connection_id).delete()
            daily_logs_deleted, _ = MetaTempoMemberLogDaily.objects.filter(
                metatempo_connection_id=connection_id).delete()
            overall_logs_deleted, _ = MetaTempoProjectOverallLog.objects.filter(
                metatempo_connection_id=connection_id).delete()
        except Exception as e:
            messages.error(request, f"Failed to purge logs for the selected MetaTempo connection. Error: {str(e)}")
            return redirect('metatempo:main_board', connection_id=connection_id)

        messages.success(request, f"All logs for the selected MetaTempo connection have been purged successfully.")
        return redirect('metatempo:main_board', connection_id=connection_id)
