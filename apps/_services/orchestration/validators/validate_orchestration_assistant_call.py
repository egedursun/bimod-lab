#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: validate_orchestration_assistant_call.py
#  Last Modified: 2024-10-05 02:25:59
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
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

def validate_orchestration_worker_assistant_call_execution_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the
            Worker Assistant Call Execution tool. Please make sure you are defining the 'parameters' field in the
            tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "assistant_id" not in parameters:
        return """
            The 'assistant_id' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Worker Assistant Call Execution tool. Please make sure you are defining the 'assistant_id' field in
            the parameters field of the tool_usage_json.
        """

    if "query" not in parameters:
        return """
            The 'query' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Worker Assistant Call Execution tool. Please make sure you are defining the 'query' field in
            the parameters field of the tool_usage_json.
        """

    print(f"[validate_orchestration_assistant_call.validate_orchestration_worker_assistant_call_execution_tool_json] "
          f"Validation is successful.")
    return None
