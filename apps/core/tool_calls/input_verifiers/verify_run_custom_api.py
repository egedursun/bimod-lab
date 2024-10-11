#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: verify_run_custom_api.py
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


def verify_run_custom_api_content(content: dict):
    if "parameters" not in content:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the
            Custom API Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    ps = content.get("parameters")
    if "custom_api_reference_id" not in ps:
        return """
            The 'custom_api_reference_id' field is missing from the 'parameters' field in the tool_usage_json. This field is
            mandatory for using the Custom API Execution tool. Please make sure you are defining the 'custom_api_reference_id'
            field in the parameters field of the tool_usage_json.
        """
    if "endpoint_name" not in ps:
        return """
            The 'endpoint_name' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Custom API Execution tool. Please make sure you are defining the 'endpoint_name' field in the
            parameters field of the tool_usage_json.
        """
    if "path_values" not in ps:
        return """
            The 'path_values' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Custom API Execution tool. Please make sure you are defining the 'path_values' field in the
            parameters field of the tool_usage_json.
        """
    if "query_values" not in ps:
        return """
            The 'query_values' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Custom API Execution tool. Please make sure you are defining the 'query_values' field in the
            parameters field of the tool_usage_json.
        """
    if "body_values" not in ps:
        return """
            The 'body_values' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Custom API Execution tool. Please make sure you are defining the 'body_values' field in the
            parameters field of the tool_usage_json.
        """
    return None
