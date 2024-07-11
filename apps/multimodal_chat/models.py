import decimal

from django.db import models
from django.db.models import QuerySet

from apps.llm_transaction.models import LLMTransaction
from apps.multimodal_chat.utils import calculate_billable_cost, calculate_internal_service_cost, calculate_tax_cost, \
    calculate_llm_cost, calculate_number_of_tokens
from apps.starred_messages.models import StarredMessage


CHAT_SOURCES = [
    ("app", "Application"),
    ("api", "API"),
]


class ChatSourcesNames:
    APP = "app"
    API = "api"


# Create your models here.

class MultimodalChat(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE)
    assistant = models.ForeignKey('assistants.Assistant', on_delete=models.CASCADE,
                                  related_name='multimodal_chats', default=1)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='multimodal_chats', default=1)
    chat_name = models.CharField(max_length=255)
    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                                        related_name='multimodal_chats_created_by_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Chat Messages
    chat_messages = models.ManyToManyField('multimodal_chat.MultimodalChatMessage', related_name='multimodal_chats',
                                      blank=True)
    transactions = models.ManyToManyField('llm_transaction.LLMTransaction', related_name='multimodal_chats',
                                          blank=True)

    # Management for APIs
    chat_source = models.CharField(max_length=100, choices=CHAT_SOURCES, default="app")

    def __str__(self):
        return self.chat_name + " - " + self.assistant.name + " - " + self.user.username

    class Meta:
        verbose_name = "Multimodal Chat"
        verbose_name_plural = "Multimodal Chats"
        ordering = ["-created_at"]


class MessageSenderTypeNames:
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"
    TOOL = "TOOL"


MESSAGE_SENDER_TYPES = [
    ("USER", "User"),
    ("ASSISTANT", "Assistant"),
    ("SYSTEM", "System"),
    ("TOOL", "Tool"),
]


class MultimodalChatMessage(models.Model):
    multimodal_chat = models.ForeignKey('multimodal_chat.MultimodalChat', on_delete=models.CASCADE,
                                        related_name='messages_chat')
    sender_type = models.CharField(max_length=10, choices=MESSAGE_SENDER_TYPES)
    message_text_content = models.TextField()
    message_json_content = models.JSONField(default=dict, blank=True, null=True)
    starred = models.BooleanField(default=False)

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.multimodal_chat.chat_name} - {self.sender_type} - {self.sent_at}"

    class Meta:
        verbose_name = "Multimodal Chat Message"
        verbose_name_plural = "Multimodal Chat Messages"
        ordering = ["-sent_at"]

    def get_organization_balance(self):
        return self.multimodal_chat.organization.balance

    def token_cost_surpasses_the_balance(self, total_billable_cost):
        return self.multimodal_chat.organization.balance < total_billable_cost

    # create the transaction on save
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        MultimodalChat.objects.get(id=self.multimodal_chat.id).chat_messages.add(self.id)

        # if the message is starred, create the starred item
        if self.starred:
            StarredMessage.objects.create(
                user=self.multimodal_chat.user,
                organization=self.multimodal_chat.organization,
                assistant=self.multimodal_chat.assistant,
                chat=self.multimodal_chat,
                chat_message=self,
                message_text=self.message_text_content,
                sender_type=self.sender_type
            )
        else:
            # remove the starred item if it exists
            starred_message = StarredMessage.objects.filter(chat_message=self.id)
            if starred_message:
                starred_message.delete()

