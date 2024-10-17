#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: verify_audio_processing_query.py
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


from apps.core.audio_processing.utils import RunAudioProcessingActionTypesNames


def verify_audio_processing_query(content: dict):
    if "parameters" not in content:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Audio
            Processing Execution tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    ps = content.get("parameters")

    if "action" not in ps:
        return """
            The 'action' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Audio Processing Execution tool. Please make sure you are defining the 'action' field in the parameters
            field of the tool_usage_json.
            """

    if ps.get("action") not in RunAudioProcessingActionTypesNames.as_list():
        return f"""
            The 'action' field in the 'parameters' field of the tool_usage_json must be one of
             {RunAudioProcessingActionTypesNames.as_list()}. This field is mandatory for using the Audio
             Processing Execution tool. Please make sure you are defining the 'action' field in
            the parameters field of the tool_usage_json.
        """

    if ps.get("action") == RunAudioProcessingActionTypesNames.TTS:
        if "text_content" not in ps:
            return """
                The 'text_content' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
                for using the Audio Processing Execution tool with the action 'tts'. Please make sure you are defining the 'text_content' field in
                the parameters field of the tool_usage_json.
            """
        if "voice_selection" not in ps:
            return """
                The 'voice_selection' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
                for using the Audio Processing Execution tool with the action 'tts'. Please make sure you are
                defining the 'voice_selection' field in the parameters field of the tool_usage_json.
            """
    elif ps.get("action") == RunAudioProcessingActionTypesNames.STT:
        if "audio_file_path" not in ps:
            return """
                The 'audio_file_path' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
                for using the Audio Processing Execution tool with the action 'stt'. Please make sure you are defining the 'audio_file_path' field in
                the parameters field of the tool_usage_json.
            """
    return None
