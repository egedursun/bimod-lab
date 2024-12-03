#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auxiliary_tokens_manager.py
#  Last Modified: 2024-10-09 21:53:07
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 22:38:47
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


class AuxiliaryTokensManager:

    @staticmethod
    def calculate_tokens_per_organizations(
        orgs,
        txs,
        n_days
    ):

        org_tokens = {}

        for org in orgs:
            txs_f = txs.filter(
                organization=org,
                created_at__gte=timezone.now() - timezone.timedelta(
                    days=n_days
                )
            )

            total = 0

            for tx in txs_f:
                total += tx.number_of_tokens if tx.number_of_tokens else 0

            if total > 0:
                org_tokens[org.name] = total

        return org_tokens

    @staticmethod
    def calculate_tokens_per_assistants(
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
                total += tx.number_of_tokens if tx.number_of_tokens else 0

            if total > 0:
                result[a.name] = total

        return result

    @staticmethod
    def calculate_tokens_per_users(
        org_users,
        txs,
        n_days
    ):

        result = {}

        for usr in org_users:
            txs_f = txs.filter(
                responsible_user=usr,
                created_at__gte=timezone.now() - timezone.timedelta(
                    days=n_days
                )
            )

            total = 0

            for tx in txs_f:
                total += tx.number_of_tokens if tx.number_of_tokens else 0

            if total > 0:
                result[usr.username] = total

        return result

    @staticmethod
    def calculate_tokens_per_sources(
        txs,
        n_days
    ):

        result = {
            "main": {},
            "tool": {}
        }

        for src in LLMTransactionSourcesTypesNames.as_list():

            txs_f = txs.filter(
                transaction_source=src,
                created_at__gte=timezone.now() - timezone.timedelta(
                    days=n_days
                )
            )

            total_tokens = 0

            for tx in txs_f:
                total_tokens += tx.number_of_tokens if tx.number_of_tokens else 0

            if total_tokens > 0:

                if (
                    src == LLMTransactionSourcesTypesNames.APP or
                    src == LLMTransactionSourcesTypesNames.API
                ):
                    result["main"][src] = total_tokens

                else:
                    result["tool"][src] = total_tokens

        return result
