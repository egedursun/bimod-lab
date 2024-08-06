from apps._services.config.costs_map import ToolCostsMap
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames


class CustomScriptsContentRetriever:

    def __init__(self, context_organization, context_assistant, script):
        self.script = script
        self.context_organization = context_organization
        self.context_assistant = context_assistant

    def retrieve_custom_script_content(self):
        from apps._services.llms.openai import GPT_DEFAULT_ENCODING_ENGINE, ChatRoles
        script = self.script
        script_content = script.script_content
        print(f"[CustomScriptsContentRetriever.retrieve_custom_script_content] Script content has been retrieved.")

        transaction = LLMTransaction(
            organization=self.context_organization,
            model=self.context_assistant.llm_model,
            responsible_user=None,
            responsible_assistant=None,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=ToolCostsMap.ExternalCustomScriptExecutor.COST
            if self.script.is_public else
            ToolCostsMap.InternalCustomScriptExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=TransactionSourcesNames.EXTERNAL_SCRIPT_RETRIEVAL
            if self.script.is_public else
            TransactionSourcesNames.INTERNAL_SCRIPT_RETRIEVAL,
            is_tool_cost=True
        )
        transaction.save()
        print(f"[CustomScriptsContentRetriever.retrieve_custom_script_content] Transaction has been saved.")
        response = script_content if script_content else "[The script content is empty.]"
        return response
