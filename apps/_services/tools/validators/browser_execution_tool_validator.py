#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: browser_execution_tool_validator.py
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
#  File: browser_execution_tool_validator.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:15:26
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

def validate_browser_execution_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Browser Execution tool.
            Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "browser_connection_id" not in parameters:
        return """
            The 'browser_connection_id' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Browser Execution tool. Please make sure you are defining the 'browser_connection_id' field in the parameters
            field of the tool_usage_json.
        """

    if "action" not in parameters:
        return """
            The 'action' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Browser Execution tool. Please make sure you are defining the 'action' field in the parameters
            field of the tool_usage_json.
        """

    if parameters["action"] not in [
        "browser_search", "click_url_in_search"
    ]:
        return """
            The 'action' field in the 'parameters' field of the tool_usage_json must be one of the following values:
            'browser_search', 'click_url_in_search'. This field is mandatory for using the Browser Execution tool.
            Please make sure you are defining the 'action' field in the parameters field of the tool_usage_json.
        """

    if parameters["action"] == "browser_search":
        if "query" not in parameters:
            return """
                The 'query' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
                using the Browser Execution tool with the 'browser_search' action. Please make sure you are defining the 'query'
                field in the parameters field of the tool_usage_json.
            """
        if "page" not in parameters:
            return """
                The 'page' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
                using the Browser Execution tool with the 'browser_search' action. Please make sure you are defining the 'page'
                field in the parameters field of the tool_usage_json.
            """
    elif parameters["action"] == "click_url_in_search":
        if "search_results" not in parameters:
            return """
                The 'search_results' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
                using the Browser Execution tool with the 'click_url_in_search' action. Please make sure you are defining the 'search_results'
                field in the parameters field of the tool_usage_json.
            """
        if not isinstance(parameters["search_results"], list):
            return """
                The 'search_results' field in the 'parameters' field of the tool_usage_json must be a list. This field is mandatory for
                using the Browser Execution tool with the 'click_url_in_search' action. Please make sure you are defining the 'search_results'
                field in the parameters field of the tool_usage_json.
            """
        if "click_url" not in parameters:
            return """
                The 'click_url' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
                using the Browser Execution tool with the 'click_url_in_search' action. Please make sure you are defining the 'click_url'
                field in the parameters field of the tool_usage_json.
            """
    else:
        return """
            The 'action' field in the 'parameters' field of the tool_usage_json must be one of the following values:
            'connect', 'close', 'browser_search', 'get_search_results', 'click_url_in_search', 'get_title', 'get_page_content'.
            This field is mandatory for using the Browser Execution tool. Please make sure you are defining the 'action' field in
            the parameters field of the tool_usage_json.
        """
    print("[validate_browser_execution_tool_json] The Browser Execution tool JSON is valid.")
    return None
