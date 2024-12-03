#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auxiliary_api_calls_manager.py
#  Last Modified: 2024-10-09 21:51:25
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 21:51:26
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


class AuxiliaryAPICallsManager:
    @staticmethod
    def calculate_total_internal_api_calls_per_assistants(
        agents,
        txs,
        n_days
    ):

        result = {}

        for a in agents:
            txs_f = txs.filter(
                responsible_assistant=a,
                created_at__gte=timezone.now() - timezone.timedelta(
                    days=n_days
                )
            )

            total = 0

            for tx in txs_f:
                if tx.transaction_source in [
                    LLMTransactionSourcesTypesNames.INTERNAL_API_EXECUTION
                ]:
                    total += 1

            result[a.name] = total

        return result

    @staticmethod
    def calculate_total_external_api_calls_per_assistants(
        agents,
        txs,
        n_days
    ):

        result = {}

        for a in agents:
            txs_f = txs.filter(
                responsible_assistant=a,
                created_at__gte=timezone.now() - timezone.timedelta(
                    days=n_days
                )
            )

            total = 0

            for tx in txs_f:
                if tx.transaction_source in [
                    LLMTransactionSourcesTypesNames.EXTERNAL_API_EXECUTION
                ]:
                    total += 1

            result[a.name] = total

        return result

    @staticmethod
    def calculate_total_api_calls_per_assistants(
        agents,
        txs,
        n_days
    ):

        result = {}

        for a in agents:
            txs_f = txs.filter(
                responsible_assistant=a,
                created_at__gte=timezone.now() - timezone.timedelta(
                    days=n_days
                )
            )

            total = 0

            for tx in txs_f:
                if tx.transaction_source in [
                    LLMTransactionSourcesTypesNames.INTERNAL_API_EXECUTION,
                    LLMTransactionSourcesTypesNames.EXTERNAL_API_EXECUTION
                ]:
                    total += 1

            result[a.name] = total

        return result
