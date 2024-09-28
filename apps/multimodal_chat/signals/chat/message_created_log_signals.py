#  Copyright Policy & Ownership
#
#  Bimod.io is a product of BMD Holdings. All materials, including but not limited to software, code, documentation,
#  graphics, design elements, and user interfaces provided by Bimod.io are protected by copyright law and international
#  treaties.
#  All content within Bimod.io is the exclusive property of BMD Holdings, unless otherwise stated.
#  Unauthorized use, distribution, or reproduction of any material contained in this software without the express
#  written consent of BMD Holdings is strictly prohibited.
#  Users may not copy, modify, distribute, display, perform, or create derivative works of Bimod.io without prior
#  written permission from BMD Holdings.


from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.multimodal_chat.models import MultimodalChatMessage, ChatMessageCreationLog


@receiver(post_save, sender=MultimodalChatMessage)
def create_chat_message_created_log(sender, instance, created, **kwargs):
    # Add a new periodic task for this ScheduledJob
    if created:
        ChatMessageCreationLog.objects.create(organization=instance.multimodal_chat.assistant.organization)
