#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: custom_script_content_retriever_tool_validator.py
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


def validate_custom_script_retriever_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the
            Custom Script Content Retriever tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "custom_script_reference_id" not in parameters:
        return """
            The 'custom_script_reference_id' field is missing from the 'parameters' field in the tool_usage_json. This field is
            mandatory for using the Custom Script Content Retriever tool. Please make sure you are defining the 'custom_script_reference_id'
            field in the parameters field of the tool_usage_json.
        """
    print(
        f"[custom_script_content_retriever_tool_validator.validate_custom_script_retriever_tool_json] Validation is successful.")
    return None
