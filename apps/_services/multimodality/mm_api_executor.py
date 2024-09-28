from apps._services.config.costs_map import ToolCostsMap
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames
from apps.mm_apis.tasks import mm_api_execution_task


class CustomAPIExecutor:

    def __init__(self, context_organization, context_assistant, api):
        self.api = api
        self.context_organization = context_organization
        self.context_assistant = context_assistant

    def execute_custom_api(self, endpoint_name: str, path_values=None, query_values=None, body_values=None):
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
        api_id = self.api.id
        promise = mm_api_execution_task.delay(
            custom_api_id=api_id,
            endpoint_name=endpoint_name,
            path_values=path_values,
            query_values=query_values,
            body_values=body_values)
        response = promise.get()
        print(f"[CustomAPIExecutor.execute_custom_api] Response has been received.")

        transaction = LLMTransaction(
            organization=self.context_organization,
            model=self.context_assistant.llm_model,
            responsible_user=None,
            responsible_assistant=None,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=ToolCostsMap.ExternalCustomAPIExecutor.COST
            if self.api.is_public else
            ToolCostsMap.InternalCustomAPIExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=TransactionSourcesNames.EXTERNAL_API_EXECUTION
            if self.api.is_public else
            TransactionSourcesNames.INTERNAL_API_EXECUTION,
            is_tool_cost=True
        )
        transaction.save()
        print(f"[CustomAPIExecutor.execute_custom_api] Transaction has been saved.")
        return response
