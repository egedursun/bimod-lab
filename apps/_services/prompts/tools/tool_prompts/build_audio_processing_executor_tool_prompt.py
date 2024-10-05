#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: build_audio_processing_executor_tool_prompt.py
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
#
#

from apps._services.tools.utils import ToolTypeNames
from config.settings import MEDIA_URL


def build_structured_tool_prompt__audio_processing():
    response_prompt = f"""
            **TOOL**: Audio Processing Tool

            - The Audio Processing Tool is a tool that allows you to execute audio processing operations on audio files.
            You can use this tool to convert text to speech (TTS) and speech to text (STT) on either texts within the
            context of the conversations with the users, or for the specific, valid files the users have in their
            storages or other data sources. For example, the user might ask you to convert a certain message text into
            an audio file, or can share a text file with you to convert that text file to an audio file as well. On
            another scenario, the user might ask you to convert an audio file that they have shared with you into text
            content. Similarly, the users can send their own recorded voice in the form of audio files to you to convert
            them into text content.

            - The standardized format for the dictionary that you will output to use the Audio Processing Tool is as follows:

            '''
                {{
                    "tool": "{ToolTypeNames.AUDIO_PROCESSING}",
                    "parameters": {{
                        "action": "tts" | "stt",
                        "audio_file_path": "...",  # Required if action is 'stt', must be empty if action is 'tts'
                        "text_content": "..."  # Required if action is 'tts', must be empty if action is 'stt'
                        "voice_selection": "alloy" | "echo" | "fable" | "onyx" | "nova" | "shimmer"  # Required if action is 'tts', must be empty if action is 'stt'
                    }}
                }}
            '''

            **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            **INSTRUCTIONS:** The "action" field should be either "tts" or "stt". If the action is "tts", you need to
            provide the "text_content" field with the text content that you would like to convert to an audio file. If the
            action is "stt", you need to provide the "audio_file_path" field with the path of the audio file that you would
            like to convert to text content. You must provide the "audio_file_path" field as an empty string if the action
            is "tts", and you must provide the "text_content" field as an empty string if the action is "stt".

            To use this tool, you need to provide the following field 'VERY CAREFULLY':

            1. For "action", provide either "tts" or "stt" based on the operation that you would like to execute.

            2. For "audio_file_path", provide the path of the audio file that you would like to convert to text content.
                You must fill this field if the action you have chosen is "stt". If the action is "tts", you must provide
                an empty string for this field, or simply leave it empty.
                - **IMPORTANT NOTE:** The path MUST ALWAYS be an "ABSOLUTE URI" to the file, NOT a relative path.
                    ASSERTING AGAIN: The path MUST ALWAYS be an "ABSOLUTE URI" to the file, NOT a relative path.
                    ASSERTING ONE MORE TIME: The path MUST ALWAYS be an "ABSOLUTE URI" to the file, NOT a relative path.

            3. For "text_content", provide the text content that you would like to convert to an audio file. You must fill
                this field if the action you have chosen is "tts". If the action is "stt", you must provide an empty string
                for this field, or simply leave it empty.

            4. For "voice_selection", provide the voice selection that you would like to use for the text-to-speech
            operation. THIS IS A MANDATORY FIELD if the action is "tts". If the action is "stt", you must provide an empty
            string for this field, or simply leave it empty.

            **AVAILABLE VOICES:**
            - "alloy": The speaker is a "Male Speaker" with vocal style/range in "Baritone"..
            - "echo":  The speaker is a "Male Speaker" with vocal style/range in "Baritone-Bass".
            - "fable": The speaker is a "Male Speaker" with vocal style/range in "Tenor".
            - "onyx":  The speaker is a "Male Speaker" with vocal style/range in "Bass".
            - "nova":  The speaker is a "Female Speaker" with vocal style/range in "Older and Wiser".
            - "shimmer": The speaker is a "Female Speaker" with vocal style/range in "Younger and Energetic".

                *NOTE:* If the user specifies a certain expectation about the voice style, you can choose the voice
                that you think would be the best fit for the user's expectation.

            ---

            **IMPORTANT NOTES:**

            - For audio interpretations, you will receive the output in a single response containing a string, which
            will include a message to tell you about the possible errors during the process, and another field to
            provide you with the path of the generated audio file. If the process is successful, you will receive the
            path of the generated audio file, and if the process is not successful, you will receive an error message
            to inform you about the issue.

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
