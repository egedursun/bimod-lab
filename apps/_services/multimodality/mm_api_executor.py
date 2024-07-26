from apps._services.config.costs_map import ToolCostsMap
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames
from apps.mm_apis.tasks import mm_api_execution_task


class CustomAPIExecutor:

    def __init__(self, context_organization, context_assistant, api):
        self.api = api
        self.context_organization = context_organization
        self.context_assistant = context_assistant

    def execute_custom_api(self, endpoint_name: str, path_values=None, query_values=None, body_values=None):
        api_id = self.api.id
        promise = mm_api_execution_task.delay(
            custom_api_id=api_id,
            endpoint_name=endpoint_name,
            path_values=path_values,
            query_values=query_values,
            body_values=body_values)
        response = promise.get()

        transaction = LLMTransaction(
            organization=self.context_organization,
            model=self.context_assistant.llm_model,
            responsible_user=None,
            responsible_assistant=None,
            encoding_engine="cl100k_base",
            llm_cost=ToolCostsMap.ExternalCustomFunctionExecutor.COST
            if self.api.is_public else
            ToolCostsMap.InternalCustomFunctionExecutor.COST,
            transaction_type="system",
            transaction_source=TransactionSourcesNames.EXTERNAL_API_EXECUTION
            if self.api.is_public else
            TransactionSourcesNames.INTERNAL_API_EXECUTION,
            is_tool_cost=True
        )
        transaction.save()

        return response
