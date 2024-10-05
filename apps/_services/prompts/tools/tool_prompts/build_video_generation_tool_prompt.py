#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: build_video_generation_tool_prompt.py
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
#  File: build_video_generation_tool_prompt.py
#  Last Modified: 2024-10-01 18:24:22
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-10-01 18:24:24
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#


from apps._services.tools.utils import ToolTypeNames
from apps.assistants.models import Assistant
from apps.video_generations.models import VideoGeneratorConnection
from apps._services.video_generation.utils import VideoGenerationActionTypes
from config.settings import MEDIA_URL


def build_structured_tool_prompt__video_generator(assistant_id: int):
    assistant = Assistant.objects.get(id=assistant_id)
    connections = VideoGeneratorConnection.objects.filter(
        assistant=assistant
    )

    video_generator_connections_text = ""
    for connection in connections:
        video_generator_connections_text += f"""
            --------------------------------------------------
            - ID: {connection.id}
            - Connection Nickname: {connection.name}
            - Connection Description: {connection.description}
             --------------------------------------------------
             ...
        """

    response_prompt = f"""
            **TOOL**: Video Generation Tool

            - The Video Generation Tool is a tool that allows you to generate videos based on the prompts that you provide.
            You can use this tool to generate videos based on the prompts that you provide, and the assistant will generate
            a video based on the prompt you provide. You can use this tool to generate videos for various use cases
            such as generating videos for creative use cases, generating videos for contents, and much more.

            - You CAN ONLY generate videos by using the Video Generator Connections, and you will not be able to generate
            videos unless there is a valid connection available for you to use, since your JSON call requires the input
            of a connection_id field. If you don't have valid connections, don't attempt to generate videos. Below is the
            video generator connections you have. If you dont have any, it will look empty.

            *Video Generator Connections:*
            '''
            {video_generator_connections_text}
            '''

            ---

            - After you decide on which connection to use (if any) to generate the videos, you need to define the action
            you want to perform with the video generation tool. The action types that you can perform with the video
            generation tool, and their **'action_type'** specifiers are as follows:

            1. Text to Video with Loop and Aspect Ratio -> {VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP_AND_ASPECT_RATIO}
            2. Text to Video with Loop -> {VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP}
            3. Text to Video with Aspect Ratio -> {VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_ASPECT_RATIO}
            4. Text to Video -> {VideoGenerationActionTypes.TEXT_TO_VIDEO}
            5. Text and Image to Video with Loop and with Start Frame -> {VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_LOOP_AND_WITH_START_FRAME}
            6. Text and Image to Video with Start Frame -> {VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_FRAME}
            7. Text and Image to Video with End Frame -> {VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_END_FRAME}
            8. Text and Image to Video with Start and End Frame -> {VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_AND_END_FRAME}

            ---

            - The standardized format for the dictionary that you will output to use the Image Generation Tool is as
            follows (where N, A, B are integers, and " symbols represents the variables which are strings):

            '''
                {{
                    "tool": "{ToolTypeNames.VIDEO_GENERATION}",
                    "parameters": {{
                        "connection_id": N,
                        "query": "...",
                        "action_type": "{VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP_AND_ASPECT_RATIO}" | "{VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP}" | "{VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_ASPECT_RATIO}" | "{VideoGenerationActionTypes.TEXT_TO_VIDEO}" | "{VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_LOOP_AND_WITH_START_FRAME}" | "{VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_FRAME}" | "{VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_END_FRAME}" | "{VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_AND_END_FRAME}",
                        "aspect_ratio": "A:B",  #  Only for the action types that require aspect ratio
                        "start_frame_url": "https://www.abc.com",  # Only for the action types that require start frame
                        "end_frame_url": "https://www.abc.com"  # Only for the action types that require end frame
                    }}
                }}
            '''

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:**

            - The "connection_id" field should be the ID of the connection that you would like to use to generate the video.
            You can't leave this field empty, neither you can put a sample/example value here, or make up IDs out of your
            mind. If you don't have an available connection, don't use this tool.

            - The "query" field should be the prompt that you would like to generate the video based on.

           - The "action_type" field should be the action type that you would like to perform with the video generation tool.
              You can choose one of the action types that are listed above. If you fail to provide a valid action type, the
                system will not be able to generate the video for you.

            - The "aspect_ratio" field should be the aspect ratio that you would like to use for the video. This field is
                only required for the action types that require aspect ratio. Otherwise, you can skip this field.

            - The "start_frame_url" field should be the ABSOLUTE URL of the start frame that you would like to use for the video.
                This field is only required for the action types that require a start frame. Otherwise, you can skip this field.
                Don't provide relative URLs, always provide absolute URLs.

            - The "end_frame_url" field should be the ABSOLUTE URL of the end frame that you would like to use for the video.
                This field is only required for the action types that require an end frame. Otherwise, you can skip this field.
                Don't provide relative URLs, always provide absolute URLs.

            To use this tool, you need to be careful about the following details:

            1. Never omit the 'connection_id' field, and always provide a valid connection ID.
            2. Always provide a valid 'action_type' field in the parameters field of the tool_usage_json, don't
            make up action types.
            3. Always provide the 'prompt' field in the parameters field of the tool_usage_json.

            - These 3 fields are always mandatory, and you need to provide them in the parameters field of the tool_usage_json
            whatever the action type you choose to use.

            4. If you are using an action type that requires an aspect ratio, always provide the 'aspect_ratio' field in the
            parameters field of the tool_usage_json.

            5. If you are using an action type that requires a start frame, always provide the 'start_frame_url' field in the
            parameters field of the tool_usage_json.

            6. If you are using an action type that requires an end frame, always provide the 'end_frame_url' field in the
            parameters field of the tool_usage_json.

            ---

            **IMPORTANT NOTES:**

            **NOTE**: The system will provide you with the results in the next 'assistant' message. This message will
            have the output of the query execution, and you will be expected to take this response and provide an answer
            to the user's question based on the response that you receive, in your own words. Think of this tool
            as an employee of yours that you are instructing to execute a query on a media item, and you are expected
            to take the response of this employee and provide an answer to the user's question based on the response
            that you receive from this employee.

            **ABOUT YOU PROVIDING LINKS:**
            - If you need to provide a direct link to the user for reaching the files, here is the base
                URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP reference to the file:
                - {MEDIA_URL}
            - **NEVER, EVER:** provide a 'relative' path to the files. Always provide the 'absolute' path by
            appending the file path to the base URL.

        """
    return response_prompt


