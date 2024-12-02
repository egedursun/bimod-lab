#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: verify_media_item_search.py
#  Last Modified: 2024-12-01 23:16:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-01 23:16:48
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


def verify_media_item_search_content(content: dict):
    if "parameters" not in content:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Media
            Item Search tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """

    ps = content.get("parameters")

    if "connection_id" not in ps:
        return """
            The 'connection_id' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Media Item Search tool. Please make sure you are defining the 'connection_id' field in the
            parameters field of the tool_usage_json.
        """

    if "query" not in ps:
        return """
            The 'query' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Media Item Search tool. Please make sure you are defining the 'query' field in the parameters field
            of the tool_usage_json.
        """

    return None
