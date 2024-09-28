import io
from uuid import uuid4

import boto3
import filetype
from PIL import Image

from apps._services.config.costs_map import ToolCostsMap
from apps._services.storages.utils import UNCLASSIFIED_FILE_EXTENSION, GENERATED_FILES_ROOT_PATH, \
    GENERATED_IMAGES_ROOT_PATH, DEFAULT_PATH_FREEFORM_USER_SKETCH, DEFAULT_PATH_EDIT_IMAGE_ORIGINAL, \
    DEFAULT_PATH_EDIT_IMAGE_MASKED
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import TransactionSourcesNames
from config import settings
from config.settings import MEDIA_URL


class StorageExecutor:

    def __init__(self, connection, chat):
        self.connection_object = connection
        self.chat = chat

    @staticmethod
    def generate_save_name(extension):
        generated_uuid = str(uuid4())
        additional_uuid = str(uuid4())
        print(
            f"[StorageExecutor.generate_save_name] Generated UUID: {generated_uuid}, Additional UUID: {additional_uuid}")
        return f"{generated_uuid}_{additional_uuid}.{extension}"

    @staticmethod
    def save_file_and_provide_full_uri(file_bytes, remote_name):
        if not remote_name:
            guess_file_type = filetype.guess(file_bytes)
            if guess_file_type is None:
                guess_file_type = UNCLASSIFIED_FILE_EXTENSION
            extension = guess_file_type.extension
        else:
            extension = remote_name.split(".")[-1]

        save_name = StorageExecutor.generate_save_name(extension=extension)
        s3_uri = f"{GENERATED_FILES_ROOT_PATH}{save_name}"
        full_uri = f"{MEDIA_URL}{s3_uri}"
        print(f"[StorageExecutor.save_file_and_provide_full_uri] Full URI: {full_uri}")
        print(f"[StorageExecutor.save_file_and_provide_full_uri] S3 URI: {s3_uri}")
        try:
            # save the file to the s3 bucket
            boto3_client = boto3.client('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            boto3_client.put_object(Bucket=bucket_name, Key=s3_uri, Body=file_bytes)
            print(f"[StorageExecutor.save_file_and_provide_full_uri] File saved successfully.")
        except Exception as e:
            print(f"[StorageExecutor.save_file_and_provide_full_uri] Error occurred while saving file: {str(e)}")
            return None
        return full_uri

    @staticmethod
    def save_sketch_images(sketch_image_dict):
        sketch_image_bytes = sketch_image_dict.get("sketch_image")

        save_name_sketch_image = DEFAULT_PATH_FREEFORM_USER_SKETCH + str(uuid4()) + "." + "jpeg"
        s3_path = f"{GENERATED_IMAGES_ROOT_PATH}{save_name_sketch_image}"
        full_uri_sketch_image = f"{MEDIA_URL}{s3_path}"
        try:
            # save the image to the s3 bucket
            boto3_client = boto3.client('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            # compress the image and assign to a new variable
            image = Image.open(io.BytesIO(sketch_image_bytes))
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            output_io = io.BytesIO()
            image.save(output_io, format='JPEG', quality=80)
            compressed_image_bytes = output_io.getvalue()
            boto3_client.put_object(Bucket=bucket_name, Key=s3_path, Body=compressed_image_bytes)
            print(f"[StorageExecutor.save_sketch_images] Sketch image saved successfully.")
        except Exception as e:
            print(f"[StorageExecutor.save_sketch_images] Error occurred while saving image: {str(e)}")
            return None, None
        return [full_uri_sketch_image]

    @staticmethod
    def save_edit_images(edit_image_dict):
        edit_image_bytes = edit_image_dict.get("edit_image")
        edit_image_mask_bytes = edit_image_dict.get("edit_image_mask")

        guess_file_type_edit_image = filetype.guess(edit_image_bytes)
        guess_file_type_edit_image_mask = filetype.guess(edit_image_mask_bytes)
        if guess_file_type_edit_image is None:
            guess_file_type_edit_image = UNCLASSIFIED_FILE_EXTENSION
        if guess_file_type_edit_image_mask is None:
            guess_file_type_edit_image_mask = UNCLASSIFIED_FILE_EXTENSION
        extension_edit_image = guess_file_type_edit_image.extension
        extension_edit_image_mask = guess_file_type_edit_image_mask.extension

        save_name_edit_image = DEFAULT_PATH_EDIT_IMAGE_ORIGINAL + str(uuid4()) + "." + extension_edit_image
        save_name_edit_image_mask = DEFAULT_PATH_EDIT_IMAGE_MASKED + str(uuid4()) + "." + extension_edit_image_mask
        boto3_uri_edit_image = f"{GENERATED_IMAGES_ROOT_PATH}{save_name_edit_image}"
        boto3_uri_edit_image_mask = f"{GENERATED_IMAGES_ROOT_PATH}{save_name_edit_image_mask}"
        full_uri_edit_image = f"{MEDIA_URL}{boto3_uri_edit_image}"
        full_uri_edit_image_mask = f"{MEDIA_URL}{boto3_uri_edit_image_mask}"
        try:
            # save the image to the s3 bucket
            boto3_client = boto3.client('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            boto3_client.put_object(Bucket=bucket_name, Key=boto3_uri_edit_image, Body=edit_image_bytes)
            boto3_client.put_object(Bucket=bucket_name, Key=boto3_uri_edit_image_mask, Body=edit_image_mask_bytes)
            print(f"[StorageExecutor.save_edit_images] Edit images saved successfully.")
        except Exception as e:
            print(f"[StorageExecutor.save_edit_images] Error occurred while saving image: {str(e)}")
            return None, None
        print(
            f"[StorageExecutor.save_edit_images] Returning full URIs: {full_uri_edit_image}, {full_uri_edit_image_mask}")
        return [full_uri_edit_image, full_uri_edit_image_mask]

    @staticmethod
    def save_image_and_provide_full_uri(image_bytes):
        guess_file_type = filetype.guess(image_bytes)
        if guess_file_type is None:
            guess_file_type = UNCLASSIFIED_FILE_EXTENSION
        extension = guess_file_type.extension
        save_name = StorageExecutor.generate_save_name(extension=extension)
        s3_uri = f"{GENERATED_IMAGES_ROOT_PATH}{save_name}"
        full_uri = f"{MEDIA_URL}{s3_uri}"
        print(f"[StorageExecutor.save_image_and_provide_full_uri] Full URI: {full_uri}")
        print(f"[StorageExecutor.save_image_and_provide_full_uri] S3 URI: {s3_uri}")
        try:
            # save the image to the s3 bucket
            boto3_client = boto3.client('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            boto3_client.put_object(Bucket=bucket_name, Key=s3_uri, Body=image_bytes)
            print(f"[StorageExecutor.save_image_and_provide_full_uri] Image saved successfully.")
        except Exception as e:
            print(f"[StorageExecutor.save_image_and_provide_full_uri] Error occurred while saving image: {str(e)}")
            return None
        return full_uri

    @staticmethod
    def save_files_and_provide_full_uris(file_bytes_list: list[tuple]):
        full_uris = []
        for file_bytes, remote_name in file_bytes_list:
            full_uri = StorageExecutor.save_file_and_provide_full_uri(file_bytes, remote_name)
            if full_uri is not None:
                full_uris.append(full_uri)
        print(f"[StorageExecutor.save_files_and_provide_full_uris] Full URIs: {full_uris}")
        return full_uris

    @staticmethod
    def save_images_and_provide_full_uris(image_bytes_list):
        full_uris = []
        for image_bytes in image_bytes_list:
            full_uri = StorageExecutor.save_image_and_provide_full_uri(image_bytes)
            if full_uri is not None:
                full_uris.append(full_uri)
        print(f"[StorageExecutor.save_images_and_provide_full_uris] Full URIs: {full_uris}")
        return full_uris

    def interpret_file(self, full_file_paths: list, query_string: str):
        from apps._services.llms.openai import InternalOpenAIClient
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
        try:
            openai_client = InternalOpenAIClient(
                assistant=self.connection_object.assistant,
                multimodal_chat=self.chat)
            print(f"[StorageExecutor.interpret_file] OpenAI client has been created.")
        except Exception as e:
            print(f"[StorageExecutor.interpret_file] Error occurred while creating the OpenAI client: {str(e)}")
            return None
        texts, files, images = openai_client.ask_about_file(full_file_paths=full_file_paths,
                                                            query_string=query_string,
                                                            interpretation_temperature=self.connection_object.interpretation_temperature)
        print(f"[StorageExecutor.interpret_file] Texts, Files, and Images are received.")
        # Save the files and files
        full_uris = self.save_files_and_provide_full_uris(files)
        full_image_uris = self.save_images_and_provide_full_uris(images)
        # Prepare the response in the dictionary format
        response = {"response": texts, "file_uris": full_uris, "image_uris": full_image_uris}
        print(f"[StorageExecutor.interpret_file] Response has been prepared.")

        transaction = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection_object.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=ToolCostsMap.FileInterpreter.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=TransactionSourcesNames.INTERPRET_FILE,
            is_tool_cost=True
        )
        transaction.save()
        print(f"[StorageExecutor.interpret_file] Transaction has been saved.")
        return response

    def interpret_image(self, full_image_paths: list, query_string: str):
        from apps._services.llms.openai import InternalOpenAIClient
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles

        try:
            openai_client = InternalOpenAIClient(assistant=self.connection_object.assistant,
                                                 multimodal_chat=self.chat)
            print(f"[StorageExecutor.interpret_image] OpenAI client has been created.")
        except Exception as e:
            print(f"[StorageExecutor.interpret_image] Error occurred while creating the OpenAI client: {str(e)}")
            return None
        response = openai_client.ask_about_image(full_image_paths=full_image_paths, query_string=query_string,
                                                 interpretation_temperature=self.connection_object.interpretation_temperature,
                                                 interpretation_maximum_tokens=self.connection_object.interpretation_maximum_tokens)
        print(f"[StorageExecutor.interpret_image] Response has been received.")

        transaction = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection_object.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=ToolCostsMap.ImageInterpreter.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=TransactionSourcesNames.INTERPRET_IMAGE,
            is_tool_cost=True
        )
        transaction.save()
        print(f"[StorageExecutor.interpret_image] Transaction has been saved.")
        return response
