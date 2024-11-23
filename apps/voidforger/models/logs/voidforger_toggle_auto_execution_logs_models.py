#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_toggle_auto_execution_logs_models.py
#  Last Modified: 2024-11-15 15:47:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 18:26:43
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

from apps.voidforger.utils import VOIDFORGER_TOGGLE_AUTO_EXECUTION_ACTION_TYPES

logger = logging.getLogger(__name__)


class VoidForgerToggleAutoExecutionLog(models.Model):
    voidforger = models.ForeignKey(
        'voidforger.VoidForger',
        on_delete=models.CASCADE
    )
    action_type = models.CharField(
        max_length=20,
        choices=VOIDFORGER_TOGGLE_AUTO_EXECUTION_ACTION_TYPES
    )
    metadata = models.JSONField(default=dict, blank=True, null=True)

    responsible_user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.voidforger.id} - {self.action_type} - {self.timestamp}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # create the vector object on creation of the log object
        from apps.voidforger.models import VoidForgerAutoExecutionMemoryVectorData

        try:
            _, _ = VoidForgerAutoExecutionMemoryVectorData.objects.get_or_create(
                voidforger_auto_execution_memory=self
            )

        except Exception as e:
            logger.error(
                f"Error creating vector data for auto execution memory log, continuing without vectorization: {e}")
            pass

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'VoidForger Toggle Auto Execution Log'
        verbose_name_plural = 'VoidForger Toggle Auto Execution Logs'
        indexes = [
            models.Index(fields=[
                'voidforger',
                'action_type'
            ]),
            models.Index(fields=[
                'voidforger',
                'timestamp'
            ]),
            models.Index(fields=[
                'voidforger',
                'action_type',
                'timestamp'
            ]),
        ]
