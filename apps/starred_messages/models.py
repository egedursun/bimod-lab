from django.db import models


STARRED_MESSAGE_SENDER_TYPES = [
    ("USER", "User"),
    ("ASSISTANT", "Assistant"),
]


class StarredMessage(models.Model):
    # Foreign keys
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    organization = models.ForeignKey("organization.Organization", on_delete=models.CASCADE)
    assistant = models.ForeignKey("assistants.Assistant", on_delete=models.CASCADE)
    chat = models.ForeignKey("multimodal_chat.MultimodalChat", on_delete=models.CASCADE)
    chat_message = models.ForeignKey("multimodal_chat.MultimodalChatMessage", on_delete=models.CASCADE)
    sender_type = models.CharField(max_length=10, choices=STARRED_MESSAGE_SENDER_TYPES, default="USER")

    # Original field derived from chat_message
    message_text = models.TextField(blank=True, null=True)

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
            models.Index(fields=["user", "organization", "assistant", "chat", "chat_message", "sender_type", "starred_at"]),
        ]

    def __str__(self):
        return f"{self.user} starred {self.chat_message}"

    def save(self, *args, **kwargs):
        self.message_text = self.chat_message.message_text_content
        super().save(*args, **kwargs)
