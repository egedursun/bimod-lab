#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: video_generation_executor.py
#  Last Modified: 2024-10-01 16:59:44
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-10-01 16:59:45
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#
import os
import time

import filetype
import requests
import boto3

from apps._services.config.costs_map import ToolCostsMap
from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE, ChatRoles
from apps._services.storages.utils import GENERATED_VIDEOS_ROOT_PATH
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import TransactionSourcesNames
from apps.video_generations.models import VideoGeneratorConnection, GeneratedVideo
from apps._services.video_generation.utils import VideoGeneratorFrameTypes, LumaAIGenerationStates, \
    VIDEO_GENERATOR_PING_INTERVAL_SECONDS, UNCLASSIFIED_FILE_EXTENSION, generate_save_name
from lumaai import LumaAI

from config.settings import MEDIA_URL


class VideoGenerationExecutor:
    def __init__(self, connection: VideoGeneratorConnection):
        self.connection = connection
        try:
            self.client = LumaAI(auth_token=connection.provider_api_key)
        except Exception as e:
            print("[VideoGenerationExecutor.__init__]: There was an error while initializing the LumaAI client: ", e)

    def _download_and_save_video(self, generation, video_url: str):

        try:
            transaction = LLMTransaction(
                organization=self.connection.assistant.organization,
                model=self.connection.assistant.llm_model,
                responsible_user=None,
                responsible_assistant=self.connection.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=ToolCostsMap.VideoGenerator.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=TransactionSourcesNames.GENERATE_VIDEO,
                is_tool_cost=True
            )
            transaction.save()
            print(f"[ImageGeneratorExecutor.execute_generate_image] Transaction saved successfully.")
        except Exception as e:
            print(
                f"[ImageGeneratorExecutor.execute_generate_image] Error occurred while saving the transaction: {str(e)}")
            return {"success": False, "message": "Error occurred while saving the transaction.", "image_url": None}

        # Download the video
        try:
            response = requests.get(video_url, stream=True)
            data_bytes = response.content
            print(f"[VideoGenerationExecutor._download_and_save_video]: Video is downloaded successfully.")
        except Exception as e:
            print(f"[VideoGenerationExecutor._download_and_save_video] Error occurred while downloading the video: {str(e)}")
            return None

        # Save the video to S3 bucket
        guess_file_type = filetype.guess(data_bytes)
        if guess_file_type is None:
            guess_file_type = UNCLASSIFIED_FILE_EXTENSION
        extension = guess_file_type.extension
        save_name = generate_save_name(extension=extension)
        s3_path = f"{GENERATED_VIDEOS_ROOT_PATH}{save_name}"
        full_uri = f"{MEDIA_URL}{s3_path}"
        try:
            # Save the video to S3
            boto3_client = boto3.client('s3')
            bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
            boto3_client.put_object(Bucket=bucket_name, Key=s3_path, Body=data_bytes)
        except Exception as e:
            print(
                f"[VideoGenerationExecutor._download_and_save_video] Error occurred while saving the video to S3: {str(e)}")
            return None
        print(f"[VideoGenerationExecutor._download_and_save_video]: Video is saved to S3 successfully.")
        return full_uri

    ###############################################################################################################

    def text_to_video(self, query: str, loop=False, with_aspect_ratio=False, aspect_ratio=None):
        generation = None
        if loop is True:
            if with_aspect_ratio is True:
                aspect_ratio = "3:4" if not aspect_ratio else aspect_ratio
                generation = self.client.generations.create(prompt=query, loop=True, aspect_ratio=aspect_ratio)
            else:
                generation = self.client.generations.create(prompt=query, loop=True)
        else:
            if with_aspect_ratio is True:
                # CALL: Text to video, with aspect ratio
                aspect_ratio = "3:4" if not aspect_ratio else aspect_ratio
                generation = self.client.generations.create(prompt=query, aspect_ratio=aspect_ratio)
            else:
                # CALL: Text to video
                generation = self.client.generations.create(prompt=query)

        completed = False
        while not completed:
            generation = self.client.generations.get(id=generation.id)
            completed = True if generation.state == LumaAIGenerationStates.COMPLETED else False
            if generation.state == LumaAIGenerationStates.FAILED:
                print("[VideoGenerationExecutor.text_to_video]: Client video generation failed.")
                return {
                    "error": "The video generation process has failed on the client side.",
                    "video_url": None
                }
            time.sleep(VIDEO_GENERATOR_PING_INTERVAL_SECONDS)

        print("[VideoGenerationExecutor.text_to_video]: LumaAI video generation completed.")
        video_url = generation.assets.video

        # Download and save the video, and get the S3 URL
        print("[VideoGenerationExecutor.text_to_video]: Downloading and saving the video.")
        s3_url = self._download_and_save_video(generation, video_url)
        print("[VideoGenerationExecutor.text_to_video]: Video is downloaded and saved successfully.")
        return {
            "video_url": s3_url,
            "error": None
        }

    def text_and_image_to_video(self, query: str, start_frame_url: str = None, end_frame_url: str = None,
                                frame_type: str = VideoGeneratorFrameTypes.START, loop=False):
        if start_frame_url is None and end_frame_url is None:
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
                        "frame0":
                            {
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
            generation = self.client.generations.get(id=generation.id)
            completed = True if generation.state == LumaAIGenerationStates.COMPLETED else False
            if generation.state == LumaAIGenerationStates.FAILED:
                print("[VideoGenerationExecutor.text_to_video]: LumaAI video generation failed.")
                return {
                    "error": "The video generation process has failed on the client side.",
                    "video_url": None
                }
            time.sleep(VIDEO_GENERATOR_PING_INTERVAL_SECONDS)

        print("[VideoGenerationExecutor.text_to_video]: Client video generation completed.")
        video_url = generation.assets.video

        # Download and save the video, and get the S3 URL
        print("[VideoGenerationExecutor.text_to_video]: Downloading and saving the video.")
        s3_url = self._download_and_save_video(generation, video_url)
        print("[VideoGenerationExecutor.text_to_video]: Video is downloaded and saved successfully.")
        return {
            "video_url": s3_url,
            "error": None
        }
