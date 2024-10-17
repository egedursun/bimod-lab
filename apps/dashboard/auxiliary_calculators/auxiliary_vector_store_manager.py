#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auxiliary_vector_store_manager.py
#  Last Modified: 2024-10-09 21:52:11
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 21:52:12
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.utils import timezone

from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames


class AuxiliaryVectorStoreManager:

    @staticmethod
    def calculate_total_knowledge_base_searches_per_assistants(agents, txs, n_days):
        result = {}
        for a in agents:
            txs = txs.filter(responsible_assistant=a, created_at__gte=timezone.now() - timezone.timedelta(days=n_days))
            total = 0
            for tx in txs:
                if tx.transaction_source in [LLMTransactionSourcesTypesNames.KNOWLEDGE_BASE_SEARCH]:
                    total += 1
            result[a.name] = total
        return result
