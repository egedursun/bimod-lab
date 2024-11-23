#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: transcriber_executor.py
#  Last Modified: 2024-10-26 20:59:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-26 20:59:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import io
import json
import logging
import wave

from vosk import Model, KaldiRecognizer

from config.settings import VOSK_MODEL_PATH

logger = logging.getLogger(__name__)


class TranscriberExecutionManager:

    def __init__(self, model_path=VOSK_MODEL_PATH):

        try:
            self.model = Model(model_path)

        except Exception as e:
            logger.error(f"Failed to load Vosk model from path: {model_path}. Error: {e}")
            raise e

    def transcribe_audio(self, audio_data):

        transcription, error = "N/A", None

        # audio_data is a WAV file in bytes
        try:

            audio_stream = io.BytesIO(audio_data)
            with wave.open(audio_stream, "rb") as wf:

                if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                    error = "Audio file must be WAV format mono PCM."
                    logger.error(error)
                    return transcription, error

                recognizer = KaldiRecognizer(
                    self.model,
                    wf.getframerate()
                )

                transcription = []

                while True:
                    data = wf.readframes(4000)

                    if len(data) == 0:
                        break

                    if recognizer.AcceptWaveform(data):

                        result = recognizer.Result()
                        transcription.append(json.loads(result).get("text", ""))

                transcription.append(json.loads(recognizer.FinalResult()).get("text", ""))

        except Exception as e:
            logger.error(f"Failed to transcribe audio. Error: {e}")
            error = str(e)
            return "N/A", error

        final_transcription = " ".join(transcription)
        return final_transcription, None