def build_lean_structured_tool_prompt__video_generator():
    response_prompt = f"""
            **TOOL**: Video Generation Tool

            - The Video Generation Tool is a tool that allows you to generate videos based on the prompts that you provide.
            You can use this tool to generate videos based on the prompts that you provide, and the assistant will generate
            a video based on the prompt you provide. You can use this tool to generate videos for various use cases
            such as generating videos for creative use cases, generating videos for contents, and much more.

            - You CAN ONLY generate videos by using the Video Generator Connections, and you will not be able to generate
            videos unless there is a valid connection available for you to use, since your JSON call requires the input
            of a connection_id field. If you don't have valid connections, don't attempt to generate videos. Below is the
            video generator connections you have. If you dont have any, it will look empty.

            *Video Generator Connections:*
            '''
            <This data is redacted because you won't need it to serve your instructions.>
            '''

            ---

            - After you decide on which connection to use (if any) to generate the videos, you need to define the action
            you want to perform with the video generation tool. The action types that you can perform with the video
            generation tool, and their **'action_type'** specifiers are as follows:

            1. Text to Video with Loop and Aspect Ratio -> {VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP_AND_ASPECT_RATIO}
            2. Text to Video with Loop -> {VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP}
            3. Text to Video with Aspect Ratio -> {VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_ASPECT_RATIO}
            4. Text to Video -> {VideoGenerationActionTypes.TEXT_TO_VIDEO}
            5. Text and Image to Video with Loop and with Start Frame -> {VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_LOOP_AND_WITH_START_FRAME}
            6. Text and Image to Video with Start Frame -> {VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_FRAME}
            7. Text and Image to Video with End Frame -> {VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_END_FRAME}
            8. Text and Image to Video with Start and End Frame -> {VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_AND_END_FRAME}

            ---

            - The standardized format for the dictionary that you will output to use the Image Generation Tool is as
            follows (where N, A, B are integers, and " symbols represents the variables which are strings):

            '''
                {{
                    "tool": "{ToolTypeNames.VIDEO_GENERATION}",
                    "parameters": {{
                        "connection_id": N,
                        "query": "...",
                        "action_type": "{VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP_AND_ASPECT_RATIO}" | "{VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP}" | "{VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_ASPECT_RATIO}" | "{VideoGenerationActionTypes.TEXT_TO_VIDEO}" | "{VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_LOOP_AND_WITH_START_FRAME}" | "{VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_FRAME}" | "{VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_END_FRAME}" | "{VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_AND_END_FRAME}",
                        "aspect_ratio": "A:B",  #  Only for the action types that require aspect ratio
                        "start_frame_url": "https://www.abc.com",  # Only for the action types that require start frame
                        "end_frame_url": "https://www.abc.com"  # Only for the action types that require end frame
                    }}
                }}
            '''

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:**

            - The "connection_id" field should be the ID of the connection that you would like to use to generate the video.
            You can't leave this field empty, neither you can put a sample/example value here, or make up IDs out of your
            mind. If you don't have an available connection, don't use this tool.

            - The "query" field should be the prompt that you would like to generate the video based on.

           - The "action_type" field should be the action type that you would like to perform with the video generation tool.
              You can choose one of the action types that are listed above. If you fail to provide a valid action type, the
                system will not be able to generate the video for you.

            - The "aspect_ratio" field should be the aspect ratio that you would like to use for the video. This field is
                only required for the action types that require aspect ratio. Otherwise, you can skip this field.

            - The "start_frame_url" field should be the ABSOLUTE URL of the start frame that you would like to use for the video.
                This field is only required for the action types that require a start frame. Otherwise, you can skip this field.
                Don't provide relative URLs, always provide absolute URLs.

            - The "end_frame_url" field should be the ABSOLUTE URL of the end frame that you would like to use for the video.
                This field is only required for the action types that require an end frame. Otherwise, you can skip this field.
                Don't provide relative URLs, always provide absolute URLs.

            To use this tool, you need to be careful about the following details:

            1. Never omit the 'connection_id' field, and always provide a valid connection ID.
            2. Always provide a valid 'action_type' field in the parameters field of the tool_usage_json, don't
            make up action types.
            3. Always provide the 'prompt' field in the parameters field of the tool_usage_json.

            - These 3 fields are always mandatory, and you need to provide them in the parameters field of the tool_usage_json
            whatever the action type you choose to use.

            4. If you are using an action type that requires an aspect ratio, always provide the 'aspect_ratio' field in the
            parameters field of the tool_usage_json.

            5. If you are using an action type that requires a start frame, always provide the 'start_frame_url' field in the
            parameters field of the tool_usage_json.

            6. If you are using an action type that requires an end frame, always provide the 'end_frame_url' field in the
            parameters field of the tool_usage_json.

            ---

            **IMPORTANT NOTES:**

            **NOTE**: The system will provide you with the results in the next 'assistant' message. This message will
            have the output of the query execution, and you will be expected to take this response and provide an answer
            to the user's question based on the response that you receive, in your own words. Think of this tool
            as an employee of yours that you are instructing to execute a query on a media item, and you are expected
            to take the response of this employee and provide an answer to the user's question based on the response
            that you receive from this employee.

            **ABOUT YOU PROVIDING LINKS:**
            - If you need to provide a direct link to the user for reaching the files, here is the base
                URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP reference to the file:
                - {MEDIA_URL}
            - **NEVER, EVER:** provide a 'relative' path to the files. Always provide the 'absolute' path by
            appending the file path to the base URL.

        """
    return response_prompt
