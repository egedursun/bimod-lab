#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: verify_semantor_consultation_query.py
#  Last Modified: 2024-11-10 17:14:29
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-10 17:14:30
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


def verify_semantor_consultation_query_content(content: dict):

    if "parameters" not in content:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Semantor
            Consultation tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """

    ps = content.get("parameters")

    if "query" not in ps:
        return """
            The 'query' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Semantor Consultation tool. Please make sure you are defining the 'query' field in the parameters field
            of the tool_usage_json.
        """

    if "object_id" not in ps:
        return """
            The 'object_id' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Semantor Consultation tool. Please make sure you are defining the 'object_id' field in the parameters field
            of the tool_usage_json.
        """

    if "is_local" not in ps:
        return """
            The 'is_local' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Semantor Consultation tool. Please make sure you are defining the 'is_local' field in the parameters field
            of the tool_usage_json.
        """

    if type(ps.get("is_local")) is not bool:
        return """
            The 'is_local' field in the 'parameters' field of the tool_usage_json must be a boolean. Please make sure you are
            defining the 'is_local' field as a boolean in the parameters field of the tool_usage_json.
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
