#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: core_service_process_audio.py
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


from apps.core.audio_processing.audio_processing_executor import AudioProcessingExecutor
from apps.core.audio_processing.utils import RunAudioProcessingActionTypesNames
from apps.assistants.models import Assistant
from apps.multimodal_chat.models import MultimodalChat


def run_process_audio(agent_id, chat_id, process_audio_action_type, audio_uri=None, txt_data=None,
                      llm_voice_type=None):
    agent = Assistant.objects.get(id=agent_id)
    chat = MultimodalChat.objects.get(id=chat_id)
    xc = AudioProcessingExecutor(assistant=agent, chat=chat)
    if process_audio_action_type == RunAudioProcessingActionTypesNames.TTS:
        output = xc.convert_text_to_audio_file(text_content=txt_data, voice_selection=llm_voice_type)
    elif process_audio_action_type == RunAudioProcessingActionTypesNames.STT:
        output = xc.convert_audio_to_text(audio_file_path=audio_uri)
    else:
        output = None
    return output
