#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: calculate_costs_manager.py
#  Last Modified: 2024-10-09 21:39:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 21:39:09
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


class AuxiliaryCalculateMLManager:

    @staticmethod
    def calculate_total_ml_predictions_per_assistants(agents, txs, n_days):
        result = {}
        for a in agents:
            txs = txs.filter(
                responsible_assistant=a,
                created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            total = 0
            for tx in txs:
                if tx.transaction_source in [LLMTransactionSourcesTypesNames.ML_MODEL_PREDICTION]:
                    total += 1
            result[a.name] = total
        return result
