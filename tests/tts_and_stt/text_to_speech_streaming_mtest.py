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


"""
Supported Output Formats:
=========================
- Opus,
- AAC,
- FLAC,
- WAV,
- PCM
"""

"""
Supported Languages
===================
Afrikaans, Arabic, Armenian, Azerbaijani,
Belarusian, Bosnian, Bulgarian,
Catalan, Chinese, Croatian, Czech,
Danish, Dutch,
English, Estonian,
Finnish, French,
Galician, German, Greek,
Hebrew, Hindi, Hungarian,
Icelandic, Indonesian, Italian,
Japanese, Kannada, Kazakh, Korean,
Latvian, Lithuanian,
Macedonian, Malay, Marathi, Maori,
Nepali, Norwegian,
Persian, Polish, Portuguese,
Romanian, Russian,
Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish,
Tagalog, Tamil, Thai, Turkish,
Ukrainian, Urdu,
Vietnamese,
Welsh
"""

model_name = "tts-1"
test_input_text = "Today is a wonderful day to build something people love!"
output_file_name = "speech.mp3"

response = client.audio.speech.create(
    model=model_name,
    voice=OpenAITTSVoiceNames.ALLOY,
    input=test_input_text
)

response.stream_to_file(output_file_name)
