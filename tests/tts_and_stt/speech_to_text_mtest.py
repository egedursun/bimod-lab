
from openai import OpenAI
client = OpenAI()

audio_file_path = f"..."
model_name = "whisper-1"

audio_file= open(audio_file_path, "rb")
transcription = client.audio.transcriptions.create(
  model=model_name,
  file=audio_file
)

response_text = transcription.text
print(response_text)
