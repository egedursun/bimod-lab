#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: reasoning_execution_handler.py
#  Last Modified: 2024-10-06 20:31:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-06 20:31:27
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from apps._services.reasoning.reasoning_executor import ReasoningExecutor
from apps.assistants.models import Assistant
from apps.multimodal_chat.models import MultimodalChat


def execute_reasoning_process(assistant_id, chat_id, query):
    assistant = Assistant.objects.get(id=assistant_id)
    chat = MultimodalChat.objects.get(id=chat_id)
    executor = ReasoningExecutor(assistant=assistant, chat=chat)
    print(f"[reasoning_execution_handler.execute_reasoning_process] Processing the reasoning...")
    response = None
    try:
        response = executor.execute_process_reasoning(query_string=query)
        print(f"[reasoning_execution_handler.execute_reasoning_process] Response is ready.")
        print(f"[reasoning_execution_handler.execute_reasoning_process] Reasoning Response: [{response}]")
    except Exception as e:
        print(
            f"[reasoning_execution_handler.execute_reasoning_process] Error occurred while interpreting the code: {str(e)}")
        return f"Failed to process the reasoning. The cause of the error is as follows: {str(e)}"
    print(f"[code_interpreter_execution_handler.execute_code_interpretation] Reasoning process completed successfully.")
    return response
