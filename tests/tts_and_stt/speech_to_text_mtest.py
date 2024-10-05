#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: speech_to_text_mtest.py
#  Last Modified: 2024-10-03 12:42:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:37:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#

from openai import OpenAI


openai_api_key = '...'

client = OpenAI(
    api_key=openai_api_key
)

# audio_file_path = f"audio_test_files/human_voice.wav"
# audio_file_path = f"audio_test_files/human_voice_noisy.wav"
audio_file_path = f"audio_test_files/test_downloaded.wav"
model_name = "whisper-1"

audio_file = open(audio_file_path, "rb")
transcription = client.audio.transcriptions.create(
    model=model_name,
    file=audio_file
)

response_text = transcription.text
print(response_text)
