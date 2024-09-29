#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: leanmod_expert_network_query_validator.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:14:57
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

def validate_expert_network_query_tool_json(tool_usage_json):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' is missing from tool_usage_json. This field is mandatory to use Expert Network Query
            Execution tool.
        """
    parameters = tool_usage_json.get("parameters")

    if "assistant_id" not in parameters:
        return """
            The 'alpha' field is missing from 'parameters' field in tool_usage_json. This field is mandatory for
            using Expert Network Query Execution tool.
        """

    if "query" not in parameters:
        return """
            The 'query' field is missing from 'parameters' field in tool_usage_json. This field is mandatory for
            using Expert Network Query Execution tool.
        """

    if not isinstance(parameters.get("image_urls"), list) and parameters.get("image_urls") is not None:
        return """
            The 'image_urls' field must be a list of URLs of images.
        """

    if not isinstance(parameters.get("file_urls"), list) and parameters.get("file_urls") is not None:
        return """
            The 'file_urls' field must be a list of URLs of files.
        """

    print(
        f"[leanmod_expert_network_query_validator.validate_expert_network_query_tool_json] Validation is successful.")
    return None
