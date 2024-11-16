#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_action_memory_logs_models.py
#  Last Modified: 2024-11-15 15:58:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 18:25:28
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from django.db import models

from apps.voidforger.utils import VOIDFORGER_ACTION_TYPES

logger = logging.getLogger(__name__)


class VoidForgerActionMemoryLog(models.Model):
    voidforger = models.ForeignKey('voidforger.VoidForger', on_delete=models.CASCADE)
    action_type = models.CharField(max_length=255, choices=VOIDFORGER_ACTION_TYPES)
    action_order_raw_text = models.TextField(null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.voidforger.id} - {self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}'

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'VoidForger Action Memory Log'
        verbose_name_plural = 'VoidForger Action Memory Logs'
        indexes = [
            models.Index(fields=['voidforger', 'action_type']),
            models.Index(fields=['voidforger', 'timestamp']),
            models.Index(fields=['voidforger', 'action_type', 'timestamp']),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # create the vector object on creation of the log object
        from apps.voidforger.models import VoidForgerActionMemoryVectorData
        try:
            _, _ = VoidForgerActionMemoryVectorData.objects.get_or_create(voidforger_action_memory=self)
        except Exception as e:
            logger.error(f"Error creating vector data for action memory log, continuing without vectorization: {e}")
            pass
