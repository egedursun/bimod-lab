#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: verify_dream_image.py
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


def verify_dream_image_content(content: dict):

    if "parameters" not in content:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Image
            Variation tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """

    parameters = content.get("parameters")

    if "image_uri" not in parameters:
        return """
            The 'image_uri' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Image Variation tool. Please make sure you are defining the 'image_uri' field in the parameters
            field of the tool_usage_json.
        """

    if "image_size" not in parameters:
        return """
            The 'image_size' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Image Variation tool. Please make sure you are defining the 'image_size' field in the parameters
            field of the tool_usage_json.
        """

    return None
