#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: multimodal_lean_chat_models.py
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

from apps.multimodal_chat.utils import (
    SOURCES_FOR_MULTIMODAL_CHATS
)


class MultimodalLeanChat(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE
    )

    lean_assistant = models.ForeignKey(
        'leanmod.LeanAssistant',
        on_delete=models.CASCADE,
        related_name='multimodal_lean_chats',
        null=True
    )

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='multimodal_lean_chats',
        default=1
    )

    chat_name = models.CharField(max_length=255)

    created_by_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='multimodal_lean_chats_created_by_user'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    transactions = models.ManyToManyField(
        'llm_transaction.LLMTransaction',
        related_name='multimodal_lean_chats',
        blank=True
    )

    is_archived = models.BooleanField(default=False)

    chat_source = models.CharField(
        max_length=100,
        choices=SOURCES_FOR_MULTIMODAL_CHATS,
        default="app"
    )

    def __str__(self):
        return self.chat_name + " - " + self.lean_assistant.name + " - " + self.user.username

    class Meta:
        verbose_name = "Multimodal Lean Chat"
        verbose_name_plural = "Multimodal Lean Chats"

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=[
                'id'
            ]),
            models.Index(fields=[
                'organization'
            ]),
            models.Index(fields=[
                'lean_assistant'
            ]),
            models.Index(fields=[
                'user'
            ]),
            models.Index(fields=[
                'chat_source'
            ]),
            models.Index(fields=[
                'is_archived'
            ]),
            models.Index(fields=[
                'created_by_user'
            ]),
            models.Index(fields=[
                'created_at'
            ]),
            models.Index(fields=[
                'updated_at'
            ]),
            models.Index(fields=[
                'organization',
                'lean_assistant'
            ]),
            models.Index(fields=[
                'organization',
                'user'
            ]),
            models.Index(fields=[
                'organization',
                'chat_source'
            ]),
            models.Index(fields=[
                'organization',
                'is_archived'
            ]),
            models.Index(fields=[
                'organization',
                'created_by_user'
            ]),
            models.Index(fields=[
                'organization',
                'created_at'
            ]),
            models.Index(fields=[
                'organization',
                'updated_at'
            ]),
            models.Index(fields=[
                'lean_assistant',
                'user'
            ]),
            models.Index(fields=[
                'lean_assistant',
                'chat_source'
            ]),
            models.Index(fields=[
                'lean_assistant',
                'is_archived'
            ]),
            models.Index(fields=[
                'lean_assistant',
                'created_by_user'
            ]),
            models.Index(fields=[
                'lean_assistant',
                'created_at'
            ]),
            models.Index(fields=[
                'lean_assistant',
                'updated_at'
            ]),
        ]
