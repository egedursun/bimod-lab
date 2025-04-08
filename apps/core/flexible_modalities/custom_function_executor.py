#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: mm_functions_executor.py
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

from apps.llm_transaction.models import LLMTransaction

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames,
    LLMTokenTypesNames
)

from apps.mm_functions.tasks import mm_function_execution_task

logger = logging.getLogger(__name__)


class CustomFunctionExecutor:

    def __init__(
        self,
        context_organization,
        context_assistant,
        function
    ):
        self.function = function
        self.context_organization = context_organization
        self.context_assistant = context_assistant

    def execute_custom_function(self, input_data):
        from apps.core.generative_ai.utils import (
            GPT_DEFAULT_ENCODING_ENGINE
        )

        from apps.core.generative_ai.utils import ChatRoles

        function_id = self.function.id

        promise = mm_function_execution_task.delay(
            function_id,
            input_data
        )

        response = promise.get()

        tx = LLMTransaction(
            organization=self.context_organization,
            model=self.context_assistant.llm_model,
            responsible_user=None,
            responsible_assistant=None,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.EXTERNAL_FUNCTION_EXECUTION
            if self.function.is_public else LLMTransactionSourcesTypesNames.INTERNAL_FUNCTION_EXECUTION,
            is_tool_cost=True,
            llm_token_type=LLMTokenTypesNames.OUTPUT,
        )

        tx.save()

        logger.info(f"Executed custom function: {self.function.name} with response: {response}")

        return response
