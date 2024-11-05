#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auxiliary_media_manager.py
#  Last Modified: 2024-10-09 21:52:18
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 22:38:22
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


class AuxiliaryMediaManager:

    @staticmethod
    def calculate_total_file_downloads_per_assistants(agents, txs, n_days):
        result = {}
        for a in agents:
            txs_f = txs.filter(
                responsible_assistant=a, created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            total = 0
            for tx in txs_f:
                if tx.transaction_source in [LLMTransactionSourcesTypesNames.DOWNLOAD_FILE]:
                    total += 1
            result[a.name] = total
        return result

    @staticmethod
    def calculate_total_multimedia_generations_per_assistants(agents, txs, n_days):
        result = {}
        for a in agents:
            txs_f = txs.filter(
                responsible_assistant=a, created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            total = 0
            for tx in txs_f:
                if tx.transaction_source in [LLMTransactionSourcesTypesNames.GENERATION,
                                             LLMTransactionSourcesTypesNames.GENERATE_IMAGE,
                                             LLMTransactionSourcesTypesNames.MODIFY_IMAGE,
                                             LLMTransactionSourcesTypesNames.VARIATE_IMAGE]:
                    total += 1
            result[a.name] = total
        return result
