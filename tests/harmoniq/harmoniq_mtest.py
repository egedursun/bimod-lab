#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: harmoniq_mtest.py
#  Last Modified: 2024-10-05 15:32:33
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 20:28:24
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

import base64
import io
import json
from pydub import AudioSegment


def audio_to_item_create_event(audio_bytes: bytes) -> str:
    # Load the audio file from the byte stream
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

    # Resample to 24kHz mono pcm16
    pcm_audio = audio.set_frame_rate(24000).set_channels(1).set_sample_width(2).raw_data

    # Encode to base64 string
    pcm_base64 = base64.b64encode(pcm_audio).decode()

    event = {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [{
                "type": "input_audio",
                "audio": pcm_base64
            }]
        }
    }
    return json.dumps(event)


def retrieve_llm_response(event):
    pass


if __name__ == "__main__":
    with open("test_audio.mp3", "rb") as f:
        audio_bytes = f.read()
        event = audio_to_item_create_event(audio_bytes=audio_bytes)
        print(event)
