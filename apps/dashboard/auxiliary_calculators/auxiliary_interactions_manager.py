#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auxiliary_interactions_manager.py
#  Last Modified: 2024-10-09 21:52:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 21:52:58
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.utils import timezone

from apps.export_assistants.models import RequestLog

from apps.multimodal_chat.models import (
    ChatCreationLog,
    ChatMessageCreationLog
)


class AuxiliaryInteractionsManager:

    @staticmethod
    def calculate_total_chats_per_organizations(
        orgs,
        n_days
    ):

        result = {}

        for org in orgs:
            chats = ChatCreationLog.objects.filter(
                organization=org,
                created_at__gte=timezone.now() - timezone.timedelta(
                    days=n_days
                )
            )

            total = chats.count()

            if total > 0:
                result[org.name] = total

        return result

    @staticmethod
    def calculate_total_messages_per_organizations(
        orgs,
        n_days
    ):

        result = {}

        for org in orgs:
            msgs = ChatMessageCreationLog.objects.filter(
                organization=org,
                created_at__gte=timezone.now() - timezone.timedelta(
                    days=n_days
                )
            )

            total = msgs.count()

            if total > 0:
                result[org.name] = total

        return result

    @staticmethod
    def calculate_total_request_count_per_exported_assistants(
        exp_agents,
        n_days
    ):

        result = {}

        for exp_a in exp_agents:
            reqs = RequestLog.objects.filter(
                export_assistant=exp_a,
                timestamp__gte=timezone.now() - timezone.timedelta(
                    days=n_days
                )
            )

            total = reqs.count()

            if total > 0:
                result[exp_a.assistant.name] = total

        return result
