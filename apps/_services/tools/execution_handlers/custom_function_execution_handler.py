#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: custom_function_execution_handler.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:33
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
#  File: custom_function_execution_handler.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:14:16
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.multimodality.mm_functions_executor import CustomFunctionExecutor
from apps.mm_functions.models import CustomFunctionReference


def execute_custom_code_executor(custom_function_reference_id, input_values: dict):
    function_reference = CustomFunctionReference.objects.filter(id=custom_function_reference_id).first()
    print(
        f"[custom_function_execution_handler.execute_custom_code_executor] Executing the function: {function_reference.custom_function.name}.")
    try:
        executor = CustomFunctionExecutor(function=function_reference.custom_function,
                                          context_organization=function_reference.assistant.organization,
                                          context_assistant=function_reference.assistant)
        response = executor.execute_custom_function(input_data=input_values)
    except Exception as e:
        error = (f"[custom_function_execution_handler.execute_custom_code_executor] Error occurred while executing "
                 f"the function: {str(e)}")
        return error
    print(f"[custom_function_execution_handler.execute_custom_code_executor] Function executed successfully.")
    return response
