#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auxiliary_tts_client.py
#  Last Modified: 2024-10-09 00:56:02
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 00:56:02
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
import logging
import mimetypes
import os
from pathlib import Path

import boto3
import requests
from openai import OpenAI

from apps.core.generative_ai.auxiliary_methods.errors.error_log_prompts import (
    get_audio_reading_error_log,
    get_audio_upload_error_log,
    get_audio_generation_error_log,
    get_audio_transcription_error_log
)

from apps.core.generative_ai.utils import (
    OpenAITTSVoiceNames,
    generate_random_audio_filename,
    TTS_MODEL_NAME,
    TTS_RETRY_REMOVAL,
    DEFAULT_AUDIO_MIME_TYPE,
    STT_MODEL_NAME
)

from apps.core.media_managers.utils import GENERATED_FILES_ROOT_MEDIA_PATH
from config.settings import MEDIA_URL, AWS_STORAGE_BUCKET_NAME

logger = logging.getLogger(__name__)


class AuxiliaryLLMAudioClient:

    def __init__(
        self,
        assistant,
        chat_object
    ):
        self.assistant = assistant
        self.chat = chat_object
        self.connection = OpenAI(
            api_key=assistant.llm_model.api_key
        )

    def tts_audio_content_message(
        self,
        message,
        extension="mp3",
        voice=OpenAITTSVoiceNames.ONYX
    ):
        final_output = {
            "success": False,
            "message": "",
            "audio_url": ""
        }
        msg_output = message.message_text_content

        try:
            model_name = TTS_MODEL_NAME
            output_name = generate_random_audio_filename(
                extension=extension
            )

            bucket_path = f"{GENERATED_FILES_ROOT_MEDIA_PATH}{output_name}"
            uri = f"{MEDIA_URL}{bucket_path}"
            temporary_path = os.path.join(str(Path(__file__).parent.parent), "tmp", output_name)

            c_data = self.connection.audio.speech.create(
                model=model_name,
                voice=voice, input=msg_output
            )
            c_data.stream_to_file(temporary_path)

            try:
                with open(temporary_path, "rb") as f:
                    audio_data = f.read()
                logger.info(f"Retrieved audio content from: {temporary_path}")

            except Exception as e:
                logger.error(f"Failed to read audio content from: {temporary_path}")
                final_output["message"] = get_audio_reading_error_log(error_logs=str(e))
                return final_output

            try:
                s3 = boto3.client('s3')
                s3.put_object(
                    Bucket=AWS_STORAGE_BUCKET_NAME,
                    Key=bucket_path,
                    Body=audio_data
                )
                logger.info(f"Uploaded audio content to: {bucket_path}")

            except Exception as e:
                logger.error(f"Failed to upload audio content to: {bucket_path}")
                final_output["message"] = get_audio_upload_error_log(error_logs=str(e))
                return final_output

        except Exception as e:
            logger.error(f"Failed to generate audio content: {e}")
            final_output["message"] = get_audio_generation_error_log(error_logs=str(e))
            return final_output

        for i in range(0, TTS_RETRY_REMOVAL, 1):
            try:
                os.remove(temporary_path)
                logger.info(f"Removed temporary audio content: {temporary_path}")
                break

            except Exception as e:
                logger.error(f"Failed to remove temporary audio content: {temporary_path}")
                continue

        final_output["success"] = True
        final_output["audio_url"] = uri
        return final_output

    def transform_text_to_speech(
        self,
        text_content,
        extension="mp3",
        voice=OpenAITTSVoiceNames.ONYX
    ):
        final_output = {
            "success": False,
            "message": "",
            "audio_url": ""
        }

        try:
            model_name = TTS_MODEL_NAME
            output_name = generate_random_audio_filename(
                extension=extension
            )

            bucket_path = f"{GENERATED_FILES_ROOT_MEDIA_PATH}{output_name}"
            uri = f"{MEDIA_URL}{bucket_path}"
            temporary_path = os.path.join(str(Path(__file__).parent.parent), "tmp", output_name)

            c_data = self.connection.audio.speech.create(
                model=model_name,
                voice=voice,
                input=text_content
            )
            c_data.stream_to_file(temporary_path)

            try:
                with open(temporary_path, "rb") as f:
                    audio_bytes = f.read()
                logger.info(f"Retrieved audio content from: {temporary_path}")

            except Exception as e:
                logger.error(f"Failed to read audio content from: {temporary_path}")
                final_output["message"] = get_audio_reading_error_log(error_logs=str(e))
                return final_output

            try:
                s3 = boto3.client('s3')
                s3.put_object(
                    Bucket=AWS_STORAGE_BUCKET_NAME,
                    Key=bucket_path,
                    Body=audio_bytes
                )
                logger.info(f"Uploaded audio content to: {bucket_path}")

            except Exception as e:
                logger.error(f"Failed to upload audio content to: {bucket_path}")
                final_output["message"] = get_audio_upload_error_log(error_logs=str(e))
                return final_output

        except Exception as e:
            logger.error(f"Failed to generate audio content: {e}")
            final_output["message"] = get_audio_generation_error_log(error_logs=str(e))
            return final_output

        for i in range(0, TTS_RETRY_REMOVAL, 1):
            try:
                os.remove(temporary_path)
                logger.info(f"Removed temporary audio content: {temporary_path}")
                break

            except Exception as e:
                logger.error(f"Failed to remove temporary audio content: {temporary_path}")
                continue

        final_output["success"] = True
        final_output["audio_url"] = uri
        return final_output

    def transform_speech_to_text(self, audio_uri: str):
        final_output = {
            "success": False,
            "message": "",
            "text": ""
        }

        try:
            http_audio_file = requests.get(audio_uri)
            mime_type, _ = mimetypes.guess_type(audio_uri)

            if not mime_type:
                mime_type = DEFAULT_AUDIO_MIME_TYPE

            f_sound_data = io.BytesIO(http_audio_file.content)
            f_sound_data.name = audio_uri.split('/')[-1]
            logger.info(f"Retrieved audio content from: {audio_uri}")

        except Exception as e:
            logger.error(f"Failed to read audio content from: {audio_uri}")
            final_output["message"] = get_audio_reading_error_log(error_logs=str(e))
            return final_output

        try:
            model_name = STT_MODEL_NAME
            transcription = self.connection.audio.transcriptions.create(
                model=model_name,
                file=f_sound_data
            )
            final_output["success"] = True
            final_output["text"] = transcription.text

        except Exception as e:
            logger.error(f"Failed to transcribe audio content: {e}")
            final_output["message"] = get_audio_transcription_error_log(error_logs=str(e))
            return final_output

        logger.info(f"Transcribed audio content: {audio_uri}")
        return final_output
