from django.db import models


# Create your models here.

"""
class MultimodalChat(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255)

    created_by_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='multimodal_chats')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Chat Messages
    messages = models.ForeignKey('multimodal_chat.MultimodalChatMessage', on_delete=models.CASCADE,
                                 related_name='multimodal_chat')


class MultimodalChatMessage(models.Model):
    multimodal_chat = models.ForeignKey('multimodal_chat.MultimodalChat', on_delete=models.CASCADE,
                                        related_name='messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='multimodal_chat_messages')

    def __str__(self):
        return f"{self.multimodal_chat.nickname} - {self.created_at}"

    class Meta:
        verbose_name = "Multimodal Chat Message"
        verbose_name_plural = "Multimodal Chat Messages"
        ordering = ["-created_at"]
"""
