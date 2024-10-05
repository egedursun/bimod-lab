#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
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
