from django.utils import timezone

from apps.assistants.models import Assistant
from apps.export_assistants.models import RequestLog, ExportAssistantAPI
from apps.llm_transaction.models import LLMTransaction, OrganizationBalanceSnapshot
from apps.mm_scheduled_jobs.models import ScheduledJobInstance, ScheduledJob
from apps.mm_triggered_jobs.models import TriggeredJob, TriggeredJobInstance
from apps.multimodal_chat.models import ChatCreationLog, ChatMessageCreationLog
from apps.organization.models import Organization


class TransactionSourcesNames:
    APP = "app"
    API = "api"
    GENERATION = "generation"
    SQL_READ = "sql-read"
    SQL_WRITE = "sql-write"
    STORE_MEMORY = "store-memory"
    INTERPRET_CODE = "interpret-code"
    DOWNLOAD_FILE = "download-file"
    FILE_SYSTEM_COMMANDS = "file-system-commands"
    KNOWLEDGE_BASE_SEARCH = "knowledge-base-search"
    RETRIEVE_MEMORY = "retrieve-memory"
    CODE_REPOSITORY_SEARCH = "code-repository-search"
    ML_MODEL_PREDICTION = "ml-model-prediction"
    BROWSING = "browsing"
    INTERNAL_FUNCTION_EXECUTION = "internal-function-execution"
    EXTERNAL_FUNCTION_EXECUTION = "external-function-execution"
    INTERNAL_API_EXECUTION = "internal-api-execution"
    EXTERNAL_API_EXECUTION = "external-api-execution"
    INTERNAL_SCRIPT_RETRIEVAL = "internal-script-retrieval"
    EXTERNAL_SCRIPT_RETRIEVAL = "external-script-retrieval"
    INTERPRET_FILE = "interpret-file"
    INTERPRET_IMAGE = "interpret-image"
    SCHEDULED_JOB_EXECUTION = "scheduled-job-execution"
    TRIGGER_JOB_EXECUTION = "trigger-job-execution"
    GENERATE_IMAGE = "generate-image"
    MODIFY_IMAGE = "modify-image"
    VARIATE_IMAGE = "variate-image"

    @staticmethod
    def as_list():
        return [
            TransactionSourcesNames.APP,
            TransactionSourcesNames.API,
            TransactionSourcesNames.GENERATION,
            TransactionSourcesNames.SQL_READ,
            TransactionSourcesNames.SQL_WRITE,
            TransactionSourcesNames.STORE_MEMORY,
            TransactionSourcesNames.INTERPRET_CODE,
            TransactionSourcesNames.DOWNLOAD_FILE,
            TransactionSourcesNames.FILE_SYSTEM_COMMANDS,
            TransactionSourcesNames.KNOWLEDGE_BASE_SEARCH,
            TransactionSourcesNames.RETRIEVE_MEMORY,
            TransactionSourcesNames.CODE_REPOSITORY_SEARCH,
            TransactionSourcesNames.ML_MODEL_PREDICTION,
            TransactionSourcesNames.BROWSING,
            TransactionSourcesNames.INTERNAL_FUNCTION_EXECUTION,
            TransactionSourcesNames.EXTERNAL_FUNCTION_EXECUTION,
            TransactionSourcesNames.INTERNAL_API_EXECUTION,
            TransactionSourcesNames.EXTERNAL_API_EXECUTION,
            TransactionSourcesNames.INTERNAL_SCRIPT_RETRIEVAL,
            TransactionSourcesNames.EXTERNAL_SCRIPT_RETRIEVAL,
            TransactionSourcesNames.INTERPRET_FILE,
            TransactionSourcesNames.INTERPRET_IMAGE,
            TransactionSourcesNames.SCHEDULED_JOB_EXECUTION,
            TransactionSourcesNames.TRIGGER_JOB_EXECUTION,
            TransactionSourcesNames.GENERATE_IMAGE,
            TransactionSourcesNames.MODIFY_IMAGE,
            TransactionSourcesNames.VARIATE_IMAGE,
        ]


