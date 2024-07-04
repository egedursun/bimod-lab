from django.db import models
from django.db.models import QuerySet

from apps.llm_transaction.models import LLMTransaction
from apps.multimodal_chat.utils import calculate_billable_cost, calculate_internal_service_cost, calculate_tax_cost, \
    calculate_llm_cost, calculate_number_of_tokens


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


MESSAGE_SENDER_TYPES = [
    ("USER", "User"),
    ("ASSISTANT", "Assistant"),
    ("SYSTEM", "System"),
]


class MultimodalChatMessage(models.Model):
    multimodal_chat = models.ForeignKey('multimodal_chat.MultimodalChat', on_delete=models.CASCADE,
                                        related_name='messages_chat')
    transaction = models.ForeignKey('llm_transaction.LLMTransaction', on_delete=models.CASCADE,
                                    related_name='messages_transaction', blank=True, null=True)
    sender_type = models.CharField(max_length=10, choices=MESSAGE_SENDER_TYPES)
    message_text_content = models.TextField()
    message_json_content = models.JSONField(default=dict, blank=True, null=True)

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.multimodal_chat.chat_name} - {self.sender_type} - {self.sent_at}"

    class Meta:
        verbose_name = "Multimodal Chat Message"
        verbose_name_plural = "Multimodal Chat Messages"
        ordering = ["-sent_at"]

    # create the transaction on save
    def save(self, *args, **kwargs):
        ############################################################
        # BALANCE MANAGEMENT (TODO: handling errors when the balance is not enough)
        ############################################################
        # calculate the cost, if the balance is not enough, return False
        number_of_tokens = calculate_number_of_tokens("cl100k_base", self.message_text_content)
        llm_cost = calculate_llm_cost(self.multimodal_chat.assistant.llm_model.model_name, number_of_tokens)
        internal_service_cost = calculate_internal_service_cost(llm_cost)
        tax_cost = calculate_tax_cost(internal_service_cost)
        total_billable_cost = calculate_billable_cost(internal_service_cost, tax_cost)
        if self.sender_type == MessageSenderTypeNames.USER and (self.multimodal_chat.organization.balance < total_billable_cost):
            return False, {
                "message": "Insufficient balance.",
                "balance": self.multimodal_chat.organization.balance,
                "total_billable_cost": total_billable_cost
            }
        ############################################################

        if not self.transaction:
            self.transaction = LLMTransaction.objects.create(
                organization=self.multimodal_chat.organization,
                model=self.multimodal_chat.assistant.llm_model,
                responsible_user=self.multimodal_chat.user,
                encoding_engine="cl100k_base",
                transaction_context_content=self.message_text_content,
                llm_cost=0,
                internal_service_cost=0,
                tax_cost=0,
                total_cost=0,
                total_billable_cost=0,
            )

        # append the transaction to the list of transactions in the chat object
        MultimodalChat.objects.get(id=self.multimodal_chat.id).transactions.add(self.transaction)
        super().save(*args, **kwargs)
        MultimodalChat.objects.get(id=self.multimodal_chat.id).chat_messages.add(self.id)

