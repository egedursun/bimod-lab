from uuid import uuid4

import boto3
import filetype

from apps._services.code_interpreter.utils import UNCATEGORIZED_FILE_FORMAT_EXTENSION
from apps._services.config.costs_map import ToolCostsMap
from apps._services.ml_models.utils import GENERATED_FILES_ROOT_PATH, GENERATED_IMAGES_ROOT_PATH
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames
from config import settings
from config.settings import MEDIA_URL


class CodeInterpreterExecutor:

    def __init__(self, assistant, chat):
        self.assistant = assistant
        self.chat = chat

    def interpret_code(self, full_file_paths: list, query_string: str):
        from apps._services.llms.openai import InternalOpenAIClient
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
        try:
            openai_client = InternalOpenAIClient(
                assistant=self.assistant,
                multimodal_chat=self.chat)
            print(f"[CodeInterpreterExecutor.interpret_code] OpenAI client created successfully.")
        except Exception as e:
            print(
                f"[CodeInterpreterExecutor.interpret_code] Error occurred while creating the OpenAI client: {str(e)}")
            return None
        try:
            texts, files, images = openai_client.interpret_code(full_file_paths=full_file_paths,
                                                                query_string=query_string,
                                                                interpretation_temperature=float(
                                                                    self.assistant.llm_model.temperature))
            print(f"[CodeInterpreterExecutor.interpret_code] Code interpreting completed successfully.")
        except Exception as e:
            print(f"[CodeInterpreterExecutor.interpret_code] Error occurred while interpreting the code: {str(e)}")
            return None, None, None

        try:
            # Save the files and images
            full_uris = self.save_files_and_provide_full_uris(files)
            full_image_uris = self.save_images_and_provide_full_uris(images)
            print(f"[CodeInterpreterExecutor.interpret_code] Files and images saved successfully.")
        except Exception as e:
            print(
                f"[CodeInterpreterExecutor.interpret_code] Error occurred while saving the files and images: {str(e)}")
            return None, None, None

        # Prepare the response in the dictionary format
        response = {"response": texts, "file_uris": full_uris, "image_uris": full_image_uris}
        print(f"[CodeInterpreterExecutor.interpret_code] Response prepared successfully.")
        try:
            transaction = LLMTransaction(
                organization=self.chat.assistant.organization,
                model=self.chat.assistant.llm_model,
                responsible_user=self.chat.user,
                responsible_assistant=self.chat.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=ToolCostsMap.CodeInterpreter.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=TransactionSourcesNames.INTERPRET_CODE,
                is_tool_cost=True
            )
            transaction.save()
        except Exception as e:
            print(f"[CodeInterpreterExecutor.interpret_code] Error occurred while saving the transaction: {str(e)}")
            return None, None, None
        print(f"[CodeInterpreterExecutor.interpret_code] Transaction saved successfully.")
        return response

    @staticmethod
    def generate_save_name(extension):
        try:
            generated_uuid = str(uuid4())
            additional_uuid = str(uuid4())
            print(f"[CodeInterpreterExecutor.generate_save_name] Save name generated successfully.")
        except Exception as e:
            print(
                f"[CodeInterpreterExecutor.generate_save_name] Error occurred while generating the save name: {str(e)}")
            return None
        print(
            f"[CodeInterpreterExecutor.generate_save_name] Save name: {generated_uuid}_{additional_uuid}.{extension}")
        return f"{generated_uuid}_{additional_uuid}.{extension}"

    @staticmethod
    def save_file_and_provide_full_uri(file_bytes, remote_name):
        if not remote_name:
            guess_file_type = filetype.guess(file_bytes)
            if guess_file_type is None:
                guess_file_type = UNCATEGORIZED_FILE_FORMAT_EXTENSION
            extension = guess_file_type.extension
        else:
            extension = remote_name.split(".")[-1]

        print(f"[CodeInterpreterExecutor.save_file_and_provide_full_uri] Extension: {extension}")
        save_name = CodeInterpreterExecutor.generate_save_name(extension=extension)
        s3_path = f"{GENERATED_FILES_ROOT_PATH}{save_name}"
        full_uri = f"{MEDIA_URL}{s3_path}"
        print(f"[CodeInterpreterExecutor.save_file_and_provide_full_uri] Full URI: {full_uri}")
        print(f"[CodeInterpreterExecutor.save_file_and_provide_full_uri] S3 Path: {s3_path}")
        try:
            # Save the file to s3
            boto3_client = boto3.client('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            boto3_client.put_object(Bucket=bucket_name, Key=s3_path, Body=file_bytes)
            print(f"[CodeInterpreterExecutor.save_file_and_provide_full_uri] File saved successfully.")
        except Exception as e:
            print(
                f"[CodeInterpreterExecutor.save_file_and_provide_full_uri] Error occurred while saving file: {str(e)}")
            return None
        return full_uri

    @staticmethod
    def save_image_and_provide_full_uri(image_bytes):
        guess_file_type = filetype.guess(image_bytes)
        if guess_file_type is None:
            guess_file_type = UNCATEGORIZED_FILE_FORMAT_EXTENSION
        extension = guess_file_type.extension
        save_name = CodeInterpreterExecutor.generate_save_name(extension=extension)
        s3_path = f"{GENERATED_IMAGES_ROOT_PATH}{save_name}"
        full_uri = f"{MEDIA_URL}{s3_path}"
        try:
            boto3_client = boto3.client('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            boto3_client.put_object(Bucket=bucket_name, Key=s3_path, Body=image_bytes)
            print(f"[CodeInterpreterExecutor.save_image_and_provide_full_uri] Image saved successfully.")
        except Exception as e:
            print(
                f"[CodeInterpreterExecutor.save_image_and_provide_full_uri] Error occurred while saving image: {str(e)}")
            return None
        return full_uri

    @staticmethod
    def save_files_and_provide_full_uris(file_bytes_list: list[tuple]):
        full_uris = []
        for file_bytes, remote_name in file_bytes_list:
            try:
                full_uri = CodeInterpreterExecutor.save_file_and_provide_full_uri(file_bytes, remote_name)
                if full_uri is not None:
                    full_uris.append(full_uri)
            except Exception as e:
                print(
                    f"[CodeInterpreterExecutor.save_files_and_provide_full_uris] Error occurred while saving the files: {str(e)}")
        print(f"[CodeInterpreterExecutor.save_files_and_provide_full_uris] Full URIs: {full_uris}")
        return full_uris

    @staticmethod
    def save_images_and_provide_full_uris(image_bytes_list):
        full_uris = []
        for image_bytes in image_bytes_list:
            try:
                full_uri = CodeInterpreterExecutor.save_image_and_provide_full_uri(image_bytes)
                if full_uri is not None:
                    full_uris.append(full_uri)
            except Exception as e:
                print(
                    f"[CodeInterpreterExecutor.save_images_and_provide_full_uris] Error occurred while saving the images: {str(e)}")
        print(f"[CodeInterpreterExecutor.save_images_and_provide_full_uris] Full URIs: {full_uris}")
        return full_uris
