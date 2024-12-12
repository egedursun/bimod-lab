#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_chat_message_models.py
#  Last Modified: 2024-11-15 16:08:02
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 18:23:45
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

from django.db import models

from apps.multimodal_chat.utils import CHAT_MESSAGE_ROLE_SENDER_TYPES

logger = logging.getLogger(__name__)


class MultimodalVoidForgerChatMessage(models.Model):
    multimodal_voidforger_chat = models.ForeignKey(
        'voidforger.MultimodalVoidForgerChat',
        on_delete=models.CASCADE,
        related_name='voidforger_chat_messages'
    )

    sender_type = models.CharField(
        max_length=100,
        choices=CHAT_MESSAGE_ROLE_SENDER_TYPES
    )

    message_text_content = models.TextField()

    message_json_content = models.JSONField(
        default=dict,
        blank=True,
        null=True
    )  # Not used for now

    message_image_contents = models.JSONField(
        default=list,
        blank=True,
        null=True
    )

    message_file_contents = models.JSONField(
        default=list,
        blank=True,
        null=True
    )

    message_audio = models.URLField(
        max_length=10000,
        blank=True,
        null=True
    )

    hidden = models.BooleanField(default=False)

    sent_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.multimodal_voidforger_chat.chat_name} - {self.sender_type} - {self.sent_at}"

    class Meta:
        verbose_name = "Multimodal VoidForger Chat Message"
        verbose_name_plural = "Multimodal VoidForger Chat Messages"
        ordering = ["-sent_at"]
        indexes = [
            models.Index(fields=[
                'multimodal_voidforger_chat'
            ]),
            models.Index(fields=[
                'sender_type'
            ]),
            models.Index(fields=[
                'sent_at'
            ]),
            models.Index(fields=[
                'multimodal_voidforger_chat',
                'sender_type'
            ]),
            models.Index(fields=[
                'multimodal_voidforger_chat',
                'sent_at'
            ]),
            models.Index(fields=[
                'sender_type',
                'sent_at'
            ]),
            models.Index(fields=[
                'multimodal_voidforger_chat',
                'sender_type',
                'sent_at'
            ]),
        ]

    def token_cost_surpasses_the_balance(self, total_billable_cost):
        return self.multimodal_voidforger_chat.voidforger.llm_model.organization.balance < total_billable_cost

    def save(self, *args, **kwargs):
        from apps.voidforger.models import MultimodalVoidForgerChat
        super().save(*args, **kwargs)

        MultimodalVoidForgerChat.objects.get(
            id=self.multimodal_voidforger_chat.id
        ).voidforger_chat_messages.add(self)

        # create the vector object on creation of the message object
        from apps.voidforger.models import VoidForgerOldChatMessagesVectorData

        try:
            _, _ = VoidForgerOldChatMessagesVectorData.objects.get_or_create(
                voidforger_chat_message=self
            )

        except Exception as e:
            logger.error(f"Error creating vector data for chat message, continuing without vectorization: {e}")
            pass
