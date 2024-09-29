#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: image_variation_tool_validator.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:16:01
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

def validate_image_variation_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Image
            Variation tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

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
    print(f"[image_variation_tool_validator.validate_image_variation_tool_json] Validation is successful.")
    return None
