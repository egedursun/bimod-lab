#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: verify_expert_network_query_harmoniq.py
#  Last Modified: 2024-10-11 21:11:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-11 21:11:07
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


def verify_expert_network_query_content_harmoniq(content):
    if "parameters" not in content:
        return """
            The 'parameters' is missing from tool_usage_json. This field is mandatory to use Expert Network Query
            Execution tool.
        """
    ps = content.get("parameters")
    if "assistant_id" not in ps:
        return """
            The 'alpha' field is missing from 'parameters' field in tool_usage_json. This field is mandatory for
            using Expert Network Query Execution tool.
        """
    if "query" not in ps:
        return """
            The 'query' field is missing from 'parameters' field in tool_usage_json. This field is mandatory for
            using Expert Network Query Execution tool.
        """
    if not isinstance(ps.get("image_urls"), list) and ps.get("image_urls") is not None:
        return """
            The 'image_urls' field must be a list of URLs of images.
        """
    if not isinstance(ps.get("file_urls"), list) and ps.get("file_urls") is not None:
        return """
            The 'file_urls' field must be a list of URLs of files.
        """
    return None
