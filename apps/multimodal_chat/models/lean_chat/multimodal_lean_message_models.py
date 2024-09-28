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
