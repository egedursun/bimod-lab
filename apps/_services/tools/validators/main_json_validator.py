#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: main_json_validator.py
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


def validate_main_tool_json(tool_usage_json: dict):
    if not tool_usage_json:
        return """
                    The JSON is empty. Please make sure you are passing the correct JSON object to the
                    ToolDecoder class.
                """

    if not tool_usage_json.get("tool"):
        return """
                    The 'tool' field is missing from the tool_usage_json. Please make sure you are defining the tool
                    name in the tool_usage_json.
                """
    print(f"[main_json_validator.validate_main_tool_json] Validation is successful.")
    return None
