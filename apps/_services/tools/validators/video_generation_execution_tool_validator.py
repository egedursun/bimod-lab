#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: video_generation_execution_tool_validator.py
#  Last Modified: 2024-10-01 22:54:15
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
#  File: video_generation_execution_tool_validator.py
#  Last Modified: 2024-10-01 18:23:33
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-10-01 18:23:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#


from apps._services.video_generation.utils import VideoGenerationActionTypes


def validate_video_generation_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Video
            Generation tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "connection_id" not in parameters:
        return """
            The 'connection_id' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Video Generation tool. Please make sure you are defining the 'connection_id' field in the parameters field
            of the tool_usage_json.
        """

    if "action_type" not in parameters:
        return """
            The 'action_type' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Video Generation tool. Please make sure you are defining the 'action_type' field in the parameters field
            of the tool_usage_json.
        """

    action_type = parameters.get("action_type")
    if action_type not in VideoGenerationActionTypes.as_list():
        return """
            The 'action_type' field in the 'parameters' field of the tool_usage_json is invalid. Please make sure you are defining
            a valid 'action_type' field in the parameters field of the tool_usage_json.
        """

    if "query" not in parameters:
        return """
            The 'query' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Video Generation tool. Please make sure you are defining the 'query' field in the parameters field
            of the tool_usage_json.
        """

    #################################################################################################################

    if action_type == VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP_AND_ASPECT_RATIO:
        if "aspect_ratio" not in parameters:
            return """
                The 'aspect_ratio' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
                using the Video Generation tool with the 'TEXT_TO_VIDEO_WITH_LOOP_AND_ASPECT_RATIO' action type. Please make sure
                you are defining the 'aspect_ratio' field in the parameters field of the tool_usage_json.
            """

    if action_type == VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_ASPECT_RATIO:
        if "aspect_ratio" not in parameters:
            return """
                The 'aspect_ratio' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
                using the Video Generation tool with the 'TEXT_TO_VIDEO_WITH_ASPECT_RATIO' action type. Please make sure
                you are defining the 'aspect_ratio' field in the parameters field of the tool_usage_json.
            """

    if action_type == VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP:
        # No additional validation is required for this action type.
        pass
        #############################################################

    if action_type == VideoGenerationActionTypes.TEXT_TO_VIDEO:
        # No additional validation is required for this action type.
        pass
        #############################################################

    if action_type == VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_LOOP_AND_WITH_START_FRAME:
        if "start_frame_url" not in parameters:
            return """
                The 'start_frame_url' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
                using the Video Generation tool with the 'TEXT_AND_IMAGE_TO_VIDEO_WITH_LOOP_AND_WITH_START_FRAME' action type. Please make
                sure you are defining the 'start_frame_url' field in the parameters field of the tool_usage_json.
            """

    if action_type == VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_FRAME:
        if "start_frame_url" not in parameters:
            return """
                The 'start_frame_url' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
                using the Video Generation tool with the 'TEXT_AND_IMAGE_TO_VIDEO_WITH_START_FRAME' action type. Please make sure
                you are defining the 'start_frame_url' field in the parameters field of the tool_usage_json.
            """

    if action_type == VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_END_FRAME:
        if "end_frame_url" not in parameters:
            return """
                The 'end_frame_url' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
                using the Video Generation tool with the 'TEXT_AND_IMAGE_TO_VIDEO_WITH_END_FRAME' action type. Please make sure
                you are defining the 'end_frame_url' field in the parameters field of the tool_usage_json.
            """

    if action_type == VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_AND_END_FRAME:
        if "start_frame_url" not in parameters:
            return """
                The 'start_frame_url' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
                using the Video Generation tool with the 'TEXT_AND_IMAGE_TO_VIDEO_WITH_START_AND_END_FRAME' action type. Please make
                sure you are defining the 'start_frame_url' field in the parameters field of the tool_usage_json.
            """

        if "end_frame_url" not in parameters:
            return """
                The 'end_frame_url' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
                using the Video Generation tool with the 'TEXT_AND_IMAGE_TO_VIDEO_WITH_START_AND_END_FRAME' action type. Please make
                sure you are defining the 'end_frame_url' field in the parameters field of the tool_usage_json.
            """

    print(f"[video_generation_execution_tool_validator.validate_video_generation_tool_json] Validation is successful.")
    return None
