from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.multimodal_chat.models import MultimodalChat, ChatCreationLog, ChatMessageCreationLog, MultimodalChatMessage, \
    MultimodalLeanChat, MultimodalLeanChatMessage


@receiver(post_save, sender=MultimodalChat)
def create_chat_created_log(sender, instance, created, **kwargs):
    # Add a new periodic task for this ScheduledJob
    if created:
        ChatCreationLog.objects.create(organization=instance.assistant.organization)


@receiver(post_save, sender=MultimodalLeanChat)
def create_lean_chat_created_log(sender, instance, created, **kwargs):
    # Add a new periodic task for this ScheduledJob
    if created:
        ChatCreationLog.objects.create(organization=instance.lean_assistant.organization)


####################################################################################################


@receiver(post_save, sender=MultimodalChatMessage)
def create_chat_message_created_log(sender, instance, created, **kwargs):
    # Add a new periodic task for this ScheduledJob
    if created:
        ChatMessageCreationLog.objects.create(organization=instance.multimodal_chat.assistant.organization)


@receiver(post_save, sender=MultimodalLeanChatMessage)
def create_lean_chat_message_created_log(sender, instance, created, **kwargs):
    # Add a new periodic task for this ScheduledJob
    if created:
        ChatMessageCreationLog.objects.create(organization=instance.multimodal_lean_chat.lean_assistant.organization)
