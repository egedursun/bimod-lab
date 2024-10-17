#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: lean_chat_created_log_signals.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#


from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.multimodal_chat.models import MultimodalLeanChat, ChatCreationLog


@receiver(post_save, sender=MultimodalLeanChat)
def create_lean_chat_created_log(sender, instance, created, **kwargs):
    if created:
        ChatCreationLog.objects.create(organization=instance.lean_assistant.organization)
