#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: auxiliary_memory_manager.py
#  Last Modified: 2024-10-09 21:51:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 21:51:54
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
from django.utils import timezone

from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames


class AuxiliaryMemoryManager:

    @staticmethod
    def calculate_total_memory_saves_per_assistants(agents, txs, n_days):
        result = {}
        for a in agents:
            txs = txs.filter(
                responsible_assistant=a, created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            total = 0
            for tx in txs:
                if tx.transaction_source in [LLMTransactionSourcesTypesNames.STORE_MEMORY]:
                    total += 1
            result[a.name] = total
        return result

    @staticmethod
    def calculate_total_memory_retrievals_per_assistants(agents, txs, n_days):
        result = {}
        for a in agents:
            txs = txs.filter(
                responsible_assistant=a, created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            total = 0
            for tx in txs:
                if tx.transaction_source in [LLMTransactionSourcesTypesNames.RETRIEVE_MEMORY]:
                    total += 1
            result[a.name] = total
        return result
