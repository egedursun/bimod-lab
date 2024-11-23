#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: verify_run_custom_function.py
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


def verify_run_custom_function_content(content: dict):
    if "parameters" not in content:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Custom
            Function Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """

    ps = content.get("parameters")

    if "custom_function_reference_id" not in ps:
        return """
            The 'custom_function_reference_id' field is missing from the 'parameters' field in the tool_usage_json. This field is
            mandatory for using the Custom Function Execution tool. Please make sure you are defining the 'custom_function_reference_id'
            field in the parameters field of the tool_usage_json.
        """

    if "input_data" not in ps:
        return """
            The 'input_data' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Custom Function Execution tool. Please make sure you are defining the 'input_data' field in the
            parameters field of the tool_usage_json.
        """

    if not isinstance(ps.get("input_data"), dict):
        return """
            The 'input_data' field in the 'parameters' field of the tool_usage_json must be a dictionary. This field is
            mandatory for using the Custom Function Execution tool. Please make sure you are defining the 'input_data'
            field in the parameters field of the tool_usage_json.
        """

    return None
