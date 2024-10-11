#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: verify_edit_image.py
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
#   For permission inquiries, please contact: admin@br6.in.
#


def verify_edit_image_content(content: dict):
    if "parameters" not in content:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Image
            Modification tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    ps = content.get("parameters")
    if "prompt" not in ps:
        return """
            The 'prompt' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Image Modification tool. Please make sure you are defining the 'prompt' field in the parameters field
            of the tool_usage_json.
        """
    if "image_size" not in ps:
        return """
            The 'image_size' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Image Modification tool. Please make sure you are defining the 'file_paths' field in the parameters
            field of the tool_usage_json.
        """
    if "edit_image_uri" not in ps:
        return """
            The 'edit_image_uri' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Image Modification tool. Please make sure you are defining the 'edit_image_uri' field in the parameters
            field of the tool_usage_json.
        """
    if "edit_image_mask_uri" not in ps:
        return """
            The 'edit_image_mask_uri' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Image Modification tool. Please make sure you are defining the 'edit_image_mask_uri' field in the parameters
            field of the tool_usage_json.
        """
    return None
