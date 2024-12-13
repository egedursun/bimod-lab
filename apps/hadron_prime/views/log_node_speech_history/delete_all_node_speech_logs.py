#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_system_speech_logs.py
#  Last Modified: 2024-10-22 13:59:26
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 13:59:26
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

from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.hadron_prime.models import (
    HadronNode,
    HadronNodeSpeechLog
)

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class HadronPrimeView_DeleteAllNodeSpeechLogs(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        node_id = kwargs.get('pk')

        node = HadronNode.objects.get(
            id=node_id
        )

        hadron_node_speech_logs = HadronNodeSpeechLog.objects.filter(
            node=node
        )

        ##############################
        # PERMISSION CHECK FOR - DELETE_HADRON_NODE_SPEECH_LOGS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_HADRON_NODE_SPEECH_LOGS
        ):
            messages.error(self.request, "You do not have permission to delete hadron node speech logs")
            return redirect(
                'hadron_prime:detail_hadron_node',
                pk=node_id
            )
        ##############################

        try:
            for hadron_node_speech_log in hadron_node_speech_logs:
                hadron_node_speech_log.delete()

            logger.info(f"All hadron speech logs associated with the node have been deleted.")
            messages.success(request, "All hadron speech logs associated with the node have been deleted.")

        except Exception as e:
            logger.error(f"Error deleting hadron speech logs for node: {e}")
            messages.error(request, f"Error deleting hadron speech logs for node: {e}")

        return redirect(
            'hadron_prime:detail_hadron_node',
            pk=node_id
        )
