from openai import OpenAI

client = OpenAI(
    api_key=""
)

audio_file_path = f"some_german_speaking_file.mp3"
model_name = "whisper-1"

"""
Supported Languages for Translation + Transcription:
===================================================
Afrikaans, Arabic, Armenian, Azerbaijani,
Belarusian, Bosnian, Bulgarian,
Catalan, Chinese, Croatian, Czech,
Danish, Dutch,
English, Estonian,
Finnish, French,
Galician, German, Greek,
Hebrew, Hindi, Hungarian,
Icelandic, Indonesian, Italian,
Japanese,
Kannada, Kazakh, Korean,
Latvian, Lithuanian,
Macedonian, Malay, Marathi, Maori,
Nepali, Norwegian,
Persian, Polish, Portuguese,
Romanian, Russian,
Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish,
Tagalog, Tamil, Thai, Turkish,
Ukrainian, Urdu,
Vietnamese,
Welsh.
"""

audio_file = open("/path/to/file/german.mp3", "rb")
translation = client.audio.translations.create(
    model=model_name,
    file=audio_file
)

translated_transcribed_text = translation.text
print(translated_transcribed_text)
