from apps._services.config.costs_map import ToolCostsMap
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames
from apps.mm_functions.tasks import mm_function_execution_task


class CustomFunctionExecutor:

    def __init__(self, context_organization, context_assistant, function):
        self.function = function
        self.context_organization = context_organization
        self.context_assistant = context_assistant

    def execute_custom_function(self, input_data):
        from apps._services.llms.openai import GPT_DEFAULT_ENCODING_ENGINE, ChatRoles
        function_id = self.function.id
        promise = mm_function_execution_task.delay(function_id, input_data)
        response = promise.get()

        transaction = LLMTransaction(
            organization=self.context_organization,
            model=self.context_assistant.llm_model,
            responsible_user=None,
            responsible_assistant=None,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=ToolCostsMap.ExternalCustomFunctionExecutor.COST
            if self.function.is_public else
            ToolCostsMap.InternalCustomFunctionExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=TransactionSourcesNames.EXTERNAL_FUNCTION_EXECUTION
            if self.function.is_public else
            TransactionSourcesNames.INTERNAL_FUNCTION_EXECUTION,
            is_tool_cost=True
        )
        transaction.save()
        return response