class DashboardStatisticsCalculator:
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
            "costs": {}, "tokens": {}, "communication": {}, "exports": {}, "sql": {}, "file_system": {},
            "browsing": {}, "knowledge_base": {}, "functions": {}, "apis": {}, "scripts": {}, "crons": {},
            "triggers": {}, "users": {}, "ml": {},
        }
        self._calculate()

    def _calculate(self):
        # COSTS
        self.costs_per_organizations()
        self.costs_per_assistants()
        self.costs_per_users()
        self.costs_per_sources()
        # BALANCE SNAPSHOTS
        self.balance_snapshot_per_organizations()
        # TOKENS
        self.tokens_per_organizations()
        self.tokens_per_assistants()
        self.tokens_per_users()
        self.tokens_per_sources()
        # ASSISTANT COMMUNICATION
        self.total_chats_per_organizations()
        self.total_messages_per_organizations()
        self.total_request_count_per_exported_assistants()
        # SQL DATABASE USAGE
        self.total_sql_read_queries_per_assistants()
        self.total_sql_write_queries_per_assistants()
        self.total_sql_queries_per_assistants()
        # FILE SYSTEMS
        self.total_ssh_file_system_access_per_assistants()
        # BROWSING
        self.total_web_queries_per_assistants()
        # ML MODEL PREDICTIONS
        self.total_ml_predictions_per_assistants()
        #  MULTIMEDIA MANAGEMENT
        self.total_documents_interpretations_per_assistants()
        self.total_image_interpretations_per_assistants()
        self.total_code_interpretations_per_assistants()
        self.total_file_downloads_per_assistants()
        self.total_multimedia_generations_per_assistants()
        # KNOWLEDGE BASE SEARCHES
        self.total_knowledge_base_searches_per_assistants()
        # MEMORY MANAGEMENT
        self.total_memory_saves_per_assistants()
        self.total_memory_retrievals_per_assistants()
        # FUNCTION EXECUTIONS
        self.total_internal_function_calls_per_assistants()
        self.total_external_function_calls_per_assistants()
        self.total_function_calls_per_assistants()
        # API EXECUTIONS
        self.total_internal_third_party_api_calls_per_assistants()
        self.total_external_third_party_api_calls_per_assistants()
        self.total_third_party_api_calls_per_assistants()
        # SCRIPT EXECUTIONS
        self.total_internal_script_executions_per_assistants()
        self.total_external_script_executions_per_assistants()
        self.total_script_executions_per_assistants()
        # CRON JOBS AND TRIGGERS
        self.total_scheduled_task_executions_per_assistants()
        self.total_triggered_task_executions_per_assistants()
        # USERS
        self.total_users_per_organizations()
        self.latest_registered_users_per_organizations()

    ########################################
    # COSTS
    ########################################

    def costs_per_organizations(self):
        # Calculate the costs for each organization for the last self.last_days days
        # Return the costs as a dictionary
        organization_costs = {}
        for organization in self.organizations:
            transactions = self.transactions.filter(
                organization=organization,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_cost = 0
            for transaction in transactions:
                total_cost += float(transaction.total_billable_cost)
            if total_cost > 0:
                organization_costs[organization.name] = total_cost
        self.statistics["costs"]['costs_per_organizations'] = organization_costs

    def costs_per_assistants(self):
        # Calculate the costs for each assistant for the last self.last_days days
        # Return the costs as a dictionary
        assistant_costs = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_cost = 0
            for transaction in transactions:
                total_cost += float(transaction.total_billable_cost)
            if total_cost > 0:
                assistant_costs[assistant.name] = total_cost
        self.statistics["costs"]['costs_per_assistants'] = assistant_costs

    def costs_per_users(self):
        # Calculate the costs for each user for the last self.last_days days
        # Return the costs as a dictionary
        user_costs = {}
        for user in self.organization_users:
            transactions = self.transactions.filter(
                responsible_user=user,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_cost = 0
            for transaction in transactions:
                total_cost += float(transaction.total_billable_cost)
            if total_cost > 0:
                user_costs[user.profile.username] = total_cost
        self.statistics["costs"]['costs_per_users'] = user_costs

    def costs_per_sources(self):
        # Calculate the costs for each source for the last self.last_days days
        # Return the costs as a dictionary
        source_costs = {"main": {}, "tool": {}}
        for source in TransactionSourcesNames.as_list():
            transactions = self.transactions.filter(
                transaction_source=source,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_cost = 0
            for transaction in transactions:
                total_cost += float(transaction.total_billable_cost)
            if total_cost > 0:
                if source == TransactionSourcesNames.APP or source == TransactionSourcesNames.API:
                    source_costs["main"][source] = total_cost
                else:
                    source_costs["tool"][source] = total_cost
        self.statistics["costs"]['costs_per_sources'] = source_costs

    def balance_snapshot_per_organizations(self):
        # Calculate the balance snapshot for each organization for the last self.last_days days
        # Return the balance snapshot as a dictionary
        organization_balance_snapshots = {}
        for organization in self.organizations:
            balance_snapshots = OrganizationBalanceSnapshot.objects.filter(
                organization=organization,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            ss = []
            for s in balance_snapshots:
                ss.append({"balance": float(s.balance), "created_at": s.created_at})
            organization_balance_snapshots[organization.name] = ss
        self.statistics["costs"]['balance_snapshot_per_organizations'] = organization_balance_snapshots

    ########################################
    # TOKENS
    ########################################

    def tokens_per_organizations(self):
        # Calculate the tokens for each organization for the last self.last_days days
        # Return the tokens as a dictionary
        organization_tokens = {}
        for organization in self.organizations:
            transactions = self.transactions.filter(
                organization=organization,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_tokens = 0
            for transaction in transactions:
                total_tokens += transaction.number_of_tokens if transaction.number_of_tokens else 0
            if total_tokens > 0:
                organization_tokens[organization.name] = total_tokens
        self.statistics["tokens"]['tokens_per_organizations'] = organization_tokens

    def tokens_per_assistants(self):
        # Calculate the tokens for each assistant for the last self.last_days days
        # Return the tokens as a dictionary
        assistant_tokens = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_tokens = 0
            for transaction in transactions:
                total_tokens += transaction.number_of_tokens if transaction.number_of_tokens else 0
            if total_tokens > 0:
                assistant_tokens[assistant.name] = total_tokens
        self.statistics["tokens"]['tokens_per_assistants'] = assistant_tokens

    def tokens_per_users(self):
        # Calculate the tokens for each user for the last self.last_days days
        # Return the tokens as a dictionary
        user_tokens = {}
        for user in self.organization_users:
            transactions = self.transactions.filter(
                responsible_user=user,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_tokens = 0
            for transaction in transactions:
                total_tokens += transaction.number_of_tokens if transaction.number_of_tokens else 0
            if total_tokens > 0:
                user_tokens[user.profile.username] = total_tokens
        self.statistics["tokens"]['tokens_per_users'] = user_tokens

    def tokens_per_sources(self):
        # Calculate the tokens for each source for the last self.last_days days
        # Return the tokens as a dictionary
        source_tokens = {"main": {}, "tool": {}}
        for source in TransactionSourcesNames.as_list():
            transactions = self.transactions.filter(
                transaction_source=source,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_tokens = 0
            for transaction in transactions:
                total_tokens += transaction.number_of_tokens if transaction.number_of_tokens else 0
            if total_tokens > 0:
                if source == TransactionSourcesNames.APP or source == TransactionSourcesNames.API:
                    source_tokens["main"][source] = total_tokens
                else:
                    source_tokens["tool"][source] = total_tokens
        self.statistics["tokens"]['tokens_per_sources'] = source_tokens

    ########################################
    # ASSISTANT COMMUNICATION
    ########################################

    def total_chats_per_organizations(self):
        # Calculate the total number of chats for each assistant for the last self.last_days days
        # Return the total chats as a dictionary
        assistant_chats = {}
        for organization in self.organizations:
            chats = ChatCreationLog.objects.filter(
                organization=organization,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_chats = chats.count()
            if total_chats > 0:
                assistant_chats[organization.name] = total_chats
        self.statistics["communication"]['total_chats_per_organizations'] = assistant_chats

    def total_messages_per_organizations(self):
        # Calculate the total number of messages for each assistant for the last self.last_days days
        # Return the total messages as a dictionary
        assistant_messages = {}
        for organization in self.organizations:
            messages = ChatMessageCreationLog.objects.filter(
                organization=organization,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_messages = messages.count()
            if total_messages > 0:
                assistant_messages[organization.name] = total_messages
        self.statistics["communication"]['total_messages_per_organizations'] = assistant_messages

    ########################################
    # EXPORTED ASSISTANTS
    ########################################

    def total_request_count_per_exported_assistants(self):
        # Calculate the total number of requests for each assistant for the last self.last_days days
        # Return the total requests as a dictionary
        assistant_requests = {}
        for export_assistant in self.export_assistants:
            requests = RequestLog.objects.filter(
                export_assistant=export_assistant,
                timestamp__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_requests = requests.count()
            if total_requests > 0:
                assistant_requests[export_assistant.assistant.name] = total_requests
        self.statistics["exports"]['total_request_count_per_exported_assistants'] = assistant_requests

    ########################################
    # SQL DATABASE USAGE
    ########################################

    def total_sql_read_queries_per_assistants(self):
        # Calculate the total number of SQL read queries for each assistant for the last self.last_days days
        # Return the total SQL read queries as a dictionary
        assistant_sql_read_queries = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_sql_read_queries = 0
            for transaction in transactions:
                if transaction.transaction_source == TransactionSourcesNames.SQL_READ:
                    total_sql_read_queries += 1
            assistant_sql_read_queries[assistant.name] = total_sql_read_queries
        self.statistics["sql"]['total_sql_read_queries_per_assistants'] = assistant_sql_read_queries

    def total_sql_write_queries_per_assistants(self):
        # Calculate the total number of SQL write queries for each assistant for the last self.last_days days
        # Return the total SQL write queries as a dictionary
        assistant_sql_write_queries = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_sql_write_queries = 0
            for transaction in transactions:
                if transaction.transaction_source == TransactionSourcesNames.SQL_WRITE:
                    total_sql_write_queries += 1
            assistant_sql_write_queries[assistant.name] = total_sql_write_queries
        self.statistics["sql"]['total_sql_write_queries_per_assistants'] = assistant_sql_write_queries

    def total_sql_queries_per_assistants(self):
        # Calculate the total number of SQL queries for each assistant for the last self.last_days days
        # Return the total SQL queries as a dictionary
        assistant_sql_queries = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_sql_queries = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.SQL_READ,
                                                      TransactionSourcesNames.SQL_WRITE]:
                    total_sql_queries += 1
            assistant_sql_queries[assistant.name] = total_sql_queries
        self.statistics["sql"]['total_sql_queries_per_assistants'] = assistant_sql_queries

    ########################################
    # SSH FILE SYSTEMS
    ########################################

    def total_ssh_file_system_access_per_assistants(self):
        # Calculate the total number of SSH file system access for each assistant for the last self.last_days days
        # Return the total SSH file system access as a dictionary
        assistant_ssh_file_system_access = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_ssh_file_system_access = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.FILE_SYSTEM_COMMANDS]:
                    total_ssh_file_system_access += 1
            assistant_ssh_file_system_access[assistant.name] = total_ssh_file_system_access
        self.statistics["file_system"][
            'total_ssh_file_system_access_per_assistants'] = assistant_ssh_file_system_access

    ########################################
    # BROWSING
    ########################################

    def total_web_queries_per_assistants(self):
        # Calculate the total number of web queries for each assistant for the last self.last_days days
        # Return the total web queries as a dictionary
        assistant_web_queries = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_web_queries = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.BROWSING]:
                    total_web_queries += 1
            assistant_web_queries[assistant.name] = total_web_queries
        self.statistics["browsing"]['total_web_queries_per_assistants'] = assistant_web_queries

    ########################################
    # KNOWLEDGE BASE & MULTIMEDIA
    ########################################

    def total_documents_interpretations_per_assistants(self):
        # Calculate the total number of documents uploaded for each assistant for the last self.last_days days
        # Return the total documents uploaded as a dictionary
        assistant_documents_uploaded = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_documents_uploaded = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.INTERPRET_FILE]:
                    total_documents_uploaded += 1
            assistant_documents_uploaded[assistant.name] = total_documents_uploaded
        self.statistics["knowledge_base"][
            'total_documents_interpretations_per_assistants'] = assistant_documents_uploaded

    def total_image_interpretations_per_assistants(self):
        # Calculate the total number of image interpretations for each assistant for the last self.last_days days
        # Return the total image interpretations as a dictionary
        assistant_images_interpreted = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_images_interpreted = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.INTERPRET_IMAGE]:
                    total_images_interpreted += 1
            assistant_images_interpreted[assistant.name] = total_images_interpreted
        self.statistics["knowledge_base"]['total_image_interpretations_per_assistants'] = assistant_images_interpreted

    def total_code_interpretations_per_assistants(self):
        # Calculate the total number of code interpretations for each assistant for the last self.last_days days
        # Return the total code interpretations as a dictionary
        assistant_code_interpreted = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_code_interpreted = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.INTERPRET_CODE]:
                    total_code_interpreted += 1
            assistant_code_interpreted[assistant.name] = total_code_interpreted
        self.statistics["knowledge_base"]['total_code_interpretations_per_assistants'] = assistant_code_interpreted

    def total_file_downloads_per_assistants(self):
        # Calculate the total number of file downloads for each assistant for the last self.last_days days
        # Return the total file downloads as a dictionary
        assistant_file_downloads = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_file_downloads = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.DOWNLOAD_FILE]:
                    total_file_downloads += 1
            assistant_file_downloads[assistant.name] = total_file_downloads
        self.statistics["knowledge_base"]['total_file_downloads_per_assistants'] = assistant_file_downloads

    def total_multimedia_generations_per_assistants(self):
        # Calculate the total number of multimedia generations for each assistant for the last self.last_days days
        # Return the total multimedia generations as a dictionary
        assistant_multimedia_generations = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_multimedia_generations = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.GENERATION,
                                                      TransactionSourcesNames.GENERATE_IMAGE,
                                                      TransactionSourcesNames.MODIFY_IMAGE,
                                                      TransactionSourcesNames.VARIATE_IMAGE]:
                    total_multimedia_generations += 1
            assistant_multimedia_generations[assistant.name] = total_multimedia_generations
        self.statistics["knowledge_base"][
            'total_multimedia_generations_per_assistants'] = assistant_multimedia_generations

    def total_knowledge_base_searches_per_assistants(self):
        # Calculate the total number of knowledge base searches for each assistant for the last self.last_days days
        # Return the total knowledge base searches as a dictionary
        assistant_knowledge_base_searches = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_knowledge_base_searches = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.KNOWLEDGE_BASE_SEARCH]:
                    total_knowledge_base_searches += 1
            assistant_knowledge_base_searches[assistant.name] = total_knowledge_base_searches
        self.statistics["knowledge_base"][
            'total_knowledge_base_searches_per_assistants'] = assistant_knowledge_base_searches

    def total_memory_saves_per_assistants(self):
        # Calculate the total number of memory saves for each assistant for the last self.last_days days
        # Return the total memory saves as a dictionary
        assistant_memory_saves = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_memory_saves = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.STORE_MEMORY]:
                    total_memory_saves += 1
            assistant_memory_saves[assistant.name] = total_memory_saves
        self.statistics["knowledge_base"]['total_memory_saves_per_assistants'] = assistant_memory_saves

    def total_memory_retrievals_per_assistants(self):
        # Calculate the total number of memory retrievals for each assistant for the last self.last_days days
        # Return the total memory retrievals as a dictionary
        assistant_memory_retrievals = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_memory_retrievals = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.RETRIEVE_MEMORY]:
                    total_memory_retrievals += 1
            assistant_memory_retrievals[assistant.name] = total_memory_retrievals
        self.statistics["knowledge_base"]['total_memory_retrievals_per_assistants'] = assistant_memory_retrievals

    ########################################
    # FUNCTIONS
    ########################################

    def total_internal_function_calls_per_assistants(self):
        # Calculate the total number of internal function calls for each assistant for the last self.last_days days
        # Return the total internal function calls as a dictionary
        assistant_internal_function_calls = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_internal_function_calls = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.INTERNAL_FUNCTION_EXECUTION]:
                    total_internal_function_calls += 1
            assistant_internal_function_calls[assistant.name] = total_internal_function_calls
        self.statistics["functions"][
            'total_internal_function_calls_per_assistants'] = assistant_internal_function_calls

    def total_external_function_calls_per_assistants(self):
        # Calculate the total number of external function calls for each assistant for the last self.last_days days
        # Return the total external function calls as a dictionary
        assistant_external_function_calls = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_external_function_calls = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.EXTERNAL_FUNCTION_EXECUTION]:
                    total_external_function_calls += 1
            assistant_external_function_calls[assistant.name] = total_external_function_calls
        self.statistics["functions"][
            'total_external_function_calls_per_assistants'] = assistant_external_function_calls

    def total_function_calls_per_assistants(self):
        # Calculate the total number of function calls for each assistant for the last self.last_days days
        # Return the total function calls as a dictionary
        assistant_function_calls = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_function_calls = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.INTERNAL_FUNCTION_EXECUTION,
                                                      TransactionSourcesNames.EXTERNAL_FUNCTION_EXECUTION]:
                    total_function_calls += 1
            assistant_function_calls[assistant.name] = total_function_calls
        self.statistics["functions"]['total_function_calls_per_assistants'] = assistant_function_calls

    ########################################
    # THIRD-PARTY APIS
    ########################################

    def total_internal_third_party_api_calls_per_assistants(self):
        # Calculate the total number of internal third-party API calls for each assistant for the last self.last_days days
        # Return the total internal third-party API calls as a dictionary
        assistant_internal_third_party_api_calls = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_internal_third_party_api_calls = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.INTERNAL_API_EXECUTION]:
                    total_internal_third_party_api_calls += 1
            assistant_internal_third_party_api_calls[assistant.name] = total_internal_third_party_api_calls
        self.statistics["apis"][
            'total_internal_third_party_api_calls_per_assistants'] = assistant_internal_third_party_api_calls

    def total_external_third_party_api_calls_per_assistants(self):
        # Calculate the total number of external third-party API calls for each assistant for the last self.last_days days
        # Return the total external third-party API calls as a dictionary
        assistant_external_third_party_api_calls = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_external_third_party_api_calls = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.EXTERNAL_API_EXECUTION]:
                    total_external_third_party_api_calls += 1
            assistant_external_third_party_api_calls[assistant.name] = total_external_third_party_api_calls
        self.statistics["apis"][
            'total_external_third_party_api_calls_per_assistants'] = assistant_external_third_party_api_calls

    def total_third_party_api_calls_per_assistants(self):
        # Calculate the total number of third-party API calls for each assistant for the last self.last_days days
        # Return the total third-party API calls as a dictionary
        assistant_third_party_api_calls = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_third_party_api_calls = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.INTERNAL_API_EXECUTION,
                                                      TransactionSourcesNames.EXTERNAL_API_EXECUTION]:
                    total_third_party_api_calls += 1
            assistant_third_party_api_calls[assistant.name] = total_third_party_api_calls
        self.statistics["apis"]['total_third_party_api_calls_per_assistants'] = assistant_third_party_api_calls

    ########################################
    # SCRIPTS
    ########################################

    def total_internal_script_executions_per_assistants(self):
        # Calculate the total number of script executions for each assistant for the last self.last_days days
        # Return the total script executions as a dictionary
        assistant_script_executions = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_script_executions = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.INTERNAL_SCRIPT_RETRIEVAL]:
                    total_script_executions += 1
            assistant_script_executions[assistant.name] = total_script_executions
        self.statistics["scripts"]['total_internal_script_executions_per_assistants'] = assistant_script_executions

    def total_external_script_executions_per_assistants(self):
        # Calculate the total number of external script executions for each assistant for the last self.last_days days
        # Return the total external script executions as a dictionary
        assistant_script_executions = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_script_executions = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.EXTERNAL_SCRIPT_RETRIEVAL]:
                    total_script_executions += 1
            assistant_script_executions[assistant.name] = total_script_executions
        self.statistics["scripts"]['total_external_script_executions_per_assistants'] = assistant_script_executions

    def total_script_executions_per_assistants(self):
        # Calculate the total number of script executions for each assistant for the last self.last_days days
        # Return the total script executions as a dictionary
        assistant_script_executions = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_script_executions = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.INTERNAL_SCRIPT_RETRIEVAL,
                                                      TransactionSourcesNames.EXTERNAL_SCRIPT_RETRIEVAL]:
                    total_script_executions += 1
            assistant_script_executions[assistant.name] = total_script_executions
        self.statistics["scripts"]['total_script_executions_per_assistants'] = assistant_script_executions

    ########################################
    # SCHEDULED TASKS
    ########################################

    def total_scheduled_task_executions_per_assistants(self):
        # Calculate the total number of scheduled task executions for each assistant for the last self.last_days days
        # Return the total scheduled task executions as a dictionary
        assistant_scheduled_task_executions = {}
        for assistant in self.assistants:
            assistant_jobs = 0
            for job in self.scheduled_jobs:
                scheduled_job_instances = ScheduledJobInstance.objects.filter(
                    scheduled_job=job,
                    started_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
                )
                assistant_jobs += scheduled_job_instances.count()
            assistant_scheduled_task_executions[assistant.name] = assistant_jobs
        self.statistics["crons"][
            'total_scheduled_task_executions_per_assistants'] = assistant_scheduled_task_executions

    ########################################
    # TRIGGERED TASKS
    ########################################

    def total_triggered_task_executions_per_assistants(self):
        # Calculate the total number of triggered task executions for each assistant for the last self.last_days days
        # Return the total triggered task executions as a dictionary
        assistant_triggered_task_executions = {}
        for assistant in self.assistants:
            assistant_jobs = 0
            for job in self.triggered_jobs:
                triggered_job_instances = TriggeredJobInstance.objects.filter(
                    triggered_job=job,
                    started_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
                )
                assistant_jobs += triggered_job_instances.count()
            assistant_triggered_task_executions[assistant.name] = assistant_jobs
        self.statistics["triggers"][
            'total_triggered_task_executions_per_assistants'] = assistant_triggered_task_executions

    ########################################
    # USERS
    ########################################

    def total_users_per_organizations(self):
        # Calculate the total number of users for each organization
        # Return the total users as a dictionary
        organization_users = {}
        for organization in self.organizations:
            organization_users[organization.name] = organization.users.count()
        self.statistics["users"]['total_users_per_organizations'] = organization_users

    def latest_registered_users_per_organizations(self):
        # Calculate the latest registered users for each organization
        # Return the latest registered users as a dictionary
        organization_users = {}
        for organization in self.organizations:
            organization_users[organization.name] = organization.users.filter(
                date_joined__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            ).count()
        self.statistics["users"]['latest_registered_users_per_organizations'] = organization_users

    ########################################
    # MACHINE LEARNING
    ########################################

    def total_ml_predictions_per_assistants(self):
        # Calculate the total number of ML predictions for each assistant for the last self.last_days days
        # Return the total ML predictions as a dictionary
        assistant_ml_predictions = {}
        for assistant in self.assistants:
            transactions = self.transactions.filter(
                responsible_assistant=assistant,
                created_at__gte=timezone.now() - timezone.timedelta(days=self.last_days)
            )
            total_ml_predictions = 0
            for transaction in transactions:
                if transaction.transaction_source in [TransactionSourcesNames.ML_MODEL_PREDICTION]:
                    total_ml_predictions += 1
            assistant_ml_predictions[assistant.name] = total_ml_predictions
        self.statistics["ml"]['total_ml_predictions_per_assistants'] = assistant_ml_predictions


