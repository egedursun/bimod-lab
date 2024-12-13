#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_topic_message_logs_views.py
#  Last Modified: 2024-10-18 22:53:24
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-18 22:53:25
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
    HadronTopic,
    HadronTopicMessage
)

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class HadronPrimeView_DeleteAllTopicMessages(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        topic_id = kwargs.get('pk')

        topic = HadronTopic.objects.get(
            id=topic_id
        )

        hadron_topic_messages = HadronTopicMessage.objects.filter(
            topic=topic
        )

        ##############################
        # PERMISSION CHECK FOR - DELETE_HADRON_TOPIC_MESSAGE_HISTORY_LOGS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_HADRON_TOPIC_MESSAGE_HISTORY_LOGS
        ):
            messages.error(self.request, "You do not have permission to delete hadron topic message history logs.")
            return redirect(
                'hadron_prime:detail_hadron_topic',
                pk=topic_id
            )
        ##############################

        try:
            for hadron_topic_message in hadron_topic_messages:
                hadron_topic_message.delete()

            logger.info(f"All hadron message history associated with the topic have been deleted.")
            messages.success(request, "All hadron message history associated with the topic have been deleted.")

        except Exception as e:
            logger.error(f"Error deleting hadron message history for topic: {e}")
            messages.error(request, f"Error deleting hadron message history for topic: {e}")

        return redirect(
            'hadron_prime:detail_hadron_topic',
            pk=topic_id
        )
