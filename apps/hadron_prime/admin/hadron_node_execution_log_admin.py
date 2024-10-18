#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: hadron_node_execution_log_admin.py
#  Last Modified: 2024-10-18 00:21:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-18 00:21:22
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


"""
class HadronNodeExecutionLog(models.Model):
    node = models.ForeignKey('HadronNode', on_delete=models.CASCADE)
    execution_log = models.TextField(null=True, blank=True)  # leave empty for now
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.node} - {self.created_at}"

    class Meta:
        verbose_name = 'Hadron Node Execution Log'
        verbose_name_plural = 'Hadron Node Execution Logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['node', 'created_at']),
        ]

"""

from django.contrib import admin

from apps.hadron_prime.models.hadron_node_execution_log_models import HadronNodeExecutionLog
from apps.hadron_prime.utils import HADRON_NODE_EXECUTION_LOG_ADMIN_LIST, HADRON_NODE_EXECUTION_LOG_ADMIN_FILTER, \
    HADRON_NODE_EXECUTION_LOG_ADMIN_SEARCH


@admin.register(HadronNodeExecutionLog)
class HadronNodeExecutionLogAdmin(admin.ModelAdmin):
    list_display = HADRON_NODE_EXECUTION_LOG_ADMIN_LIST
    list_filter = HADRON_NODE_EXECUTION_LOG_ADMIN_FILTER
    search_fields = HADRON_NODE_EXECUTION_LOG_ADMIN_SEARCH
    ordering = ('-created_at',)
