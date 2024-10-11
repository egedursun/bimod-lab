#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: generate_video_tool_prompt.py
#  Last Modified: 2024-10-05 02:25:59
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


from apps.core.tool_calls.utils import ToolCallDescriptorNames
from apps.assistants.models import Assistant
from apps.video_generations.models import VideoGeneratorConnection
from apps.core.video_generation.utils import VideoGenerationActionTypes
from config.settings import MEDIA_URL


def build_tool_prompt__generate_video(assistant_id: int):
    agent = Assistant.objects.get(id=assistant_id)
    conns = VideoGeneratorConnection.objects.filter(assistant=agent)
    video_generator_connections_text = ""
    for connection in conns:
        video_generator_connections_text += f"""
            --------------------------------------------------
            - ID: {connection.id}
            - Connection Nickname: {connection.name}
            - Connection Description: {connection.description}
             --------------------------------------------------
             ...
        """

    response_prompt = f"""
            ### **TOOL**: Video Generation Tool

            - The Video Generation Tool is a tool allows you to generate videos based on prompts you provide.
            You can use this to generate videos based on prompts, and the tool assistant will generate
            a video based on prompt you provided. You can use this to generate videos for various use cases
            such as for creative use cases, for contents, and much more.

            - You CAN ONLY generate videos by using Video Generator Connections, and you will not be able to generate
            videos unless there is a valid connection available for you to use, since your JSON call requires the input
            of a connection_id field. If you don't have valid connections, don't attempt to generate videos. Below is
            the video generator connections you have. If you dont have any, it will look empty.

            #### *Video Generator Connections:*

            '''
            {video_generator_connections_text}
            '''

            ---

            - After you decide on which connection to use (if any) to generate the videos, you need to define the
            action you want to perform on the video generation tool. The action types you can perform with video
            generation tool, and their **'action_type'** specifiers are as follows:

            - [1] Text to Video with Loop and Aspect Ratio -> {VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP_AND_ASPECT_RATIO}
            - [2] Text to Video with Loop -> {VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP}
            - [3] Text to Video with Aspect Ratio -> {VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_ASPECT_RATIO}
            - [4] Text to Video -> {VideoGenerationActionTypes.TEXT_TO_VIDEO}
            - [5] Text and Image to Video with Loop and with Start Frame -> {VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_LOOP_AND_WITH_START_FRAME}
            - [6] Text and Image to Video with Start Frame -> {VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_FRAME}
            - [7] Text and Image to Video with End Frame -> {VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_END_FRAME}
            - [8] Text and Image to Video with Start and End Frame -> {VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_AND_END_FRAME}

            ---

            - The format for dictionary you will output to use Video Generation Tool is as follows (where N, A, B are
                integers, and " symbols represents the variables which are strings):

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_GENERATE_VIDEO}",
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

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:**

            - The "connection_id" must be the ID of connection you need to use to generate video. You can't leave this
            empty, neither you can put a sample/example value here, or make up IDs out of your mind. If you don't have
            an available connection, don't use this.

            - The "query" field should be the prompt that you would like to generate the video based on.

            - The "action_type" must be the action type that you need to perform with video generation tool. You can
            choose one of the action types listed above. If you fail to provide a valid action type, the system will
            not be able to generate a video for you.

            - The "aspect_ratio" must be the aspect ratio that you need to use for video. This field is only required
            for the action types that require aspect ratio. Otherwise, you can skip this.

            - The "start_frame_url" must be the ABSOLUTE URL of the start frame you would like to use for the video.
            This field is only required for action types requiring a start frame. Otherwise, you can skip this. Don't
            provide relative URLs, always provide "absolute URLs".

            - The "end_frame_url" field must be the ABSOLUTE URL of the end frame you would like to use for the video.
            This field is only required for action types requiring an end frame. Otherwise, you can skip this. Don't
            provide relative URLs, always provide "absolute URLs".

            To use this, you need to be careful about following details:

            - [1] Never omit the 'connection_id' field, and always provide a valid connection ID.
            - [2] Always provide a valid 'action_type' in parameters field of tool_usage_json, don't make up action
                    types.
            - [3] Always provide 'prompt' field in parameters field of tool_usage_json.

                - These 3 fields are ALWAYS mandatory, and you need to provide them in parameters field of
                    tool_usage_json whatever action type you choose to use.

            - [4] If you are using an action type requiring an aspect ratio, always provide 'aspect_ratio' field in
            parameters field of tool_usage_json.

            - [5] If you are using an action type requiring a start frame, always provide 'start_frame_url' field in
            parameters field of tool_usage_json.

            - [6] If you are using an action type requiring an end frame, always provide 'end_frame_url' field in
            parameters field of tool_usage_json.

            ---

            #### **IMPORTANT NOTES:**

            - **NOTE**: The system will provide you the results in next 'assistant' message. This message will
            have the output of execution, and you will be expected to take this response and provide an answer
            to user's question based on response that you received, in your own words. Think of this as an employee
            you are instructing to execute a query on a media item, and you are expected to take the response of this
            employee and provide an answer to user's question.

            #### **ABOUT PROVIDING URLS & LINKS:**
            - If you need to provide a direct link to user for reaching files, here is the base
                URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP URL to file:
                - {MEDIA_URL}
            - **NEVER, EVER:** provide a 'relative' path to files. Always provide 'absolute' path by
            appending the file path to the base URL.

            ---

        """
    return response_prompt


