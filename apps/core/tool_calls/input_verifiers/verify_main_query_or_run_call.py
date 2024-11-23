#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: verify_main_query_or_run_call.py
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


def verify_main_call_or_query_content(content: dict):

    if not content:
        return """
                    The JSON is empty. Please make sure you are passing the correct JSON object to the
                    ToolDecoder class.
                """

    if not content.get("tool"):
        return """
                    The 'tool' field is missing from the tool_usage_json. Please make sure you are defining the tool
                    name in the tool_usage_json.
                """

    return None
