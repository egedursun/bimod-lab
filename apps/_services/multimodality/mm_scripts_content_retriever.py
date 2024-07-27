from apps._services.config.costs_map import ToolCostsMap
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames


class CustomScriptsContentRetriever:

    def __init__(self, context_organization, context_assistant, script):
        self.script = script
        self.context_organization = context_organization
        self.context_assistant = context_assistant

    def retrieve_custom_script_content(self):
        script = self.script
        script_content = script.script_content

        transaction = LLMTransaction(
            organization=self.context_organization,
            model=self.context_assistant.llm_model,
            responsible_user=None,
            responsible_assistant=None,
            encoding_engine="cl100k_base",
            llm_cost=ToolCostsMap.ExternalCustomScriptRetriever.COST
            if self.script.is_public else
            ToolCostsMap.InternalCustomScriptRetriever.COST,
            transaction_type="system",
            transaction_source=TransactionSourcesNames.EXTERNAL_SCRIPT_RETRIEVAL
            if self.script.is_public else
            TransactionSourcesNames.INTERNAL_SCRIPT_RETRIEVAL,
            is_tool_cost=True
        )
        transaction.save()

        response = script_content if script_content else "[The script content is empty.]"
        return response
