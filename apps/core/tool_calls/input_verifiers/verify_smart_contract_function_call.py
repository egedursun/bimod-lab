#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: verify_smart_contract_function_call.py
#  Last Modified: 2024-10-22 00:26:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 00:26:50
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

def verify_smart_contract_function_call_content(content: dict):
    if "parameters" not in content:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Smart Contract
             Function Call Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    ps = content.get("parameters")
    if "smart_contract_id" not in ps:
        return """
            The 'smart_contract_id' field is missing from the 'parameters' field in the tool_usage_json. This field is
            mandatory for using the Smart Contract Function Call Execution tool. Please make sure you are defining the
            'file_paths' field in the parameters field of the tool_usage_json.
        """
    if "function_name" not in ps:
        return """
            The 'function_name' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Smart Contract Function Call Execution tool. Please make sure you are defining the 'function_name'
            field in the parameters field of the tool_usage_json.
        """
    if "function_kwargs" not in ps:
        return """
            The 'function_kwargs' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Smart Contract Function Call Execution tool. Please make sure you are defining the 'function_kwargs'
            field in the parameters field of the tool_usage_json.
        """
    if not isinstance(ps.get("function_kwargs"), dict):
        return """
            The 'function_kwargs' field in the 'parameters' field of the tool_usage_json must be a dictionary. This field is
            mandatory for using the Smart Contract Function Call Execution tool. Please make sure you are defining the
            'function_kwargs' field in the parameters field of the tool_usage_json.
        """
    return None
