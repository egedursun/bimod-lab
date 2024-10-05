#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: starred_message_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
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

from django.db import models

from apps.starred_messages.utils import STARRED_MESSAGE_SENDER_TYPES


class StarredMessage(models.Model):
    """
    StarredMessage Model:
    - Purpose: Represents a message that has been starred by a user in a multimodal chat. It stores references to the original message and its content, along with metadata such as the user, organization, assistant, chat, and the time the message was starred.
    - Key Fields:
        - `user`: ForeignKey linking to the `User` who starred the message.
        - `organization`: ForeignKey linking to the `Organization` associated with the starred message.
        - `assistant`: ForeignKey linking to the `Assistant` associated with the starred message.
        - `chat`: ForeignKey linking to the `MultimodalChat` in which the message was starred.
        - `chat_message`: ForeignKey linking to the original `MultimodalChatMessage` that was starred.
        - `sender_type`: The type of sender who sent the original message (e.g., User, Assistant).
        - `message_text`: Text content of the starred message, derived from the original chat message.
        - `message_image_urls`: JSONField for storing image URLs related to the starred message.
        - `message_file_urls`: JSONField for storing file URLs related to the starred message.
        - `starred_at`: Timestamp for when the message was starred.
    - Methods:
        - `save()`: Overridden to automatically populate the `message_text`, `message_file_urls`, and `message_image_urls` fields from the original chat message when the starred message is saved.
    - Meta:
        - `verbose_name`: "Starred Message"
        - `verbose_name_plural`: "Starred Messages"
        - `ordering`: Orders starred messages by the time they were starred in descending order.
        - `indexes`: Indexes on various fields for optimized queries, including combinations of `user`, `organization`, `assistant`, `chat`, `chat_message`, `sender_type`, and `starred_at`.
    """

    # Foreign keys
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    organization = models.ForeignKey("organization.Organization", on_delete=models.CASCADE)
    assistant = models.ForeignKey("assistants.Assistant", on_delete=models.CASCADE)
    chat = models.ForeignKey("multimodal_chat.MultimodalChat", on_delete=models.CASCADE,
                             related_name="starred_messages")
    chat_message = models.ForeignKey("multimodal_chat.MultimodalChatMessage", on_delete=models.CASCADE)
    sender_type = models.CharField(max_length=10, choices=STARRED_MESSAGE_SENDER_TYPES, default="USER")

    # Original field derived from chat_message
    message_text = models.TextField(blank=True, null=True)
    message_image_urls = models.JSONField(blank=True, null=True)
    message_file_urls = models.JSONField(blank=True, null=True)

    starred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Starred Message"
        verbose_name_plural = "Starred Messages"
        ordering = ["-starred_at"]
        indexes = [
            models.Index(fields=["user", "organization", "assistant", "chat", "chat_message"]),
            models.Index(fields=["user", "organization", "assistant", "chat", "starred_at"]),
            models.Index(fields=["user", "organization", "assistant", "chat", "sender_type"]),
            models.Index(fields=["user", "organization", "assistant", "chat", "sender_type", "starred_at"]),
            models.Index(fields=["user", "organization", "assistant", "chat", "sender_type", "chat_message"]),
            models.Index(fields=["user", "organization", "assistant", "chat", "chat_message", "starred_at"]),
            models.Index(fields=["user", "organization", "assistant", "chat", "chat_message", "sender_type"]),
            models.Index(
                fields=["user", "organization", "assistant", "chat", "chat_message", "sender_type", "starred_at"]),
        ]

    def __str__(self):
        return f"{self.user} starred {self.chat_message}"

    def save(self, *args, **kwargs):
        self.message_text = self.chat_message.message_text_content
        self.message_file_urls = self.chat_message.message_file_contents
        self.message_image_urls = self.chat_message.message_image_contents
        super().save(*args, **kwargs)
