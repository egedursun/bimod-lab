#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: text_to_speech_mtest.py
#  Last Modified: 2024-08-17 19:46:50
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

from pathlib import Path
from openai import OpenAI

client = OpenAI(
    api_key=""
)


class OpenAITTSVoiceNames:
    ALLOY = "alloy"  # Male Speaker: Baritone
    ECHO = "echo"  # Male Speaker: Baritone-Bass
    FABLE = "fable"  # Male Speaker: Tenor
    ONYX = "onyx"  # Male Speaker: Bass
    NOVA = "nova"  # Female Speaker: Older and Wiser
    SHIMMER = "shimmer"  # Female Speaker: Younger and Energetic


model_name = "tts-1"
test_input_text = "Today is a wonderful day to build something people love!"
output_file_name = "speech.mp3"

speech_file_path = Path(__file__).parent / output_file_name
response = client.audio.speech.create(
    model=model_name,
    voice=OpenAITTSVoiceNames.ALLOY,
    input=test_input_text
)

response.stream_to_file(speech_file_path)
