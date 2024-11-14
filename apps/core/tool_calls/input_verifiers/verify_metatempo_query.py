#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: verify_metatempo_query.py
#  Last Modified: 2024-11-13 05:11:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 05:12:18
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


def verify_metatempo_query_content(content: dict):
    if "parameters" not in content:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the MetaTempo
            Query Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    ps = content.get("parameters")
    if "connection_id" not in ps:
        return """
            The 'connection_id' field is missing from the 'parameters' field in the tool_usage_json. This
            field is mandatory for using the MetaTempo Query Execution tool. Please make sure you are defining the
            'connection_id' field in the parameters field of the tool_usage_json.
        """
    if "action" not in ps:
        return """
            The 'action' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the MetaTempo Query Execution tool. Please make sure you are defining the 'action' field in the
            parameters field of the tool_usage_json.
        """
    if ps["action"] not in ["QUERY", "REPORT"]:
        return """
            The 'action' field in the 'parameters' field of the tool_usage_json is not valid. The value of the 'action'
            field should be either 'QUERY' or 'REPORT'. Please make sure you are defining the 'action' field in the
            parameters field of the tool_usage_json as either 'QUERY' or 'REPORT'.
        """
    if ps["action"] == "QUERY" and "query" not in ps:
        return """
            The 'prompt' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the MetaTempo Query Execution tool. Please make sure you are defining the 'query' field in the
            parameters field of the tool_usage_json.
        """
    return None