def prepare_data_for_charts(statistics, context):
    # costs
    costs_per_organizations = statistics.get("costs", {}).get("costs_per_organizations", {})
    costs_per_assistants = statistics.get("costs", {}).get("costs_per_assistants", {})
    costs_per_users = statistics.get("costs", {}).get("costs_per_users", {})
    costs_per_sources = statistics.get("costs", {}).get("costs_per_sources", {})
    cost_per_sources_main = costs_per_sources.get("main", {})
    cost_per_sources_tools = costs_per_sources.get("tool", {})
    # skip balance snapshots for now
    # ...
    # tokens
    tokens_per_organizations = statistics.get("tokens", {}).get("tokens_per_organizations", {})
    tokens_per_assistants = statistics.get("tokens", {}).get("tokens_per_assistants", {})
    tokens_per_users = statistics.get("tokens", {}).get("tokens_per_users", {})
    tokens_per_sources = statistics.get("tokens", {}).get("tokens_per_sources", {})
    tokens_per_sources_main = tokens_per_sources.get("main", {})
    tokens_per_sources_tools = tokens_per_sources.get("tool", {})
    # assistant communication
    total_chats_per_organizations = statistics.get("communication").get("total_chats_per_organizations", {})
    total_messages_per_organizations = statistics.get("communication").get("total_messages_per_organizations", {})
    total_request_count_per_exported_assistants = statistics.get("exports").get(
        "total_request_count_per_exported_assistants", {})
    # sql database usage
    total_sql_read_queries_per_assistants = statistics.get("sql").get("total_sql_read_queries_per_assistants", {})
    total_sql_write_queries_per_assistants = statistics.get("sql").get("total_sql_write_queries_per_assistants", {})
    total_sql_queries_per_assistants = statistics.get("sql").get("total_sql_queries_per_assistants", {})
    # file systems
    total_ssh_file_system_access_per_assistants = statistics.get("file_system").get(
        "total_ssh_file_system_access_per_assistants", {})
    # web browsing
    total_web_queries_per_assistants = statistics.get("browsing").get("total_web_queries_per_assistants", {})
    # ml model predictions
    total_ml_predictions_per_assistants = statistics.get("ml").get("total_ml_predictions_per_assistants", {})
    # multimedia management
    total_documents_interpretations_per_assistants = statistics.get("knowledge_base").get(
        "total_documents_interpretations_per_assistants", {})
    total_image_interpretations_per_assistants = statistics.get("knowledge_base").get(
        "total_image_interpretations_per_assistants", {})
    total_code_interpretations_per_assistants = statistics.get("knowledge_base").get(
        "total_code_interpretations_per_assistants", {})
    total_file_downloads_per_assistants = statistics.get("knowledge_base").get("total_file_downloads_per_assistants",
                                                                               {})
    total_multimedia_generations_per_assistants = statistics.get("knowledge_base").get(
        "total_multimedia_generations_per_assistants", {})
    # knowledge base searches
    total_knowledge_base_searches_per_assistants = statistics.get("knowledge_base").get(
        "total_knowledge_base_searches_per_assistants", {})
    # memory management
    total_memory_saves_per_assistants = statistics.get("knowledge_base").get("total_memory_saves_per_assistants", {})
    total_memory_retrievals_per_assistants = statistics.get("knowledge_base").get(
        "total_memory_retrievals_per_assistants", {})
    # function execution
    total_internal_function_calls_per_assistants = statistics.get("functions").get(
        "total_internal_function_calls_per_assistants", {})
    total_external_function_calls_per_assistants = statistics.get("functions").get(
        "total_external_function_calls_per_assistants", {})
    total_function_calls_per_assistants = statistics.get("functions").get("total_function_calls_per_assistants", {})
    # api execution
    total_internal_third_party_api_calls_per_assistants = statistics.get("apis").get(
        "total_internal_third_party_api_calls_per_assistants", {})
    total_external_third_party_api_calls_per_assistants = statistics.get("apis").get(
        "total_external_third_party_api_calls_per_assistants", {})
    total_third_party_api_calls_per_assistants = statistics.get("apis").get(
        "total_third_party_api_calls_per_assistants", {})
    # script execution
    total_internal_script_executions_per_assistants = statistics.get("scripts").get(
        "total_internal_script_executions_per_assistants", {})
    total_external_script_executions_per_assistants = statistics.get("scripts").get(
        "total_external_script_executions_per_assistants", {})
    total_script_executions_per_assistants = statistics.get("scripts").get("total_script_executions_per_assistants",
                                                                           {})
    # cron and trigger jobs
    total_scheduled_task_executions_per_assistants = statistics.get("crons").get(
        "total_scheduled_task_executions_per_assistants", {})
    total_triggered_task_executions_per_assistants = statistics.get("triggers").get(
        "total_triggered_task_executions_per_assistants", {})
    # users
    total_users_per_organizations = statistics.get("users").get("total_users_per_organizations", {})
    latest_registered_users_per_organizations = statistics.get("users").get(
        "latest_registered_users_per_organizations", {})

    # Prepare data for Chart.js / costs / labels
    context["costs_per_organizations_labels"] = list(costs_per_organizations.keys())
    context["costs_per_assistants_labels"] = list(costs_per_assistants.keys())
    context["costs_per_users_labels"] = list(costs_per_users.keys())
    context["costs_per_sources_main_labels"] = list(cost_per_sources_main.keys())
    context["costs_per_sources_tools_labels"] = list(cost_per_sources_tools.keys())
    # Prepare data for Chart.js / costs / values
    context["costs_per_organizations_values"] = list(costs_per_organizations.values())
    context["costs_per_assistants_values"] = list(costs_per_assistants.values())
    context["costs_per_users_values"] = list(costs_per_users.values())
    context["costs_per_sources_main_values"] = list(cost_per_sources_main.values())
    context["costs_per_sources_tools_values"] = list(cost_per_sources_tools.values())

    # Prepare data for Chart.js / tokens / labels
    context["tokens_per_organizations_labels"] = list(tokens_per_organizations.keys())
    context["tokens_per_assistants_labels"] = list(tokens_per_assistants.keys())
    context["tokens_per_users_labels"] = list(tokens_per_users.keys())
    context["tokens_per_sources_main_labels"] = list(tokens_per_sources_main.keys())
    context["tokens_per_sources_tools_labels"] = list(tokens_per_sources_tools.keys())
    # Prepare data for Chart.js / tokens / values
    context["tokens_per_organizations_values"] = list(tokens_per_organizations.values())
    context["tokens_per_assistants_values"] = list(tokens_per_assistants.values())
    context["tokens_per_users_values"] = list(tokens_per_users.values())
    context["tokens_per_sources_main_values"] = list(tokens_per_sources_main.values())
    context["tokens_per_sources_tools_values"] = list(tokens_per_sources_tools.values())

    # Prepare data for Chart.js / assistant communication / labels
    context["total_chats_per_organizations_labels"] = list(total_chats_per_organizations.keys())
    context["total_chat_messages_per_organizations_labels"] = list(total_messages_per_organizations.keys())
    context["total_request_count_per_exported_assistants_labels"] = list(
        total_request_count_per_exported_assistants.keys())
    # Prepare data for Chart.js / assistant communication / values
    context["total_chats_per_organizations_values"] = list(total_chats_per_organizations.values())
    context["total_chat_messages_per_organizations_values"] = list(total_messages_per_organizations.values())
    context["total_request_count_per_exported_assistants_values"] = list(
        total_request_count_per_exported_assistants.values())

    # Prepare data for Chart.js / sql database usage / labels
    context["total_sql_read_queries_per_assistants_labels"] = list(total_sql_read_queries_per_assistants.keys())
    context["total_sql_write_queries_per_assistants_labels"] = list(total_sql_write_queries_per_assistants.keys())
    context["total_sql_queries_per_assistants_labels"] = list(total_sql_queries_per_assistants.keys())
    # Prepare data for Chart.js / sql database usage / values
    context["total_sql_read_queries_per_assistants_values"] = list(total_sql_read_queries_per_assistants.values())
    context["total_sql_write_queries_per_assistants_values"] = list(total_sql_write_queries_per_assistants.values())
    context["total_sql_queries_per_assistants_values"] = list(total_sql_queries_per_assistants.values())

    # Prepare data for Chart.js / file systems / labels
    context["total_ssh_file_system_access_per_assistants_labels"] = list(
        total_ssh_file_system_access_per_assistants.keys())
    # Prepare data for Chart.js / file systems / values
    context["total_ssh_file_system_access_per_assistants_values"] = list(
        total_ssh_file_system_access_per_assistants.values())

    # Prepare data for Chart.js / web browsing / labels
    context["total_web_queries_per_assistants_labels"] = list(total_web_queries_per_assistants.keys())
    # Prepare data for Chart.js / web browsing / values
    context["total_web_queries_per_assistants_values"] = list(total_web_queries_per_assistants.values())

    # Prepare data for Chart.js / ml model predictions / labels
    context["total_ml_predictions_per_assistants_labels"] = list(total_ml_predictions_per_assistants.keys())
    # Prepare data for Chart.js / ml model predictions / values
    context["total_ml_predictions_per_assistants_values"] = list(total_ml_predictions_per_assistants.values())

    # Prepare data for Chart.js / multimedia management / labels
    context["total_documents_interpretations_per_assistants_labels"] = list(
        total_documents_interpretations_per_assistants.keys())
    context["total_image_interpretations_per_assistants_labels"] = list(
        total_image_interpretations_per_assistants.keys())
    context["total_code_interpretations_per_assistants_labels"] = list(
        total_code_interpretations_per_assistants.keys())
    context["total_file_downloads_per_assistants_labels"] = list(total_file_downloads_per_assistants.keys())
    context["total_multimedia_generations_per_assistants_labels"] = list(
        total_multimedia_generations_per_assistants.keys())
    # Prepare data for Chart.js / multimedia management / values
    context["total_documents_interpretations_per_assistants_values"] = list(
        total_documents_interpretations_per_assistants.values())
    context["total_image_interpretations_per_assistants_values"] = list(
        total_image_interpretations_per_assistants.values())
    context["total_code_interpretations_per_assistants_values"] = list(
        total_code_interpretations_per_assistants.values())
    context["total_file_downloads_per_assistants_values"] = list(total_file_downloads_per_assistants.values())
    context["total_multimedia_generations_per_assistants_values"] = list(
        total_multimedia_generations_per_assistants.values())

    # Prepare data for Chart.js / knowledge base searches / labels
    context["total_knowledge_base_searches_per_assistants_labels"] = list(
        total_knowledge_base_searches_per_assistants.keys())
    # Prepare data for Chart.js / knowledge base searches / values
    context["total_knowledge_base_searches_per_assistants_values"] = list(
        total_knowledge_base_searches_per_assistants.values())

    # Prepare data for Chart.js / memory management / labels
    context["total_memory_saves_per_assistants_labels"] = list(total_memory_saves_per_assistants.keys())
    context["total_memory_retrievals_per_assistants_labels"] = list(total_memory_retrievals_per_assistants.keys())
    # Prepare data for Chart.js / memory management / values
    context["total_memory_saves_per_assistants_values"] = list(total_memory_saves_per_assistants.values())
    context["total_memory_retrievals_per_assistants_values"] = list(total_memory_retrievals_per_assistants.values())

    # Prepare data for Chart.js / function execution / labels
    context["total_internal_function_calls_per_assistants_labels"] = list(
        total_internal_function_calls_per_assistants.keys())
    context["total_external_function_calls_per_assistants_labels"] = list(
        total_external_function_calls_per_assistants.keys())
    context["total_function_calls_per_assistants_labels"] = list(total_function_calls_per_assistants.keys())
    # Prepare data for Chart.js / function execution / values
    context["total_internal_function_calls_per_assistants_values"] = list(
        total_internal_function_calls_per_assistants.values())
    context["total_external_function_calls_per_assistants_values"] = list(
        total_external_function_calls_per_assistants.values())
    context["total_function_calls_per_assistants_values"] = list(total_function_calls_per_assistants.values())

    # Prepare data for Chart.js / api execution / labels
    context["total_internal_third_party_api_calls_per_assistants_labels"] = list(
        total_internal_third_party_api_calls_per_assistants.keys())
    context["total_external_third_party_api_calls_per_assistants_labels"] = list(
        total_external_third_party_api_calls_per_assistants.keys())
    context["total_third_party_api_calls_per_assistants_labels"] = list(
        total_third_party_api_calls_per_assistants.keys())
    # Prepare data for Chart.js / api execution / values
    context["total_internal_third_party_api_calls_per_assistants_values"] = list(
        total_internal_third_party_api_calls_per_assistants.values())
    context["total_external_third_party_api_calls_per_assistants_values"] = list(
        total_external_third_party_api_calls_per_assistants.values())
    context["total_third_party_api_calls_per_assistants_values"] = list(
        total_third_party_api_calls_per_assistants.values())

    # Prepare data for Chart.js / script execution / labels
    context["total_internal_script_executions_per_assistants_labels"] = list(
        total_internal_script_executions_per_assistants.keys())
    context["total_external_script_executions_per_assistants_labels"] = list(
        total_external_script_executions_per_assistants.keys())
    context["total_script_executions_per_assistants_labels"] = list(total_script_executions_per_assistants.keys())
    # Prepare data for Chart.js / script execution / values
    context["total_internal_script_executions_per_assistants_values"] = list(
        total_internal_script_executions_per_assistants.values())
    context["total_external_script_executions_per_assistants_values"] = list(
        total_external_script_executions_per_assistants.values())
    context["total_script_executions_per_assistants_values"] = list(total_script_executions_per_assistants.values())

    # Prepare data for Chart.js / cron and trigger jobs / labels
    context["total_scheduled_task_executions_per_assistants_labels"] = list(
        total_scheduled_task_executions_per_assistants.keys())
    context["total_triggered_task_executions_per_assistants_labels"] = list(
        total_triggered_task_executions_per_assistants.keys())
    # Prepare data for Chart.js / cron and trigger jobs / values
    context["total_scheduled_task_executions_per_assistants_values"] = list(
        total_scheduled_task_executions_per_assistants.values())
    context["total_triggered_task_executions_per_assistants_values"] = list(
        total_triggered_task_executions_per_assistants.values())

    # Prepare data for Chart.js / users / labels
    context["total_users_per_organizations_labels"] = list(total_users_per_organizations.keys())
    context["latest_registered_users_per_organizations_labels"] = list(
        latest_registered_users_per_organizations.keys())
    # Prepare data for Chart.js / users / values
    context["total_users_per_organizations_values"] = list(total_users_per_organizations.values())
    context["latest_registered_users_per_organizations_values"] = list(
        latest_registered_users_per_organizations.values())

    return context
