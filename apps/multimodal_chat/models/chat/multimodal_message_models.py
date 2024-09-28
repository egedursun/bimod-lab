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


from django.db import models

from apps.multimodal_chat.utils import MESSAGE_SENDER_TYPES
from apps.starred_messages.models import StarredMessage


class MultimodalChatMessage(models.Model):
    """
    MultimodalChatMessage Model:
    - Purpose: Represents a message within a multimodal chat session. It stores the message content, sender type, multimedia contents, and whether the message is starred. The model also provides methods for managing related transactions and starred messages.
    - Key Fields:
        - `multimodal_chat`: ForeignKey linking to the `MultimodalChat` model that this message belongs to.
        - `sender_type`: Field specifying the sender type (e.g., User, Assistant).
        - `message_text_content`: The textual content of the message.
        - `message_json_content`: JSON field for storing additional message content (not used currently).
        - `message_image_contents`: JSON field for storing image contents related to the message.
        - `message_file_contents`: JSON field for storing file contents related to the message.
        - `message_audio`: URL field for storing audio contents related to the message.
        - `starred`: Boolean field indicating whether the message is starred.
        - `sent_at`: Timestamp for when the message was sent.
    - Methods:
        - `get_organization_balance()`: Retrieves the current balance of the organization associated with the chat.
        - `token_cost_surpasses_the_balance(total_billable_cost)`: Checks if the token cost surpasses the organization's balance.
        - `save()`: Overridden to handle transactions, starred messages, and related logic when the message is saved.
    - Meta:
        - `verbose_name`: "Multimodal Chat Message"
        - `verbose_name_plural`: "Multimodal Chat Messages"
        - `ordering`: Orders messages by sent date in descending order.
        - `indexes`: Indexes on various fields for optimized queries.
    """

    multimodal_chat = models.ForeignKey('MultimodalChat', on_delete=models.CASCADE, related_name='chat_messages')
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
        return f"{self.multimodal_chat.chat_name} - {self.sender_type} - {self.sent_at}"

    class Meta:
        verbose_name = "Multimodal Chat Message"
        verbose_name_plural = "Multimodal Chat Messages"
        ordering = ["-sent_at"]
        indexes = [
            # Single-field indexes
            models.Index(fields=['multimodal_chat']),
            models.Index(fields=['sender_type']),
            models.Index(fields=['starred']),
            models.Index(fields=['sent_at']),

            # Two-field composite indexes
            models.Index(fields=['multimodal_chat', 'sender_type']),
            models.Index(fields=['multimodal_chat', 'starred']),
            models.Index(fields=['multimodal_chat', 'sent_at']),
            models.Index(fields=['sender_type', 'starred']),
            models.Index(fields=['sender_type', 'sent_at']),
            models.Index(fields=['starred', 'sent_at']),

            # Three-field composite indexes
            models.Index(fields=['multimodal_chat', 'sender_type', 'starred']),
            models.Index(fields=['multimodal_chat', 'sender_type', 'sent_at']),
            models.Index(fields=['multimodal_chat', 'starred', 'sent_at']),
            models.Index(fields=['sender_type', 'starred', 'sent_at']),

            # Four-field composite indexes
            models.Index(fields=['multimodal_chat', 'sender_type', 'starred', 'sent_at']),
        ]

    def get_organization_balance(self):
        return self.multimodal_chat.organization.balance

    def token_cost_surpasses_the_balance(self, total_billable_cost):
        return self.multimodal_chat.organization.balance < total_billable_cost

    # create the transaction on save
    def save(self, *args, **kwargs):
        from apps.multimodal_chat.models import MultimodalChat

        super().save(*args, **kwargs)
        MultimodalChat.objects.get(id=self.multimodal_chat.id).chat_messages.add(self)
        # if the message is starred, create the starred item
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
            # remove the starred item if it exists
            starred_message = StarredMessage.objects.filter(chat_message=self.id)
            if starred_message:
                starred_message.delete()
