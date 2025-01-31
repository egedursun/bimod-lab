#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: verify_instant_connection_query.py
#  Last Modified: 2025-01-28 15:45:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-01-28 15:45:01
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

def verify_run_instant_connection_query_content(content: dict):
    if "parameters" not in content:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Instant
            Connection Query Execution tool. Please make sure you are defining the 'parameters' field in the
            tool_usage_json.
        """

    ps = content.get("parameters")

    if "connection_string" not in ps:
        return """
            The 'connection_string' field is missing from the 'parameters' field in the tool_usage_json. This field is
            mandatory for using the Instant Connection Query Execution tool. Please make sure you are defining the
            'connection_string' field in the parameters field of the tool_usage_json.
        """

    if "query_command" not in ps:
        return """
            The 'query_command' field is missing from the 'parameters' field in the tool_usage_json. This field is
            mandatory for using the Instant Connection Query Execution tool. Please make sure you are defining the
            'query_command' field in the parameters field of the tool_usage_json.
        """

    return None
