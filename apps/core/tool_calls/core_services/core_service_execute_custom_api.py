#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: core_service_execute_custom_api.py
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


from apps.core.flexible_modalities.custom_api_executor import CustomAPIExecutor
from apps.mm_apis.models import CustomAPIReference


def run_execute_custom_api(ref_id, api_endpoint_str: str, header_path_vals=None, header_query_vals=None,
                           header_body_vals=None):
    ref = CustomAPIReference.objects.filter(id=ref_id).first()
    xc = CustomAPIExecutor(api=ref.custom_api,
                           context_organization=ref.assistant.organization,
                           context_assistant=ref.assistant)
    try:
        output = xc.execute_custom_api(endpoint_name=api_endpoint_str,
                                       path_values=header_path_vals,
                                       query_values=header_query_vals,
                                       body_values=header_body_vals)
    except Exception as e:
        error_msg = f"Error occurred while executing the API: {str(e)}"
        return error_msg
    return output
