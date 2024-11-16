#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_chat_models.py
#  Last Modified: 2024-11-15 16:08:02
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 18:30:31
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

from apps.multimodal_chat.utils import SOURCES_FOR_MULTIMODAL_CHATS


class MultimodalVoidForgerChat(models.Model):
    voidforger = models.ForeignKey('voidforger.VoidForger', on_delete=models.CASCADE,
                                   related_name='multimodal_chats', null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='multimodal_voidforger_chats',
                             default=1)
    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                                        related_name='multimodal_voidforger_chats_created_by_user')

    chat_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transactions = models.ManyToManyField('llm_transaction.LLMTransaction', related_name='multimodal_voidforger_chats',
                                          blank=True)
    chat_source = models.CharField(max_length=100, choices=SOURCES_FOR_MULTIMODAL_CHATS, default="app")

    def __str__(self):
        return self.chat_name + " - " + str(self.voidforger.id) + " - " + self.user.username

    class Meta:
        verbose_name = "Multimodal VoidForger Chat"
        verbose_name_plural = "Multimodal VoidForger Chats"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['voidforger']),
            models.Index(fields=['user']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['voidforger', 'user']),
            models.Index(fields=['voidforger', 'created_by_user']),
            models.Index(fields=['voidforger', 'created_at']),
            models.Index(fields=['voidforger', 'updated_at']),
        ]
