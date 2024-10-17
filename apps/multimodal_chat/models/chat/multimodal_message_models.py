#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: multimodal_message_models.py
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


from django.db import models

from apps.multimodal_chat.utils import CHAT_MESSAGE_ROLE_SENDER_TYPES
from apps.starred_messages.models import StarredMessage


class MultimodalChatMessage(models.Model):
    multimodal_chat = models.ForeignKey('MultimodalChat', on_delete=models.CASCADE, related_name='chat_messages')
    sender_type = models.CharField(max_length=10, choices=CHAT_MESSAGE_ROLE_SENDER_TYPES)
    message_text_content = models.TextField()
    message_json_content = models.JSONField(default=dict, blank=True, null=True)  # Not used for now
    message_image_contents = models.JSONField(default=list, blank=True, null=True)
    message_file_contents = models.JSONField(default=list, blank=True, null=True)
    message_audio = models.URLField(max_length=10000, blank=True, null=True)
    starred = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.multimodal_chat.chat_name} - {self.sender_type} - {self.sent_at}"

    class Meta:
        verbose_name = "Multimodal Chat Message"
        verbose_name_plural = "Multimodal Chat Messages"
        ordering = ["-sent_at"]
        indexes = [
            models.Index(fields=['multimodal_chat']),
            models.Index(fields=['sender_type']),
            models.Index(fields=['starred']),
            models.Index(fields=['sent_at']),
            models.Index(fields=['multimodal_chat', 'sender_type']),
            models.Index(fields=['multimodal_chat', 'starred']),
            models.Index(fields=['multimodal_chat', 'sent_at']),
            models.Index(fields=['sender_type', 'starred']),
            models.Index(fields=['sender_type', 'sent_at']),
            models.Index(fields=['starred', 'sent_at']),
            models.Index(fields=['multimodal_chat', 'sender_type', 'starred']),
            models.Index(fields=['multimodal_chat', 'sender_type', 'sent_at']),
            models.Index(fields=['multimodal_chat', 'starred', 'sent_at']),
            models.Index(fields=['sender_type', 'starred', 'sent_at']),
            models.Index(fields=['multimodal_chat', 'sender_type', 'starred', 'sent_at']),
        ]

    def get_organization_balance(self):
        return self.multimodal_chat.organization.balance

    def token_cost_surpasses_the_balance(self, total_billable_cost):
        return self.multimodal_chat.organization.balance < total_billable_cost

    def save(self, *args, **kwargs):
        from apps.multimodal_chat.models import MultimodalChat
        super().save(*args, **kwargs)
        MultimodalChat.objects.get(id=self.multimodal_chat.id).chat_messages.add(self)
        if self.starred:
            if not self.multimodal_chat.starred_messages.filter(chat_message=self.id).exists():
                new_starred_message = StarredMessage.objects.create(
                    user=self.multimodal_chat.user, organization=self.multimodal_chat.organization,
                    assistant=self.multimodal_chat.assistant, chat=self.multimodal_chat,
                    chat_message=self, message_text=self.message_text_content, sender_type=self.sender_type
                )
                self.multimodal_chat.starred_messages.add(new_starred_message)
                self.multimodal_chat.save()
            else:
                pass
        else:
            starred_message = StarredMessage.objects.filter(chat_message=self.id)
            if starred_message:
                starred_message.delete()
