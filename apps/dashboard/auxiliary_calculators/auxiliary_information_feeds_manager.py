#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auxiliary_information_feeds_manager.py
#  Last Modified: 2024-10-09 21:52:45
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 21:52:46
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


class AuxiliaryInformationFeedsManager:

    @staticmethod
    def calculate_total_sql_read_queries_per_assistants(agents, txs, n_days):
        result = {}
        for a in agents:
            txs_f = txs.filter(
                responsible_assistant=a, created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            total = 0
            for tx in txs_f:
                if tx.transaction_source == LLMTransactionSourcesTypesNames.SQL_READ:
                    total += 1
            result[a.name] = total
        return result

    @staticmethod
    def calculate_total_sql_write_queries_per_assistants(agents, txs, n_days):
        result = {}
        for a in agents:
            txs_f = txs.filter(
                responsible_assistant=a, created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            total = 0
            for tx in txs_f:
                if tx.transaction_source == LLMTransactionSourcesTypesNames.SQL_WRITE:
                    total += 1
            result[a.name] = total
        return result

    @staticmethod
    def calculate_total_sql_queries_per_assistants(agents, txs, n_days):
        result = {}
        for a in agents:
            txs_f = txs.filter(
                responsible_assistant=a, created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            total = 0
            for tx in txs_f:
                if tx.transaction_source in [LLMTransactionSourcesTypesNames.SQL_READ, LLMTransactionSourcesTypesNames.SQL_WRITE]:
                    total += 1
            result[a.name] = total
        return result

    @staticmethod
    def calculate_total_ssh_file_system_access_per_assistants(agents, txs, n_days):
        result = {}
        for a in agents:
            txs_f = txs.filter(
                responsible_assistant=a,
                created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            total = 0
            for tx in txs_f:
                if tx.transaction_source in [LLMTransactionSourcesTypesNames.FILE_SYSTEM_COMMANDS]:
                    total += 1
            result[a.name] = total
        return result

    @staticmethod
    def calculate_total_web_queries_per_assistants(agents, txs, n_days):
        result = {}
        for a in agents:
            txs_f = txs.filter(
                responsible_assistant=a, created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            total = 0
            for tx in txs_f:
                if tx.transaction_source in [LLMTransactionSourcesTypesNames.BROWSING]:
                    total += 1
            result[a.name] = total
        return result
