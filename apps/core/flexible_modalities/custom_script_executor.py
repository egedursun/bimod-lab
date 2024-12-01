#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames


logger = logging.getLogger(__name__)


class CustomScriptsContentRetriever:

    def __init__(
        self,
        context_organization,
        context_assistant,
        script
    ):
        self.script = script
        self.context_organization = context_organization
        self.context_assistant = context_assistant

    def retrieve_custom_script_content(self):

        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles

        script = self.script
        script_content = script.script_content

        tx = LLMTransaction(
            organization=self.context_organization,
            model=self.context_assistant.llm_model,
            responsible_user=None,
            responsible_assistant=None,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.ExternalCustomScriptExecutor.COST
            if self.script.is_public else InternalServiceCosts.InternalCustomScriptExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.EXTERNAL_SCRIPT_RETRIEVAL
            if self.script.is_public else LLMTransactionSourcesTypesNames.INTERNAL_SCRIPT_RETRIEVAL,
            is_tool_cost=True
        )
        tx.save()

        response = script_content if script_content else "[The script content is empty.]"
        logger.info(f"Retrieved custom script content: {script.name}")
        return response
