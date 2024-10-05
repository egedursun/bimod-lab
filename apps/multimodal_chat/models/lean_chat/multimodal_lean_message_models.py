#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: multimodal_lean_message_models.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:41
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
#  File: multimodal_lean_message_models.py
#  Last Modified: 2024-09-28 20:38:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:05:24
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

#
from django.db import models


from apps.multimodal_chat.utils import MESSAGE_SENDER_TYPES


class MultimodalLeanChatMessage(models.Model):
    multimodal_lean_chat = models.ForeignKey('MultimodalLeanChat', on_delete=models.CASCADE,
                                             related_name='lean_chat_messages')
    sender_type = models.CharField(max_length=10, choices=MESSAGE_SENDER_TYPES)
    message_text_content = models.TextField()
    message_json_content = models.JSONField(default=dict, blank=True, null=True)  # Not used for now
    # Multimedia Contents
    message_image_contents = models.JSONField(default=list, blank=True, null=True)
    message_file_contents = models.JSONField(default=list, blank=True, null=True)
    # Narrated audio
    message_audio = models.URLField(max_length=10000, blank=True, null=True)

    starred = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.multimodal_lean_chat.chat_name} - {self.sender_type} - {self.sent_at}"

    class Meta:
        verbose_name = "Multimodal Lean Chat Message"
        verbose_name_plural = "Multimodal Lean Chat Messages"
        ordering = ["-sent_at"]
        indexes = [
            # Single-field indexes
            models.Index(fields=['multimodal_lean_chat']),
            models.Index(fields=['sender_type']),
            models.Index(fields=['starred']),
            models.Index(fields=['sent_at']),
            # Two-field composite indexes
            models.Index(fields=['multimodal_lean_chat', 'sender_type']),
            models.Index(fields=['multimodal_lean_chat', 'starred']),
            models.Index(fields=['multimodal_lean_chat', 'sent_at']),
            models.Index(fields=['sender_type', 'starred']),
            models.Index(fields=['sender_type', 'sent_at']),
            models.Index(fields=['starred', 'sent_at']),
            # Three-field composite indexes
            models.Index(fields=['multimodal_lean_chat', 'sender_type', 'starred']),
            models.Index(fields=['multimodal_lean_chat', 'sender_type', 'sent_at']),
            models.Index(fields=['multimodal_lean_chat', 'starred', 'sent_at']),
            models.Index(fields=['sender_type', 'starred', 'sent_at']),
            # Four-field composite indexes
            models.Index(fields=['multimodal_lean_chat', 'sender_type', 'starred', 'sent_at']),
        ]

    def get_organization_balance(self):
        return self.multimodal_lean_chat.organization.balance

    def token_cost_surpasses_the_balance(self, total_billable_cost):
        return self.multimodal_lean_chat.organization.balance < total_billable_cost

    # create the transaction on save
    def save(self, *args, **kwargs):
        from apps.multimodal_chat.models import MultimodalLeanChat

        super().save(*args, **kwargs)
        MultimodalLeanChat.objects.get(id=self.multimodal_lean_chat.id).lean_chat_messages.add(self)
