from uuid import uuid4

import filetype
import requests

from apps._services.config.costs_map import ToolCostsMap
from apps._services.storages.storage_executor import GENERATED_IMAGES_ROOT_PATH
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames


class ImageGeneratorExecutor:

    def __init__(self, assistant, chat):
        self.assistant = assistant
        self.chat = chat

    def execute_generate_image(self, prompt, image_size, quality):
        from apps._services.llms.openai import InternalOpenAIClient
        try:
            openai_client = InternalOpenAIClient(
                assistant=self.assistant,
                multimodal_chat=self.chat)
        except Exception as e:
            print(f"Error occurred while creating the OpenAI client: {str(e)}")
            return None

        response = openai_client.generate_image(prompt=prompt,
                                                image_size=image_size,
                                                quality=quality)
        if response["success"] is False:
            return response

        if response["image_url"]:
            image_openai_url = response["image_url"]
            image_bytes = None
            # download the image from the URL
            try:
                image_bytes = requests.get(image_openai_url).content
            except Exception as e:
                print(f"Error occurred while downloading the image: {str(e)}")
                return {"success": False, "message": "Error occurred while downloading the image.", "image_url": None}

            transaction = LLMTransaction(
                organization=self.chat.assistant.organization,
                model=self.chat.assistant.llm_model,
                responsible_user=self.chat.user,
                responsible_assistant=self.chat.assistant,
                encoding_engine="cl100k_base",
                llm_cost=ToolCostsMap.ImageGenerator.COST,
                transaction_type="system",
                transaction_source=TransactionSourcesNames.GENERATE_IMAGE,
                is_tool_cost=True
            )
            transaction.save()

            if image_bytes:
                image_uri = self.save_images_and_provide_full_uris([image_bytes])[0]
                return {"success": True, "message": "", "image_uri": image_uri}

        return {"success": False, "message": "Error occurred while downloading the image.", "image_url": None}

    @staticmethod
    def save_images_and_provide_full_uris(image_bytes_list):
        full_uris = []
        for image_bytes in image_bytes_list:
            full_uri = ImageGeneratorExecutor.save_image_and_provide_full_uri(image_bytes)
            if full_uri is not None:
                full_uris.append(full_uri)
        return full_uris

    @staticmethod
    def save_image_and_provide_full_uri(image_bytes):
        guess_file_type = filetype.guess(image_bytes)
        if guess_file_type is None:
            guess_file_type = ".bin"
        extension = guess_file_type.extension
        save_name = ImageGeneratorExecutor.generate_save_name(extension=extension)
        full_uri = f"{GENERATED_IMAGES_ROOT_PATH}{save_name}"
        try:
            with open(full_uri, "wb") as image:
                image.write(image_bytes)
        except Exception as e:
            print(f"Error occurred while saving image: {str(e)}")
            return None
        return full_uri

    @staticmethod
    def generate_save_name(extension):
        generated_uuid = str(uuid4())
        additional_uuid = str(uuid4())
        return f"{generated_uuid}_{additional_uuid}.{extension}"
