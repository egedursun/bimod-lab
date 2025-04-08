#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: video_generation_executor.py
#  Last Modified: 2024-10-05 02:31:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging
import os
import time

import filetype
import requests
import boto3

from apps.core.generative_ai.utils import (
    GPT_DEFAULT_ENCODING_ENGINE,
    ChatRoles
)

from apps.core.media_managers.utils import (
    GENERATED_VIDEOS_ROOT_MEDIA_PATH
)

from apps.llm_transaction.models import LLMTransaction

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames,
    LLMTokenTypesNames
)

from apps.video_generations.models import (
    VideoGeneratorConnection
)

from apps.core.video_generation.utils import (
    VideoGeneratorFrameTypes,
    LumaAIGenerationStates,
    VIDEO_GENERATOR_PING_INTERVAL_SECONDS,
    UNCLASSIFIED_FILE_EXTENSION,
    generate_save_name
)

from lumaai import LumaAI

from config.settings import MEDIA_URL

logger = logging.getLogger(__name__)


class VideoGenerationExecutor:
    def __init__(
        self,
        connection: VideoGeneratorConnection
    ):

        self.connection = connection

        try:
            self.client = LumaAI(
                auth_token=connection.provider_api_key
            )

        except Exception as e:
            logger.error(f"There was an error while initializing the LumaAI client: {e}")

    def _download_and_save_video(
        self,
        generation,
        video_url: str
    ):

        try:
            tx = LLMTransaction(
                organization=self.connection.assistant.organization,
                model=self.connection.assistant.llm_model,
                responsible_user=None,
                responsible_assistant=self.connection.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.GENERATE_VIDEO,
                is_tool_cost=True,
                llm_token_type=LLMTokenTypesNames.OUTPUT,
            )

            tx.save()

            logger.info(f"Transaction created for video generation: {tx.id}")

        except Exception as e:

            logger.error(f"Error occurred while saving the transaction: {e}")

            return {
                "success": False,
                "message": "Error occurred while saving the transaction.",
                "image_url": None
            }

        try:
            response = requests.get(
                video_url,
                stream=True
            )

            data_bytes = response.content

            logger.info(f"Downloaded video data from the URL: {video_url}")

        except Exception as e:
            logger.error(f"Error occurred while downloading the video data: {e}")
            return None

        estimated_format = filetype.guess(data_bytes)

        if estimated_format is None:
            logger.error("Could not determine the file type of the downloaded video.")
            estimated_format = UNCLASSIFIED_FILE_EXTENSION

        file_format = estimated_format.extension

        save_name = generate_save_name(
            extension=file_format
        )

        bucket_path = f"{GENERATED_VIDEOS_ROOT_MEDIA_PATH}{save_name}"
        full_uri = f"{MEDIA_URL}{bucket_path}"

        try:
            s3c = boto3.client('s3')
            bucket = os.getenv('AWS_STORAGE_BUCKET_NAME')
            s3c.put_object(
                Bucket=bucket,
                Key=bucket_path,
                Body=data_bytes
            )

            logger.info(f"Saved the video to the S3 bucket: {bucket_path}")

        except Exception as e:
            logger.error(f"Error occurred while saving the video to the S3 bucket: {e}")

            return None

        return full_uri

    ###############################################################################################################

    def text_to_video(
        self,
        query: str,
        loop=False,
        with_aspect_ratio=False,
        aspect_ratio=None
    ):

        generation = None

        if loop is True:

            if with_aspect_ratio is True:

                aspect_ratio = "3:4" if not aspect_ratio else aspect_ratio

                generation = self.client.generations.create(
                    prompt=query,
                    loop=True,
                    aspect_ratio=aspect_ratio
                )

            else:
                generation = self.client.generations.create(
                    prompt=query,
                    loop=True
                )
        else:

            if with_aspect_ratio is True:

                aspect_ratio = "3:4" if not aspect_ratio else aspect_ratio

                generation = self.client.generations.create(
                    prompt=query,
                    aspect_ratio=aspect_ratio
                )

            else:

                generation = self.client.generations.create(
                    prompt=query
                )

        completed = False

        while not completed:

            generation = self.client.generations.get(
                id=generation.id
            )

            completed = True if generation.state == LumaAIGenerationStates.COMPLETED else False

            if generation.state == LumaAIGenerationStates.FAILED:
                logger.error("The video generation process has failed on the client side.")

                return {
                    "error": "The video generation process has failed on the client side.",
                    "video_url": None
                }

            time.sleep(VIDEO_GENERATOR_PING_INTERVAL_SECONDS)

            logger.info(f"Video generation process is still running. State: {generation.state}")

        video_url = generation.assets.video

        s3_url = self._download_and_save_video(
            generation,
            video_url
        )

        logger.info(f"Video generation process completed successfully. Video URL: {s3_url}")

        return {
            "video_url": s3_url,
            "error": None
        }

    def text_and_image_to_video(
        self,
        query: str,
        start_frame_url: str = None,
        end_frame_url: str = None,
        frame_type: str = VideoGeneratorFrameTypes.START,
        loop=False
    ):

        if (
            start_frame_url is None and
            end_frame_url is None
        ):
            logger.error("At least one of the start or end frame URLs must be provided.")

            return {
                "error": "At least one of the start or end frame URLs must be provided.",
                "video_url": None
            }

        generation = None

        if frame_type == VideoGeneratorFrameTypes.START:

            if loop is True:

                generation = self.client.generations.create(
                    prompt=query,
                    loop=True,
                    keyframes={
                        "frame0": {
                            "type": "image",
                            "url": start_frame_url
                        }
                    }
                )

            else:

                generation = self.client.generations.create(
                    prompt=query,
                    keyframes={
                        "frame0": {
                            "type": "image",
                            "url": start_frame_url
                        }
                    }
                )

        elif frame_type == VideoGeneratorFrameTypes.END:

            generation = self.client.generations.create(
                prompt=query,
                keyframes={
                    "frame1": {
                        "type": "image",
                        "url": end_frame_url
                    }
                }
            )

        elif frame_type == VideoGeneratorFrameTypes.START_AND_END:

            generation = self.client.generations.create(
                prompt=query,
                keyframes={
                    "frame0": {
                        "type": "image",
                        "url": start_frame_url
                    },
                    "frame1": {
                        "type": "image",
                        "url": end_frame_url
                    }
                }
            )

        completed = False

        while not completed:

            generation = self.client.generations.get(
                id=generation.id
            )

            completed = True if generation.state == LumaAIGenerationStates.COMPLETED else False

            if generation.state == LumaAIGenerationStates.FAILED:
                return {
                    "error": "The video generation process has failed on the client side.",
                    "video_url": None
                }

            time.sleep(VIDEO_GENERATOR_PING_INTERVAL_SECONDS)

        video_url = generation.assets.video

        s3_url = self._download_and_save_video(
            generation,
            video_url
        )

        logger.info(f"Video generation process completed successfully. Video URL: {s3_url}")

        return {
            "video_url": s3_url,
            "error": None
        }
