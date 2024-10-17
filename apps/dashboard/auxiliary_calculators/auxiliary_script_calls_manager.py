#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auxiliary_script_calls_manager.py
#  Last Modified: 2024-10-09 21:51:32
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 21:51:32
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


class AuxiliaryScriptCallsManager:
    @staticmethod
    def calculate_total_script_calls_per_assistants(agents, txs, n_days):
        result = {}
        for a in agents:
            txs = txs.filter(
                responsible_assistant=a,
                created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            total = 0
            for tx in txs:
                if tx.transaction_source in [LLMTransactionSourcesTypesNames.INTERNAL_SCRIPT_RETRIEVAL,
                                             LLMTransactionSourcesTypesNames.EXTERNAL_SCRIPT_RETRIEVAL]:
                    total += 1
            result[a.name] = total
        return result

    @staticmethod
    def calculate_total_external_script_calls_per_assistants(agents, txs, n_days):
        result = {}
        for a in agents:
            txs = txs.filter(
                responsible_assistant=a,
                created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            total = 0
            for tx in txs:
                if tx.transaction_source in [LLMTransactionSourcesTypesNames.EXTERNAL_SCRIPT_RETRIEVAL]:
                    total += 1
            result[a.name] = total
        return result

    @staticmethod
    def calculate_total_internal_script_calls_per_assistants(agents, txs, n_days):
        result = {}
        for a in agents:
            txs = txs.filter(
                responsible_assistant=a, created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            total = 0
            for tx in txs:
                if tx.transaction_source in [LLMTransactionSourcesTypesNames.INTERNAL_SCRIPT_RETRIEVAL]:
                    total += 1
            result[a.name] = total
        return result
