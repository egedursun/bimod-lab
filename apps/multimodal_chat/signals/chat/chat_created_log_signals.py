#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: chat_created_log_signals.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:43
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

#
from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.multimodal_chat.models import MultimodalChat, ChatCreationLog


@receiver(post_save, sender=MultimodalChat)
def create_chat_created_log(sender, instance, created, **kwargs):
    # Add a new periodic task for this ScheduledJob
    if created:
        ChatCreationLog.objects.create(organization=instance.assistant.organization)
