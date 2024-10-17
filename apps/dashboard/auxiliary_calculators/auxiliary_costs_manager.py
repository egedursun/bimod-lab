#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auxiliary_costs_manager.py
#  Last Modified: 2024-10-09 21:53:12
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 21:53:13
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

from apps.llm_transaction.models import OrganizationBalanceSnapshot
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames


class AuxiliaryCostsManager:

    @staticmethod
    def calculate_costs_per_organizations(orgs, txs, n_days):
        result = {}
        for org in orgs:
            txs = txs.filter(
                organization=org, created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            total = 0
            for tx in txs:
                total += float(tx.total_billable_cost)
            if total > 0:
                result[org.name] = total
        return result

    @staticmethod
    def calculate_cost_per_assistants(agents, txs, n_days):
        result = {}
        for a in agents:
            txs = txs.filter(
                responsible_assistant=a, created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            total = 0
            for tx in txs:
                total += float(tx.total_billable_cost)
            if total > 0:
                result[a.name] = total
        return result

    @staticmethod
    def calculate_cost_per_users(org_users, txs, n_days):
        result = {}
        for usr in org_users:
            txs = txs.filter(
                responsible_user=usr, created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            total = 0
            for tx in txs:
                total += float(tx.total_billable_cost)
            if total > 0:
                result[usr.username] = total
        return result

    @staticmethod
    def calculate_cost_per_sources(txs, n_days):
        result = {"main": {}, "tool": {}}
        for src in LLMTransactionSourcesTypesNames.as_list():
            txs = txs.filter(
                transaction_source=src, created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            total = 0
            for tx in txs:
                total += float(tx.total_billable_cost)
            if total > 0:
                if src == LLMTransactionSourcesTypesNames.APP or src == LLMTransactionSourcesTypesNames.API:
                    result["main"][src] = total
                else:
                    result["tool"][src] = total
        return result

    @staticmethod
    def calculate_balance_snapshot_per_organizations(orgs, n_days):
        result = {}
        for org in orgs:
            balance_sss = OrganizationBalanceSnapshot.objects.filter(
                organization=org, created_at__gte=timezone.now() - timezone.timedelta(days=n_days)
            )
            snapshots = []
            for ss in balance_sss:
                snapshots.append({"balance": float(ss.balance), "created_at": ss.created_at})
            result[org.name] = snapshots
        return result
