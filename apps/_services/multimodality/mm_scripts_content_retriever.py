#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: mm_scripts_content_retriever.py
#  Last Modified: 2024-10-05 02:26:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from apps._services.config.costs_map import ToolCostsMap
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import TransactionSourcesNames


class CustomScriptsContentRetriever:

    def __init__(self, context_organization, context_assistant, script):
        self.script = script
        self.context_organization = context_organization
        self.context_assistant = context_assistant

    def retrieve_custom_script_content(self):
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
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
