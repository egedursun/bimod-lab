#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: verify_browser_query.py
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


def verify_browser_query_content(content: dict):
    if "parameters" not in content:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Browser Execution tool.
            Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    ps = content.get("parameters")
    if "browser_connection_id" not in ps:
        return """
            The 'browser_connection_id' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Browser Execution tool. Please make sure you are defining the 'browser_connection_id' field in the parameters
            field of the tool_usage_json.
        """
    if "action" not in ps:
        return """
            The 'action' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Browser Execution tool. Please make sure you are defining the 'action' field in the parameters
            field of the tool_usage_json.
        """
    if ps["action"] not in [
        "browser_search", "click_url_in_search"
    ]:
        return """
            The 'action' field in the 'parameters' field of the tool_usage_json must be one of the following values:
            'browser_search', 'click_url_in_search'. This field is mandatory for using the Browser Execution tool.
            Please make sure you are defining the 'action' field in the parameters field of the tool_usage_json.
        """
    if ps["action"] == "browser_search":
        if "query" not in ps:
            return """
                The 'query' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
                using the Browser Execution tool with the 'browser_search' action. Please make sure you are defining the 'query'
                field in the parameters field of the tool_usage_json.
            """
        if "page" not in ps:
            return """
                The 'page' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
                using the Browser Execution tool with the 'browser_search' action. Please make sure you are defining the 'page'
                field in the parameters field of the tool_usage_json.
            """
    elif ps["action"] == "click_url_in_search":
        if "search_results" not in ps:
            return """
                The 'search_results' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
                using the Browser Execution tool with the 'click_url_in_search' action. Please make sure you are defining the 'search_results'
                field in the parameters field of the tool_usage_json.
            """
        if not isinstance(ps["search_results"], list):
            return """
                The 'search_results' field in the 'parameters' field of the tool_usage_json must be a list. This field is mandatory for
                using the Browser Execution tool with the 'click_url_in_search' action. Please make sure you are defining the 'search_results'
                field in the parameters field of the tool_usage_json.
            """
        if "click_url" not in ps:
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
    return None
