#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: code_interpreter_execution_handler.py
#  Last Modified: 2024-10-05 02:31:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#

from apps._services.code_interpreter.code_interpreter_executor import CodeInterpreterExecutor
from apps.assistants.models import Assistant
from apps.multimodal_chat.models import MultimodalChat


def execute_code_interpreter(assistant_id, chat_id, file_paths, query):
    assistant = Assistant.objects.get(id=assistant_id)
    chat = MultimodalChat.objects.get(id=chat_id)
    executor = CodeInterpreterExecutor(assistant=assistant, chat=chat)
    print(f"[code_interpreter_execution_handler.execute_code_interpreter] Executing code interpreter.")
    try:
        response = executor.interpret_code(full_file_paths=file_paths, query_string=query)
        print(f"[code_interpreter_execution_handler.execute_code_interpreter] Response is ready.")
    except Exception as e:
        print(
            f"[code_interpreter_execution_handler.execute_code_interpreter] Error occurred while interpreting the "
            f"code: {str(e)}")
        return None, None, None
    file_uris = response.get("file_uris")
    image_uris = response.get("image_uris")
    print(f"[code_interpreter_execution_handler.execute_code_interpreter] Code interpreted successfully.")
    return response, file_uris, image_uris
