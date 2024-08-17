import io
from pydub import AudioSegment
import requests
from openai import OpenAI

# Initialize OpenAI client
openai_api_key = 'sk-bloom-app-CAjHDM4W0FXLZlP5yVvgT3BlbkFJGeSaluzHcPr20animZV0'
client = OpenAI(api_key=openai_api_key)

# Load and process the audio file
audio_uri = "https://bimod-dev.s3.amazonaws.com/generated/files/6956b3d1-fa43-4997-9b33-6fe28eeaa79e_6959d4c9-f74b-4fcb-94bc-18974fb354bb.wav"
response = requests.get(audio_uri)
audio = AudioSegment.from_file(io.BytesIO(response.content), format="wav")

# Only use the first 5 minutes
audio = audio[:5 * 60_000]

# Export to buffer
buffer = io.BytesIO()
buffer.name = 'temp_audio.wav'  # It's important to have the right file extension
audio.export(buffer, format="wav")
buffer.seek(0)  # Important: reset buffer position to the start

# Transcribe audio
try:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=buffer
    )
    print(transcription.text)
except Exception as e:
    print(f"Error during transcription: {e}")
