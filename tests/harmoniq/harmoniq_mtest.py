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


import asyncio
import websockets
import json
import base64

# Replace with your OpenAI API key
API_KEY = "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"

# Path to your audio file
AUDIO_FILE_PATH = 'test_audio.mp3'

# Output file for the assistant's audio response
OUTPUT_AUDIO_FILE = 'response_audio.ogg'


async def connect_and_interact():
    # WebSocket connection parameters
    url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "OpenAI-Beta": "realtime=v1"
    }

    async with websockets.connect(url, extra_headers=headers) as websocket:
        print("Connected to the OpenAI Realtime API.")

        # Prepare and send the user's audio message
        event_json = audio_to_item_create_event(AUDIO_FILE_PATH)
        await websocket.send(event_json)
        print("Sent audio message to the API.")

        # Send response.create event to prompt assistant to respond
        response_event = {
            "type": "response.create",
            "response": {
                "modalities": ["audio", "text"],
                "instructions": "Please assist the user."
            }
        }
        await websocket.send(json.dumps(response_event))
        print("Sent response.create event to the API.")

        # Collect audio chunks from the assistant's response
        audio_base64_list = []

        while True:
            try:
                message = await websocket.recv()
                event = json.loads(message)
                event_type = event.get('type')

                # Handle different event types
                if event_type == 'response.audio.delta':
                    # Collect base64-encoded audio data
                    audio_data_base64 = event.get('audio', {}).get('audio')
                    if audio_data_base64:
                        audio_base64_list.append(audio_data_base64)
                elif event_type == 'response.audio.done':
                    # Audio response is complete
                    print("Audio response received from the API.")
                    # Save the audio response
                    save_audio_response(audio_base64_list, OUTPUT_AUDIO_FILE)
                    print(f"Assistant's audio response saved to {OUTPUT_AUDIO_FILE}.")
                    break  # Exit the loop after receiving the full response
                elif event_type == 'error':
                    error = event.get('error', {})
                    print("Error:", error.get('message'))
                    break
                else:
                    # Handle other events if needed
                    pass
            except websockets.exceptions.ConnectionClosed:
                print("WebSocket connection closed.")
                break


def audio_to_item_create_event(file_path):
    with open(file_path, 'rb') as f:
        audio_bytes = f.read()

    # Load the audio file from the byte stream
    from pydub import AudioSegment
    import io

    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

    # Resample to 24kHz mono PCM16
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


def save_audio_response(audio_base64_list, output_file):
    # Concatenate all base64 strings
    full_audio_base64 = ''.join(audio_base64_list)

    # Decode base64 to bytes
    full_audio_bytes = base64.b64decode(full_audio_base64)

    # Save bytes directly to an .ogg file
    with open(output_file, 'wb') as f:
        f.write(full_audio_bytes)


if __name__ == "__main__":
    # For Windows compatibility
    import sys

    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(connect_and_interact())
    except Exception as e:
        print("An error occurred:", e)
