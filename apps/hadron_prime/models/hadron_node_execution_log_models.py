#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: hadron_node_execution_log_models.py
#  Last Modified: 2024-10-18 00:18:55
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-18 00:18:55
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

from apps.hadron_prime.utils import (
    HADRON_NODE_EXECUTION_STATUSES,
    HadronNodeExecutionStatusesNames
)


class HadronNodeExecutionLog(models.Model):
    node = models.ForeignKey(
        'HadronNode',
        on_delete=models.CASCADE
    )

    execution_log = models.TextField(null=True, blank=True)

    execution_status = models.CharField(
        max_length=100,
        choices=HADRON_NODE_EXECUTION_STATUSES,
        default=HadronNodeExecutionStatusesNames.DEACTIVE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.node} - {self.created_at}"

    class Meta:
        verbose_name = 'Hadron Node Execution Log'
        verbose_name_plural = 'Hadron Node Execution Logs'

        ordering = ['-created_at']

        indexes = [
            models.Index(fields=[
                'node',
                'created_at'
            ]),
        ]
