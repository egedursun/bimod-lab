#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: audio_processing_execution_tool_validator.py
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
#
#

from apps._services.audio_processing.utils import AudioProcessingExecutorActionsNames


def validate_audio_processing_execution_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Audio
            Processing Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "action" not in parameters:
        return """
            The 'action' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Audio Processing Execution tool. Please make sure you are defining the 'action' field in the parameters
            field of the tool_usage_json.
            """

    if parameters.get("action") not in AudioProcessingExecutorActionsNames.as_list():
        return f"""
            The 'action' field in the 'parameters' field of the tool_usage_json must be one of
             {AudioProcessingExecutorActionsNames.as_list()}. This field is mandatory for using the Audio
             Processing Execution tool. Please make sure you are defining the 'action' field in
            the parameters field of the tool_usage_json.
        """

    if parameters.get("action") == AudioProcessingExecutorActionsNames.TTS:
        if "text_content" not in parameters:
            return """
                The 'text_content' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
                for using the Audio Processing Execution tool with the action 'tts'. Please make sure you are defining the 'text_content' field in
                the parameters field of the tool_usage_json.
            """
        if "voice_selection" not in parameters:
            return """
                The 'voice_selection' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
                for using the Audio Processing Execution tool with the action 'tts'. Please make sure you are
                defining the 'voice_selection' field in the parameters field of the tool_usage_json.
            """
    elif parameters.get("action") == AudioProcessingExecutorActionsNames.STT:
        if "audio_file_path" not in parameters:
            return """
                The 'audio_file_path' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
                for using the Audio Processing Execution tool with the action 'stt'. Please make sure you are defining the 'audio_file_path' field in
                the parameters field of the tool_usage_json.
            """

    print(
        f"[audio_processing_execution_tool_validator.validate_audio_processing_execution_tool_json] Validation is successful.")
    return None
