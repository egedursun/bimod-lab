#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: mm_functions_executor.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: mm_functions_executor.py
#  Last Modified: 2024-09-28 15:44:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:08:26
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.config.costs_map import ToolCostsMap
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import TransactionSourcesNames
from apps.mm_functions.tasks import mm_function_execution_task


class CustomFunctionExecutor:

    def __init__(self, context_organization, context_assistant, function):
        self.function = function
        self.context_organization = context_organization
        self.context_assistant = context_assistant

    def execute_custom_function(self, input_data):
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
        function_id = self.function.id
        promise = mm_function_execution_task.delay(function_id, input_data)
        response = promise.get()
        print(f"[CustomFunctionExecutor.execute_custom_function] Response has been received.")

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
        print(f"[CustomFunctionExecutor.execute_custom_function] Transaction has been saved.")
        return response
