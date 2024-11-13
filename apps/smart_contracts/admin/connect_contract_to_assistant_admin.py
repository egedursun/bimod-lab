#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: connect_contract_to_assistant_admin.py
#  Last Modified: 2024-11-13 04:11:37
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 04:11:37
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
class SmartContractAssistantConnection(models.Model):
    smart_contract = models.ForeignKey("smart_contracts.BlockchainSmartContract", on_delete=models.CASCADE)
    assistant = models.ForeignKey("assistants.Assistant", on_delete=models.CASCADE)

    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.assistant} - {self.smart_contract}"

    class Meta:
        unique_together = ("smart_contract", "assistant")
        verbose_name = "Smart Contract Assistant Connection"
        verbose_name_plural = "Smart Contract Assistant Connections"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["smart_contract", "assistant"]),
            models.Index(fields=["assistant", "smart_contract"]),
        ]

"""

from django.contrib import admin

from apps.smart_contracts.models import SmartContractAssistantConnection
from apps.smart_contracts.utils import SMART_CONTRACT_ASSISTANT_CONNECTION_ADMIN_LIST, \
    SMART_CONTRACT_ASSISTANT_CONNECTION_ADMIN_FILTER, SMART_CONTRACT_ASSISTANT_CONNECTION_ADMIN_SEARCH


@admin.register(SmartContractAssistantConnection)
class SmartContractAssistantConnectionAdmin(admin.ModelAdmin):
    list_display = SMART_CONTRACT_ASSISTANT_CONNECTION_ADMIN_LIST
    list_filter = SMART_CONTRACT_ASSISTANT_CONNECTION_ADMIN_FILTER
    search_fields = SMART_CONTRACT_ASSISTANT_CONNECTION_ADMIN_SEARCH
    ordering = ["-created_at"]
