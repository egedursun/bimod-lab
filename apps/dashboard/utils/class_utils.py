#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: class_utils.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from django.utils import timezone

from apps.assistants.models import Assistant
from apps.dashboard.auxiliary_calculators.auxiliary_analyze_code_manager import AuxiliaryAnalyzeCodeManager
from apps.dashboard.auxiliary_calculators.auxiliary_api_calls_manager import AuxiliaryAPICallsManager
from apps.dashboard.auxiliary_calculators.auxiliary_calculate_ml_manager import AuxiliaryCalculateMLManager
from apps.dashboard.auxiliary_calculators.auxiliary_costs_manager import AuxiliaryCostsManager
from apps.dashboard.auxiliary_calculators.auxiliary_function_calls_manager import AuxiliaryFunctionCallsManager
from apps.dashboard.auxiliary_calculators.auxiliary_information_feeds_manager import AuxiliaryInformationFeedsManager
from apps.dashboard.auxiliary_calculators.auxiliary_interactions_manager import AuxiliaryInteractionsManager
from apps.dashboard.auxiliary_calculators.auxiliary_media_manager import AuxiliaryMediaManager
from apps.dashboard.auxiliary_calculators.auxiliary_memory_manager import AuxiliaryMemoryManager
from apps.dashboard.auxiliary_calculators.auxiliary_organization_users_manager import AuxiliaryOrganizationUsersManager
from apps.dashboard.auxiliary_calculators.auxiliary_script_calls_manager import AuxiliaryScriptCallsManager
from apps.dashboard.auxiliary_calculators.auxiliary_tasks_manager import AuxiliaryTasksManager
from apps.dashboard.auxiliary_calculators.auxiliary_tokens_manager import AuxiliaryTokensManager
from apps.dashboard.auxiliary_calculators.auxiliary_vector_store_manager import AuxiliaryVectorStoreManager
from apps.export_assistants.models import ExportAssistantAPI
from apps.llm_transaction.models import LLMTransaction
from apps.mm_scheduled_jobs.models import ScheduledJob
from apps.mm_triggered_jobs.models import TriggeredJob
from apps.organization.models import Organization


logger = logging.getLogger(__name__)


