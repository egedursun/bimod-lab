#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_execute_custom_function.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from apps.core.flexible_modalities.custom_function_executor import CustomFunctionExecutor
from apps.mm_functions.models import CustomFunctionReference

logger = logging.getLogger(__name__)


def run_execute_custom_code(
    ref_id,
    function_input_values: dict
):
    ref = CustomFunctionReference.objects.filter(
        id=ref_id
    ).first()

    try:

        xc = CustomFunctionExecutor(
            function=ref.custom_function,
            context_organization=ref.assistant.organization,
            context_assistant=ref.assistant
        )

        output = xc.execute_custom_function(input_data=function_input_values)
        logger.info(f"Custom function execution output: {output}")

    except Exception as e:
        logger.error(f"Error occurred while executing the function: {e}")
        error_msg = f"Error occurred while executing the function: {str(e)}"
        return error_msg

    return output
