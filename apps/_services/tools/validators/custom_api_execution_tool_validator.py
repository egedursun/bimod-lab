#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: custom_api_execution_tool_validator.py
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
#  File: custom_api_execution_tool_validator.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:15:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

def validate_custom_api_execution_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the
            Custom API Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "custom_api_reference_id" not in parameters:
        return """
            The 'custom_api_reference_id' field is missing from the 'parameters' field in the tool_usage_json. This field is
            mandatory for using the Custom API Execution tool. Please make sure you are defining the 'custom_api_reference_id'
            field in the parameters field of the tool_usage_json.
        """

    if "endpoint_name" not in parameters:
        return """
            The 'endpoint_name' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Custom API Execution tool. Please make sure you are defining the 'endpoint_name' field in the
            parameters field of the tool_usage_json.
        """

    if "path_values" not in parameters:
        return """
            The 'path_values' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Custom API Execution tool. Please make sure you are defining the 'path_values' field in the
            parameters field of the tool_usage_json.
        """

    if "query_values" not in parameters:
        return """
            The 'query_values' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Custom API Execution tool. Please make sure you are defining the 'query_values' field in the
            parameters field of the tool_usage_json.
        """

    if "body_values" not in parameters:
        return """
            The 'body_values' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Custom API Execution tool. Please make sure you are defining the 'body_values' field in the
            parameters field of the tool_usage_json.
        """
    print(f"[custom_api_execution_tool_validator.validate_custom_api_execution_tool_json] Validation is successful.")
    return None
