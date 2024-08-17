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