def build_lean_tool_prompt__generate_video():
    response_prompt = f"""
            ### **TOOL**: Video Generation Tool

            - The Video Generation Tool is a tool allows you to generate videos based on prompts you provide.
            You can use this to generate videos based on prompts, and the tool assistant will generate
            a video based on prompt you provided. You can use this to generate videos for various use cases
            such as for creative use cases, for contents, and much more.

            - You CAN ONLY generate videos by using Video Generator Connections, and you will not be able to generate
            videos unless there is a valid connection available for you to use, since your JSON call requires the input
            of a connection_id field. If you don't have valid connections, don't attempt to generate videos. Below is
            the video generator connections you have. If you dont have any, it will look empty.

            #### *Video Generator Connections:*
            '''
            <This data is redacted because you won't need it to serve your instructions.>
            '''

            ---

            - After you decide on which connection to use (if any) to generate the videos, you need to define the
            action you want to perform on the video generation tool. The action types you can perform with video
            generation tool, and their **'action_type'** specifiers are as follows:

            - [1] Text to Video with Loop and Aspect Ratio -> {VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP_AND_ASPECT_RATIO}
            - [2] Text to Video with Loop -> {VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP}
            - [3] Text to Video with Aspect Ratio -> {VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_ASPECT_RATIO}
            - [4] Text to Video -> {VideoGenerationActionTypes.TEXT_TO_VIDEO}
            - [5] Text and Image to Video with Loop and with Start Frame -> {VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_LOOP_AND_WITH_START_FRAME}
            - [6] Text and Image to Video with Start Frame -> {VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_FRAME}
            - [7] Text and Image to Video with End Frame -> {VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_END_FRAME}
            - [8] Text and Image to Video with Start and End Frame -> {VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_AND_END_FRAME}

            ---

            - The format for dictionary you will output to use Video Generation Tool is as follows (where N, A, B are
                integers, and " symbols represents the variables which are strings):

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_GENERATE_VIDEO}",
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

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:**

            - The "connection_id" must be the ID of connection you need to use to generate video. You can't leave this
            empty, neither you can put a sample/example value here, or make up IDs out of your mind. If you don't have
            an available connection, don't use this.

            - The "query" field should be the prompt that you would like to generate the video based on.

            - The "action_type" must be the action type that you need to perform with video generation tool. You can
            choose one of the action types listed above. If you fail to provide a valid action type, the system will
            not be able to generate a video for you.

            - The "aspect_ratio" must be the aspect ratio that you need to use for video. This field is only required
            for the action types that require aspect ratio. Otherwise, you can skip this.

            - The "start_frame_url" must be the ABSOLUTE URL of the start frame you would like to use for the video.
            This field is only required for action types requiring a start frame. Otherwise, you can skip this. Don't
            provide relative URLs, always provide "absolute URLs".

            - The "end_frame_url" field must be the ABSOLUTE URL of the end frame you would like to use for the video.
            This field is only required for action types requiring an end frame. Otherwise, you can skip this. Don't
            provide relative URLs, always provide "absolute URLs".

            To use this, you need to be careful about following details:

            - [1] Never omit the 'connection_id' field, and always provide a valid connection ID.
            - [2] Always provide a valid 'action_type' in parameters field of tool_usage_json, don't make up action
                    types.
            - [3] Always provide 'prompt' field in parameters field of tool_usage_json.

                - These 3 fields are ALWAYS mandatory, and you need to provide them in parameters field of
                    tool_usage_json whatever action type you choose to use.

            - [4] If you are using an action type requiring an aspect ratio, always provide 'aspect_ratio' field in
            parameters field of tool_usage_json.

            - [5] If you are using an action type requiring a start frame, always provide 'start_frame_url' field in
            parameters field of tool_usage_json.

            - [6] If you are using an action type requiring an end frame, always provide 'end_frame_url' field in
            parameters field of tool_usage_json.

            ---

            #### **IMPORTANT NOTES:**

            - **NOTE**: The system will provide you the results in next 'assistant' message. This message will
            have the output of execution, and you will be expected to take this response and provide an answer
            to user's question based on response that you received, in your own words. Think of this as an employee
            you are instructing to execute a query on a media item, and you are expected to take the response of this
            employee and provide an answer to user's question.

            #### **ABOUT PROVIDING URLS & LINKS:**
            - If you need to provide a direct link to user for reaching files, here is the base
                URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP URL to file:
                - {MEDIA_URL}
            - **NEVER, EVER:** provide a 'relative' path to files. Always provide 'absolute' path by
            appending the file path to the base URL.

            ---

        """
    return response_prompt
