#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: custom_api_execution_handler.py
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

from apps._services.multimodality.mm_api_executor import CustomAPIExecutor
from apps.mm_apis.models import CustomAPIReference


def execute_api_executor(custom_api_reference_id, endpoint_name: str, path_values=None, query_values=None,
                         body_values=None):
    api_reference = CustomAPIReference.objects.filter(id=custom_api_reference_id).first()
    executor = CustomAPIExecutor(api=api_reference.custom_api,
                                 context_organization=api_reference.assistant.organization,
                                 context_assistant=api_reference.assistant)
    print(f"[custom_api_execution_handler.execute_api_executor] Executing the API: {api_reference.custom_api.name}.")
    try:
        response = executor.execute_custom_api(endpoint_name=endpoint_name,
                                               path_values=path_values,
                                               query_values=query_values,
                                               body_values=body_values)
    except Exception as e:
        error = f"[custom_api_execution_handler.execute_api_executor] Error occurred while executing the API: {str(e)}"
        return error
    print(f"[custom_api_execution_handler.execute_api_executor] API executed successfully.")
    return response
