from django.db import models

from apps._services.knowledge_base.memory.memory_executor import MemoryExecutor
from apps.assistants.models import ContextOverflowStrategyNames
from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection
from apps.llm_transaction.models import LLMTransaction
from apps.starred_messages.models import StarredMessage

CHAT_SOURCES = [
    ("app", "Application"),
    ("api", "API"),
    ("scheduled", "Scheduled"),
]


class ChatSourcesNames:
    APP = "app"
    API = "api"
    SCHEDULED = "scheduled"
    TRIGGERED = "triggered"


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

    # Context Memory
    context_memory_connection = models.OneToOneField(ContextHistoryKnowledgeBaseConnection, on_delete=models.CASCADE,
                                                     related_name='multimodal_chat', null=True, blank=True)

    starred_messages = models.ManyToManyField('starred_messages.StarredMessage', related_name='multimodal_chats',
                                                blank=True)

    # For archiving the chats
    is_archived = models.BooleanField(default=False)
    # Management for APIs
    chat_source = models.CharField(max_length=100, choices=CHAT_SOURCES, default="app")

    def __str__(self):
        return self.chat_name + " - " + self.assistant.name + " - " + self.user.username

    class Meta:
        verbose_name = "Multimodal Chat"
        verbose_name_plural = "Multimodal Chats"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['organization', 'assistant', 'user']),
            models.Index(fields=['organization', 'assistant', 'user', 'created_at']),
            models.Index(fields=['organization', 'assistant', 'user', 'updated_at']),
            models.Index(fields=['organization', 'assistant', 'created_at']),
            models.Index(fields=['organization', 'assistant', 'updated_at']),
            models.Index(fields=['organization', 'created_at']),
            models.Index(fields=['organization', 'updated_at']),
            models.Index(fields=['assistant', 'created_at']),
            models.Index(fields=['assistant', 'updated_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['user', 'updated_at']),
            models.Index(fields=['chat_source']),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create the knowledge base connection in the ORM
        if (self.assistant.context_overflow_strategy == ContextOverflowStrategyNames.VECTORIZE
                and self.context_memory_connection is None):
            if self.assistant.vectorizer_name is None:
                print("The assistant does not have a vectorizer name set.")
                return
            if self.assistant.vectorizer_api_key is None:
                print("The assistant does not have a vectorizer API key set.")
                return
            context_history = ContextHistoryKnowledgeBaseConnection.objects.create(
                assistant=self.assistant, chat=self, vectorizer=self.assistant.vectorizer_name,
                vectorizer_api_key=self.assistant.vectorizer_api_key
            )
            # Create the Weaviate classes for the context chat history memory
            connection = ContextHistoryKnowledgeBaseConnection.objects.get(id=context_history.id)
            self.context_memory_connection = connection
            self.save()

    def delete(self, using=None, keep_parents=False):
        # Remove the context memory connection
        if self.context_memory_connection:
            executor = MemoryExecutor(connection=self.context_memory_connection)
            executor.delete_chat_history_classes(class_name=self.context_memory_connection.class_name)
            self.context_memory_connection.delete()
        super().delete(using, keep_parents)


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
    message_json_content = models.JSONField(default=dict, blank=True, null=True)  # Not used for now
    # Multimedia Contents
    message_image_contents = models.JSONField(default=list, blank=True, null=True)
    message_file_contents = models.JSONField(default=list, blank=True, null=True)
    starred = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.multimodal_chat.chat_name} - {self.sender_type} - {self.sent_at}"

    class Meta:
        verbose_name = "Multimodal Chat Message"
        verbose_name_plural = "Multimodal Chat Messages"
        ordering = ["-sent_at"]
        indexes = [
            models.Index(fields=['multimodal_chat', 'sender_type']),
            models.Index(fields=['multimodal_chat', 'sent_at']),
            models.Index(fields=['multimodal_chat', 'sender_type', 'sent_at']),
            models.Index(fields=['multimodal_chat', 'sender_type', 'starred']),
            models.Index(fields=['multimodal_chat', 'starred']),
            models.Index(fields=['multimodal_chat', 'starred', 'sent_at']),
        ]

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
            if not self.multimodal_chat.starred_messages.filter(chat_message=self.id).exists():
                new_starred_message = StarredMessage.objects.create(
                    user=self.multimodal_chat.user, organization=self.multimodal_chat.organization,
                    assistant=self.multimodal_chat.assistant, chat=self.multimodal_chat,
                    chat_message=self, message_text=self.message_text_content,
                    sender_type=self.sender_type
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


class ChatCreationLog(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}"

    class Meta:
        verbose_name = "Chat Creation Log"
        verbose_name_plural = "Chat Creation Logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['created_at']),
        ]


class ChatMessageCreationLog(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}"

    class Meta:
        verbose_name = "Chat Message Creation Log"
        verbose_name_plural = "Chat Message Creation Logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['created_at']),
        ]
