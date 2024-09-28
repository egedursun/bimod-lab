import os
from uuid import uuid4

import boto3
import filetype
import requests

from apps._services.config.costs_map import ToolCostsMap
from apps._services.image_generation.utils import UNCLASSIFIED_FILE_EXTENSION
from apps._services.ml_models.utils import GENERATED_IMAGES_ROOT_PATH
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import TransactionSourcesNames
from config.settings import MEDIA_URL


class ImageModificationExecutor:
    def __init__(self, assistant, chat):
        self.assistant = assistant
        self.chat = chat

    def execute_modify_image(self, prompt, edit_image_uri, edit_image_mask_uri, image_size):
        from apps._services.llms.openai import InternalOpenAIClient
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
        try:
            openai_client = InternalOpenAIClient(assistant=self.assistant, multimodal_chat=self.chat)
            print(f"[ImageModificationExecutor.execute_modify_image] OpenAI client created successfully.")
        except Exception as e:
            print(
                f"[ImageModificationExecutor.execute_modify_image] Error occurred while creating the OpenAI client: {str(e)}")
            return None

        try:
            response = openai_client.edit_image(prompt=prompt, edit_image_uri=edit_image_uri,
                                                edit_image_mask_uri=edit_image_mask_uri,
                                                image_size=image_size)
            print(f"[ImageModificationExecutor.execute_modify_image] Image modification completed successfully.")
            if response["success"] is False:
                return response
        except Exception as e:
            print(
                f"[ImageModificationExecutor.execute_modify_image] Error occurred while generating the edit image: {str(e)}")
            return {"success": False, "message": "Error occurred while generating the edit image.", "image_url": None}

        if response["image_url"]:
            image_openai_url = response["image_url"]
            print(f"[ImageModificationExecutor.execute_modify_image] Image URL: {image_openai_url}")
            # download the image from the URL
            try:
                image_bytes = requests.get(image_openai_url).content
                print(f"[ImageModificationExecutor.execute_modify_image] Image downloaded successfully.")
            except Exception as e:
                print(
                    f"[ImageModificationExecutor.execute_modify_image] Error occurred while downloading the edit image resulting file: {str(e)}")
                return {"success": False, "message": "Error occurred while downloading the edit image resulting file.",
                        "image_url": None}

            try:
                transaction = LLMTransaction(
                    organization=self.chat.assistant.organization,
                    model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=self.chat.assistant,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    llm_cost=ToolCostsMap.ImageModification.COST,
                    transaction_type=ChatRoles.SYSTEM,
                    transaction_source=TransactionSourcesNames.MODIFY_IMAGE,
                    is_tool_cost=True
                )
                transaction.save()
                print(f"[ImageModificationExecutor.execute_modify_image] Transaction saved successfully.")
            except Exception as e:
                print(
                    f"[ImageModificationExecutor.execute_modify_image] Error occurred while saving the transaction: {str(e)}")
                return {"success": False, "message": "Error occurred while saving the transaction.", "image_url": None}

            try:
                if image_bytes:
                    image_uri = self.save_images_and_provide_full_uris([image_bytes])[0]
                    print(f"[ImageModificationExecutor.execute_modify_image] Image saved successfully.")
                    return {"success": True, "message": "", "image_uri": image_uri}
            except Exception as e:
                print(
                    f"[ImageModificationExecutor.execute_modify_image] Error occurred while saving the modified image: {str(e)}")
                return {"success": False, "message": "Error occurred while saving the modified image.",
                        "image_url": None}
        return {"success": False, "message": "Error occurred while downloading the edit image resulting file.",
                "image_url": None}

    @staticmethod
    def save_images_and_provide_full_uris(image_bytes_list):
        full_uris = []
        for image_bytes in image_bytes_list:
            try:
                full_uri = ImageModificationExecutor.save_image_and_provide_full_uri(image_bytes)
                if full_uri is not None:
                    full_uris.append(full_uri)
            except Exception as e:
                print(
                    f"[ImageModificationExecutor.save_images_and_provide_full_uris] Error occurred while saving the images: {str(e)}")
        print(f"[ImageModificationExecutor.save_images_and_provide_full_uris] Full URIs: {full_uris}")
        return full_uris

    @staticmethod
    def save_image_and_provide_full_uri(image_bytes):
        guess_file_type = filetype.guess(image_bytes)
        if guess_file_type is None:
            guess_file_type = UNCLASSIFIED_FILE_EXTENSION
        extension = guess_file_type.extension
        save_name = ImageModificationExecutor.generate_save_name(extension=extension)
        s3_uri = f"{GENERATED_IMAGES_ROOT_PATH}{save_name}"
        full_uri = f"{MEDIA_URL}{s3_uri}"
        try:
            # save the image to the storage
            boto3_client = boto3.client("s3")
            bucket_name = os.getenv("AWS_STORAGE_BUCKET_NAME")
            boto3_client.put_object(Bucket=bucket_name, Key=s3_uri, Body=image_bytes)
        except Exception as e:
            print(
                f"[ImageModificationExecutor.save_image_and_provide_full_uri] Error occurred while saving image: {str(e)}")
            return None
        print(f"[ImageModificationExecutor.save_image_and_provide_full_uri] Full URI: {full_uri}")
        return full_uri

    @staticmethod
    def generate_save_name(extension):
        try:
            generated_uuid = str(uuid4())
            additional_uuid = str(uuid4())
        except Exception as e:
            print(
                f"[ImageModificationExecutor.generate_save_name] Error occurred while generating the save name: {str(e)}")
            return None
        print(
            f"[ImageModificationExecutor.generate_save_name] Save name: {generated_uuid}_{additional_uuid}.{extension}")
        return f"{generated_uuid}_{additional_uuid}.{extension}"
