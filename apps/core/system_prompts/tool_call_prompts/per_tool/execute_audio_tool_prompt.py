#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#


from apps.core.tool_calls.utils import ToolCallDescriptorNames
from config.settings import MEDIA_URL


def build_tool_prompt__execute_audio():
    response_prompt = f"""
            ### **TOOL**: Audio Processing Tool

            - The Audio Processing Tool is a tool allows you to execute audio processing operations on audio files.
            You can use this to do text to speech (TTS), speech to text (STT) operations on either texts within the
            context of conversations with users, or for specific, valid files users have in their storages or other
            possible data sources. For example, the user can ask you to convert a certain text into an audio file, or
            can share a text file to be converted to an audio file. Or, user might ask to convert an audio file they
            have shared into a transcription. Or, the users can send their own recorded voice in form of audio files
            for you to convert them into textual transcriptions.

            - The format for the dictionary you will output to use Audio Processing Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_PROCESS_AUDIO}",
                    "parameters": {{
                        "action": "tts" | "stt",
                        "audio_file_path": "...",  # Required if action is 'stt', must be empty if action is 'tts'
                        "text_content": "..."  # Required if action is 'tts', must be empty if action is 'stt'
                        "voice_selection": "alloy" | "echo" | "fable" | "onyx" | "nova" | "shimmer"  # Required if action is 'tts', must be empty if action is 'stt'
                    }}
                }}
            '''

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** The "action" field must be either "tts" or "stt". If action is "tts", you need to
            provide "text_content" field with the text content you need to convert to an audio file. If the action is
            "stt", you need to provide the "audio_file_path" with the path of audio file you need to convert to text
            content. You must provide the "audio_file_path" as an empty string if the action is "tts", and you must
            provide "text_content" as an empty string if the action is "stt".

            To use this tool, you need to provide following fields 'VERY CAREFULLY':

            - [1] For "action", provide either "tts" or "stt" based on the operation you need to execute.

            - [2] For "audio_file_path", provide the path of audio file you need to convert to text content.
                You must fill this field if the action you choose is "stt". If the action is "tts", you must provide
                an empty string for this, or you can leave it empty.

                - **IMPORTANT NOTE:** The path MUST ALWAYS be an "ABSOLUTE URI" to file, NOT a "relative path".
                  **ASSERTING AGAIN:** The path MUST ALWAYS be an "ABSOLUTE URI" to the file, NOT a "relative path".

            - [3] For "text_content", provide the text content you need to convert to an audio file. You must fill
                this if the action you choose is "tts". If the action is "stt", you can provide an empty string
                for this, or leave it empty.

            - [4] For "voice_selection", provide the voice type that you need to use for text-to-speech operation.
            THIS IS A MANDATORY FIELD if the action is "tts". If the action is "stt", you must provide an empty
            string for this, or leave it empty.

                - #### **AVAILABLE VOICE TYPES:**
                    - "alloy": The speaker is a "Male Speaker" with vocal style/range in "Baritone"..
                    - "echo":  The speaker is a "Male Speaker" with vocal style/range in "Baritone-Bass".
                    - "fable": The speaker is a "Male Speaker" with vocal style/range in "Tenor".
                    - "onyx":  The speaker is a "Male Speaker" with vocal style/range in "Bass".
                    - "nova":  The speaker is a "Female Speaker" with vocal style/range in "Older and Wiser".
                    - "shimmer": The speaker is a "Female Speaker" with vocal style/range in "Younger and Energetic".

                - *NOTE:* If user specifies a certain expectation about voice style, you can choose the voice type
                            you think would be the best fit for user's expectation.

            ---

            - **IMPORTANT NOTES:**

                - For audio interpretations, you will receive the output in a single response containing a string,
                which will include a message to tell you (if there is) errors during the process, and another field to
                provide you the path of the generated audio. If the process is not successful, you will receive an
                message to inform you about the error.

            - **NOTE**: The system will provide you the results in the next 'assistant' message. This message will
            have the output of the execution, and you will be expected to take this and provide an answer to user's
            question based on the response you receive, in your own words. Think of this as an employee of yours, that
            you are instructing to execute a query on an audio file, and you are expected to take the response of the
            employee and provide an answer to user's question based on it.

            #### **ABOUT PROVIDING URLS & LINKS:**

                - If you need to provide a direct link to user for reaching files, here is the base
                    URL you need to 'DIRECTLY' append the file path to provide an absolute HTTP URL to file:
                    - {MEDIA_URL}

                - **NEVER, EVER:** provide a 'relative' path or URL to files. Always provide 'absolute' path by
                appending file path to the base URL.

        """
    return response_prompt