class TransactionStatisticsManager:
    def __init__(self, user, last_days=30):
        self.user = user
        self.last_days = last_days
        self.organizations = Organization.objects.filter(users__in=[self.user])
        self.organization_users = []
        for organization in self.organizations:
            self.organization_users += organization.users.all()
        self.organization_users = list(set(self.organization_users))
        self.assistants = Assistant.objects.filter(organization__in=self.organizations)
        self.transactions = LLMTransaction.objects.filter(
            responsible_assistant__in=self.assistants,
            created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
        )
        self.export_assistants = ExportAssistantAPI.objects.filter(assistant__in=self.assistants)
        self.scheduled_jobs = ScheduledJob.objects.filter(assistant__in=self.assistants)
        self.triggered_jobs = TriggeredJob.objects.filter(trigger_assistant__in=self.assistants)
        self.statistics = {
            "costs": {},
            "tokens": {},
            "communication": {},
            "exports": {},
            "sql": {},
            "file_system": {},
            "browsing": {},
            "knowledge_base": {},
            "functions": {},
            "apis": {},
            "scripts": {},
            "crons": {},
            "triggers": {},
            "users": {},
            "ml": {},
        }
        self._calculate()
        logger.info(f"Transaction statistics calculated for User: {self.user.id}")

    def _calculate(self):
        self._calculate__costs()
        self._calculate__balance_snapshots()
        self._calculate__tokens()
        self._calculate__interactions()
        self._calculate__sql()
        self._calculate__information_feeds()
        self._calculate__files()
        self._calculate__vector_stores()
        self._calculate__modalities()
        self._calculate__tasks()
        self._calculate__users()
        logger.info(f"Transaction statistics calculated for User: {self.user.id}")

    def _calculate__users(self):
        self.total_users_per_organizations()
        self.latest_registered_users_per_organizations()

    def _calculate__tasks(self):
        self.total_scheduled_task_executions_per_assistants()
        self.total_triggered_task_executions_per_assistants()

    def _calculate__modalities(self):
        self.total_internal_function_calls_per_assistants()
        self.total_external_function_calls_per_assistants()
        self.total_function_calls_per_assistants()
        self.total_internal_third_party_api_calls_per_assistants()
        self.total_external_third_party_api_calls_per_assistants()
        self.total_third_party_api_calls_per_assistants()
        self.total_internal_script_executions_per_assistants()
        self.total_external_script_executions_per_assistants()
        self.total_script_executions_per_assistants()

    def _calculate__vector_stores(self):
        self.total_knowledge_base_searches_per_assistants()
        self.total_memory_saves_per_assistants()
        self.total_memory_retrievals_per_assistants()

    def _calculate__files(self):
        self.total_documents_interpretations_per_assistants()
        self.total_image_interpretations_per_assistants()
        self.total_code_interpretations_per_assistants()
        self.total_file_downloads_per_assistants()
        self.total_multimedia_generations_per_assistants()

    def _calculate__information_feeds(self):
        self.total_ssh_file_system_access_per_assistants()
        self.total_web_queries_per_assistants()
        self.total_ml_predictions_per_assistants()

    def _calculate__sql(self):
        self.total_sql_read_queries_per_assistants()
        self.total_sql_write_queries_per_assistants()
        self.total_sql_queries_per_assistants()

    def _calculate__interactions(self):
        self.total_chats_per_organizations()
        self.total_messages_per_organizations()
        self.total_request_count_per_exported_assistants()

    def _calculate__tokens(self):
        self.tokens_per_organizations()
        self.tokens_per_assistants()
        self.tokens_per_users()
        self.tokens_per_sources()

    def _calculate__balance_snapshots(self):
        self.balance_snapshot_per_organizations()

    def _calculate__costs(self):
        self.costs_per_organizations()
        self.costs_per_assistants()
        self.costs_per_users()
        self.costs_per_sources()

    def costs_per_organizations(self):
        organization_costs = self._calculate_costs_per_organizations()
        self.statistics["costs"]['costs_per_organizations'] = organization_costs

    def costs_per_assistants(self):
        assistant_costs = self._calculate_cost_per_assistants()
        self.statistics["costs"]['costs_per_assistants'] = assistant_costs

    def costs_per_users(self):
        user_costs = self._calculate_cost_per_users()
        self.statistics["costs"]['costs_per_users'] = user_costs

    def costs_per_sources(self):
        source_costs = self._calculate_cost_per_sources()
        self.statistics["costs"]['costs_per_sources'] = source_costs

    def balance_snapshot_per_organizations(self):
        organization_balance_snapshots = self._calculate_balance_snapshot_per_organizations()
        self.statistics["costs"]['balance_snapshot_per_organizations'] = organization_balance_snapshots

    def tokens_per_organizations(self):
        organization_tokens = self._calculate_tokens_per_organizations()
        self.statistics["tokens"]['tokens_per_organizations'] = organization_tokens

    def tokens_per_assistants(self):
        assistant_tokens = self._calculate_tokens_per_assistants()
        self.statistics["tokens"]['tokens_per_assistants'] = assistant_tokens

    def tokens_per_users(self):
        user_tokens = self._calculate_tokens_per_users()
        self.statistics["tokens"]['tokens_per_users'] = user_tokens

    def tokens_per_sources(self):
        source_tokens = self._calculate_tokens_per_sources()
        self.statistics["tokens"]['tokens_per_sources'] = source_tokens

    def total_chats_per_organizations(self):
        assistant_chats = self._calculate_total_chats_per_organizations()
        self.statistics["communication"]['total_chats_per_organizations'] = assistant_chats

    def total_messages_per_organizations(self):
        assistant_messages = self._calculate_total_messages_per_organizations()
        self.statistics["communication"]['total_messages_per_organizations'] = assistant_messages

    def total_request_count_per_exported_assistants(self):
        assistant_requests = self._calculate_total_request_count_per_exported_assistants()
        self.statistics["exports"]['total_request_count_per_exported_assistants'] = assistant_requests

    def total_sql_read_queries_per_assistants(self):
        assistant_sql_read_queries = self._calculate_total_sql_read_queries_per_assistants()
        self.statistics["sql"]['total_sql_read_queries_per_assistants'] = assistant_sql_read_queries

    def total_sql_write_queries_per_assistants(self):
        assistant_sql_write_queries = self._calculate_total_sql_write_queries_per_assistants()
        self.statistics["sql"]['total_sql_write_queries_per_assistants'] = assistant_sql_write_queries

    def total_sql_queries_per_assistants(self):
        assistant_sql_queries = self._calculate_total_sql_queries_per_assistants()
        self.statistics["sql"]['total_sql_queries_per_assistants'] = assistant_sql_queries

    def total_ssh_file_system_access_per_assistants(self):
        assistant_ssh_file_system_access = self._calculate_total_ssh_file_system_access_per_assistants()
        self.statistics["file_system"][
            'total_ssh_file_system_access_per_assistants'] = assistant_ssh_file_system_access

    def total_web_queries_per_assistants(self):
        assistant_web_queries = self._calculate_total_web_queries_per_assistants()
        self.statistics["browsing"]['total_web_queries_per_assistants'] = assistant_web_queries

    def total_documents_interpretations_per_assistants(self):
        assistant_documents_uploaded = self._calculate_total_document_interpretations_per_assistants()
        self.statistics["knowledge_base"][
            'total_documents_interpretations_per_assistants'] = assistant_documents_uploaded

    def total_image_interpretations_per_assistants(self):
        assistant_images_interpreted = self._calculate_total_image_interpretations_per_assistants()
        self.statistics["knowledge_base"]['total_image_interpretations_per_assistants'] = assistant_images_interpreted

    def total_code_interpretations_per_assistants(self):
        assistant_code_interpreted = self._calculate_total_code_interpretations_per_assistants()
        self.statistics["knowledge_base"]['total_code_interpretations_per_assistants'] = assistant_code_interpreted

    def total_file_downloads_per_assistants(self):
        assistant_file_downloads = self._calculate_total_file_downloads_per_assistants()
        self.statistics["knowledge_base"]['total_file_downloads_per_assistants'] = assistant_file_downloads

    def total_multimedia_generations_per_assistants(self):
        assistant_multimedia_generations = self._calculate_total_multimedia_generations_per_assistants()
        self.statistics["knowledge_base"][
            'total_multimedia_generations_per_assistants'] = assistant_multimedia_generations

    def total_knowledge_base_searches_per_assistants(self):
        assistant_knowledge_base_searches = self._calculate_total_knowledge_base_searches_per_assistants()
        self.statistics["knowledge_base"][
            'total_knowledge_base_searches_per_assistants'] = assistant_knowledge_base_searches

    def total_memory_saves_per_assistants(self):
        assistant_memory_saves = self._calculate_total_memory_saves_per_assistants()
        self.statistics["knowledge_base"]['total_memory_saves_per_assistants'] = assistant_memory_saves

    def total_memory_retrievals_per_assistants(self):
        assistant_memory_retrievals = self._calculate_total_memory_retrievals_per_assistants()
        self.statistics["knowledge_base"]['total_memory_retrievals_per_assistants'] = assistant_memory_retrievals

    def total_internal_function_calls_per_assistants(self):
        assistant_internal_function_calls = self._calculate_total_internal_function_calls_per_assistants()
        self.statistics["functions"][
            'total_internal_function_calls_per_assistants'] = assistant_internal_function_calls

    def total_external_function_calls_per_assistants(self):
        assistant_external_function_calls = self._calculate_total_external_function_calls_per_assistants()
        self.statistics["functions"][
            'total_external_function_calls_per_assistants'] = assistant_external_function_calls

    def total_function_calls_per_assistants(self):
        assistant_function_calls = self._calculate_total_function_calls_per_assistants()
        self.statistics["functions"]['total_function_calls_per_assistants'] = assistant_function_calls

    def total_internal_third_party_api_calls_per_assistants(self):
        assistant_internal_third_party_api_calls = self._calculate_total_internal_api_calls_per_assistants()
        self.statistics["apis"][
            'total_internal_third_party_api_calls_per_assistants'] = assistant_internal_third_party_api_calls

    def total_external_third_party_api_calls_per_assistants(self):
        assistant_external_third_party_api_calls = self._calculate_total_external_api_calls_per_assistants()
        self.statistics["apis"][
            'total_external_third_party_api_calls_per_assistants'] = assistant_external_third_party_api_calls

    def total_third_party_api_calls_per_assistants(self):
        assistant_third_party_api_calls = self._calculate_total_api_calls_per_assistants()
        self.statistics["apis"]['total_third_party_api_calls_per_assistants'] = assistant_third_party_api_calls

    def total_internal_script_executions_per_assistants(self):
        assistant_script_executions = self._calculate_total_internal_script_calls_per_assistants()
        self.statistics["scripts"]['total_internal_script_executions_per_assistants'] = assistant_script_executions

    def total_external_script_executions_per_assistants(self):
        assistant_script_executions = self._calculate_total_external_script_calls_per_assistants()
        self.statistics["scripts"]['total_external_script_executions_per_assistants'] = assistant_script_executions

    def total_script_executions_per_assistants(self):
        assistant_script_executions = self._calculate_total_script_calls_per_assistants()
        self.statistics["scripts"]['total_script_executions_per_assistants'] = assistant_script_executions

    def total_scheduled_task_executions_per_assistants(self):
        assistant_scheduled_task_executions = self._calculate_total_scheduled_jobs_per_assistants()
        self.statistics["crons"][
            'total_scheduled_task_executions_per_assistants'] = assistant_scheduled_task_executions

    def total_triggered_task_executions_per_assistants(self):
        assistant_triggered_task_executions = self._calculate_total_triggered_jobs_per_assistants()
        self.statistics["triggers"][
            'total_triggered_task_executions_per_assistants'] = assistant_triggered_task_executions

    def total_users_per_organizations(self):
        organization_users = self._calculate_total_users_per_organizations()
        self.statistics["users"]['total_users_per_organizations'] = organization_users

    def latest_registered_users_per_organizations(self):
        organization_users = self._calculate_latest_registered_users_per_organizations()
        self.statistics["users"]['latest_registered_users_per_organizations'] = organization_users

    def total_ml_predictions_per_assistants(self):
        assistant_ml_predictions = self._calculate_total_ml_predictions_per_assistants()
        self.statistics["ml"]['total_ml_predictions_per_assistants'] = assistant_ml_predictions

    def _calculate_costs_per_organizations(self):
        o = AuxiliaryCostsManager.calculate_costs_per_organizations(
            orgs=self.organizations, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_cost_per_assistants(self):
        o = AuxiliaryCostsManager.calculate_cost_per_assistants(
            agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_cost_per_users(self):
        o = AuxiliaryCostsManager.calculate_cost_per_users(
            org_users=self.organization_users, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_cost_per_sources(self):
        o = AuxiliaryCostsManager.calculate_cost_per_sources(txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_balance_snapshot_per_organizations(self):
        o = AuxiliaryCostsManager.calculate_balance_snapshot_per_organizations(
            orgs=self.organizations, n_days=self.last_days)
        return o

    def _calculate_tokens_per_organizations(self):
        o = AuxiliaryTokensManager.calculate_tokens_per_organizations(
            orgs=self.organizations, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_tokens_per_assistants(self):
        o = AuxiliaryTokensManager.calculate_tokens_per_assistants(
            agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_tokens_per_users(self):
        o = AuxiliaryTokensManager.calculate_tokens_per_users(
            org_users=self.organization_users, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_tokens_per_sources(self):
        o = AuxiliaryTokensManager.calculate_tokens_per_sources(
            txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_chats_per_organizations(self):
        o = AuxiliaryInteractionsManager.calculate_total_chats_per_organizations(
            orgs=self.organizations, n_days=self.last_days)
        return o

    def _calculate_total_messages_per_organizations(self):
        o = AuxiliaryInteractionsManager.calculate_total_messages_per_organizations(
            orgs=self.organizations, n_days=self.last_days)
        return o

    def _calculate_total_request_count_per_exported_assistants(self):
        o = AuxiliaryInteractionsManager.calculate_total_request_count_per_exported_assistants(
            exp_agents=self.export_assistants, n_days=self.last_days)
        return o

    def _calculate_total_sql_read_queries_per_assistants(self):
        o = AuxiliaryInformationFeedsManager.calculate_total_sql_read_queries_per_assistants(
            agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_sql_write_queries_per_assistants(self):
        o = AuxiliaryInformationFeedsManager.calculate_total_sql_write_queries_per_assistants(
                agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_sql_queries_per_assistants(self):
        o = AuxiliaryInformationFeedsManager.calculate_total_sql_queries_per_assistants(
            agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_ssh_file_system_access_per_assistants(self):
        o = AuxiliaryInformationFeedsManager.calculate_total_ssh_file_system_access_per_assistants(
                agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_web_queries_per_assistants(self):
        o = AuxiliaryInformationFeedsManager.calculate_total_web_queries_per_assistants(
            agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_document_interpretations_per_assistants(self):
        o = AuxiliaryAnalyzeCodeManager.calculate_total_document_interpretations_per_assistants(
                agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_image_interpretations_per_assistants(self):
        o = AuxiliaryAnalyzeCodeManager.calculate_total_image_interpretations_per_assistants(
                agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_code_interpretations_per_assistants(self):
        o = AuxiliaryAnalyzeCodeManager.calculate_total_code_interpretations_per_assistants(
            agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_file_downloads_per_assistants(self):
        o = AuxiliaryMediaManager.calculate_total_file_downloads_per_assistants(
            agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_multimedia_generations_per_assistants(self):
        o = AuxiliaryMediaManager.calculate_total_multimedia_generations_per_assistants(
            agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_knowledge_base_searches_per_assistants(self):
        o = AuxiliaryVectorStoreManager.calculate_total_knowledge_base_searches_per_assistants(
                agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_memory_saves_per_assistants(self):
        o = AuxiliaryMemoryManager.calculate_total_memory_saves_per_assistants(
            agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_memory_retrievals_per_assistants(self):
        o = AuxiliaryMemoryManager.calculate_total_memory_retrievals_per_assistants(
            agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_internal_function_calls_per_assistants(self):
        o = AuxiliaryFunctionCallsManager.calculate_total_internal_function_calls_per_assistants(
                agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_external_function_calls_per_assistants(self):
        o = AuxiliaryFunctionCallsManager.calculate_total_external_function_calls_per_assistants(
                agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_function_calls_per_assistants(self):
        o = AuxiliaryFunctionCallsManager.calculate_total_function_calls_per_assistants(
            agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_internal_api_calls_per_assistants(self):
        o = AuxiliaryAPICallsManager.calculate_total_internal_api_calls_per_assistants(
                agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_external_api_calls_per_assistants(self):
        o = AuxiliaryAPICallsManager.calculate_total_external_api_calls_per_assistants(
                agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_api_calls_per_assistants(self):
        o = AuxiliaryAPICallsManager.calculate_total_api_calls_per_assistants(
            agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_internal_script_calls_per_assistants(self):
        o = AuxiliaryScriptCallsManager.calculate_total_internal_script_calls_per_assistants(
            agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_external_script_calls_per_assistants(self):
        o = AuxiliaryScriptCallsManager.calculate_total_external_script_calls_per_assistants(
            agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_script_calls_per_assistants(self):
        o = AuxiliaryScriptCallsManager.calculate_total_script_calls_per_assistants(
            agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o

    def _calculate_total_scheduled_jobs_per_assistants(self):
        o = AuxiliaryTasksManager.calculate_total_scheduled_jobs_per_assistants(
            agents=self.assistants, sched_jobs=self.scheduled_jobs, n_days=self.last_days)
        return o

    def _calculate_total_triggered_jobs_per_assistants(self):
        o = AuxiliaryTasksManager.calculate_total_triggered_jobs_per_assistants(
            agents=self.assistants, trg_jobs=self.triggered_jobs, n_days=self.last_days)
        return o

    def _calculate_total_users_per_organizations(self):
        o = AuxiliaryOrganizationUsersManager.calculate_total_users_per_organizations(
            orgs=self.organizations)
        return o

    def _calculate_latest_registered_users_per_organizations(self):
        o = AuxiliaryOrganizationUsersManager.calculate_latest_registered_users_per_organizations(
            orgs=self.organizations, n_days=self.last_days)
        return o

    def _calculate_total_ml_predictions_per_assistants(self):
        o = AuxiliaryCalculateMLManager.calculate_total_ml_predictions_per_assistants(
            agents=self.assistants, txs=self.transactions, n_days=self.last_days)
        return o
