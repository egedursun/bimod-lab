#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: image_generator_executor.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: image_generator_executor.py
#  Last Modified: 2024-09-28 15:44:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:05:16
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import os
from uuid import uuid4

import boto3
import filetype
import requests

from apps._services.config.costs_map import ToolCostsMap
from apps._services.image_generation.utils.constant_utils import UNCLASSIFIED_FILE_EXTENSION
from apps._services.storages.utils import GENERATED_IMAGES_ROOT_PATH
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import TransactionSourcesNames
from config.settings import MEDIA_URL


class ImageGeneratorExecutor:
    def __init__(self, assistant, chat):
        self.assistant = assistant
        self.chat = chat

    def execute_generate_image(self, prompt, image_size, quality):
        from apps._services.llms.openai import InternalOpenAIClient
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
        try:
            openai_client = InternalOpenAIClient(
                assistant=self.assistant,
                multimodal_chat=self.chat)
            print(f"[ImageGeneratorExecutor.execute_generate_image] OpenAI client created successfully.")
        except Exception as e:
            print(f"[ImageGeneratorExecutor.execute_generate_image] Error occurred while creating the OpenAI client: {str(e)}")
            return None

        try:
            response = openai_client.generate_image(prompt=prompt, image_size=image_size, quality=quality)
            print(f"[ImageGeneratorExecutor.execute_generate_image] Image generation completed successfully.")
            if response["success"] is False:
                return response
        except Exception as e:
            print(f"[ImageGeneratorExecutor.execute_generate_image] Error occurred while generating the image: {str(e)}")
            return {"success": False, "message": "Error occurred while generating the image.", "image_url": None}

        if response["image_url"]:
            image_openai_url = response["image_url"]
            print(f"[ImageGeneratorExecutor.execute_generate_image] Image URL: {image_openai_url}")
            # download the image from the URL
            try:
                image_bytes = requests.get(image_openai_url).content
                print(f"[ImageGeneratorExecutor.execute_generate_image] Image downloaded successfully.")
            except Exception as e:
                print(f"[ImageGeneratorExecutor.execute_generate_image] Error occurred while downloading the image: {str(e)}")
                return {"success": False, "message": "Error occurred while downloading the image.", "image_url": None}

            try:
                transaction = LLMTransaction(
                    organization=self.chat.assistant.organization,
                    model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=self.chat.assistant,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    llm_cost=ToolCostsMap.ImageGenerator.COST,
                    transaction_type=ChatRoles.SYSTEM,
                    transaction_source=TransactionSourcesNames.GENERATE_IMAGE,
                    is_tool_cost=True
                )
                transaction.save()
                print(f"[ImageGeneratorExecutor.execute_generate_image] Transaction saved successfully.")
            except Exception as e:
                print(f"[ImageGeneratorExecutor.execute_generate_image] Error occurred while saving the transaction: {str(e)}")
                return {"success": False, "message": "Error occurred while saving the transaction.", "image_url": None}

            if image_bytes:
                image_uri = self.save_images_and_provide_full_uris([image_bytes])[0]
                return {"success": True, "message": "", "image_uri": image_uri}
        return {"success": False, "message": "Error occurred while downloading the image.", "image_url": None}

    @staticmethod
    def save_images_and_provide_full_uris(image_bytes_list):
        full_uris = []
        for image_bytes in image_bytes_list:
            try:
                full_uri = ImageGeneratorExecutor.save_image_and_provide_full_uri(image_bytes)
                if full_uri is not None:
                    full_uris.append(full_uri)
            except Exception as e:
                print(f"[ImageGeneratorExecutor.save_images_and_provide_full_uris] Error occurred while saving the image: {str(e)}")
        print(f"[ImageGeneratorExecutor.save_images_and_provide_full_uris] Full URIs: {full_uris}")
        return full_uris

    @staticmethod
    def save_image_and_provide_full_uri(image_bytes):
        guess_file_type = filetype.guess(image_bytes)
        if guess_file_type is None:
            guess_file_type = UNCLASSIFIED_FILE_EXTENSION
        extension = guess_file_type.extension
        save_name = ImageGeneratorExecutor.generate_save_name(extension=extension)
        s3_path = f"{GENERATED_IMAGES_ROOT_PATH}{save_name}"
        full_uri = f"{MEDIA_URL}{s3_path}"
        try:
            # Save the image to s3
            boto3_client = boto3.client('s3')
            bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
            boto3_client.put_object(Bucket=bucket_name, Key=s3_path, Body=image_bytes)
        except Exception as e:
            print(f"[ImageGeneratorExecutor.save_image_and_provide_full_uri] Error occurred while saving image: {str(e)}")
            return None
        print(f"[ImageGeneratorExecutor.save_image_and_provide_full_uri] Full URI: {full_uri}")
        return full_uri

    @staticmethod
    def generate_save_name(extension):
        try:
            generated_uuid = str(uuid4())
            additional_uuid = str(uuid4())
        except Exception as e:
            print(f"[ImageGeneratorExecutor.generate_save_name] Error occurred while generating the save name: {str(e)}")
            return None
        print(f"[ImageGeneratorExecutor.generate_save_name] Save name: {generated_uuid}_{additional_uuid}.{extension}")
        return f"{generated_uuid}_{additional_uuid}.{extension}"
