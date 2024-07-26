from uuid import uuid4
import filetype

from apps._services.config.costs_map import ToolCostsMap
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames

GENERATED_FILES_ROOT_PATH = "media/generated/files/"
GENERATED_IMAGES_ROOT_PATH = "media/generated/images/"


class StorageExecutor:

    def __init__(self, connection, chat):
        self.connection_object = connection
        self.chat = chat

    @staticmethod
    def generate_save_name(extension):
        generated_uuid = str(uuid4())
        additional_uuid = str(uuid4())
        return f"{generated_uuid}_{additional_uuid}.{extension}"

    @staticmethod
    def save_file_and_provide_full_uri(file_bytes, remote_name):
        if not remote_name:
            guess_file_type = filetype.guess(file_bytes)
            if guess_file_type is None:
                guess_file_type = ".bin"
            extension = guess_file_type.extension
        else:
            extension = remote_name.split(".")[-1]

        save_name = StorageExecutor.generate_save_name(extension=extension)
        full_uri = f"{GENERATED_FILES_ROOT_PATH}{save_name}"
        try:
            with open(full_uri, "wb") as file:
                file.write(file_bytes)
        except Exception as e:
            print(f"Error occurred while saving file: {str(e)}")
            return None
        return full_uri

    @staticmethod
    def save_image_and_provide_full_uri(image_bytes):
        guess_file_type = filetype.guess(image_bytes)
        if guess_file_type is None:
            guess_file_type = ".bin"
        extension = guess_file_type.extension
        save_name = StorageExecutor.generate_save_name(extension=extension)
        full_uri = f"{GENERATED_IMAGES_ROOT_PATH}{save_name}"
        try:
            with open(full_uri, "wb") as image:
                image.write(image_bytes)
        except Exception as e:
            print(f"Error occurred while saving image: {str(e)}")
            return None
        return full_uri

    @staticmethod
    def save_files_and_provide_full_uris(file_bytes_list:list[tuple]):
        full_uris = []
        for file_bytes, remote_name in file_bytes_list:
            full_uri = StorageExecutor.save_file_and_provide_full_uri(file_bytes, remote_name)
            if full_uri is not None:
                full_uris.append(full_uri)
        return full_uris

    @staticmethod
    def save_images_and_provide_full_uris(image_bytes_list):
        full_uris = []
        for image_bytes in image_bytes_list:
            full_uri = StorageExecutor.save_image_and_provide_full_uri(image_bytes)
            if full_uri is not None:
                full_uris.append(full_uri)
        return full_uris

    def interpret_file(self, full_file_paths: list, query_string: str):
        from apps._services.llms.openai import InternalOpenAIClient
        try:
            openai_client = InternalOpenAIClient(
                assistant=self.connection_object.assistant,
                multimodal_chat=self.chat)
        except Exception as e:
            print(f"Error occurred while creating the OpenAI client: {str(e)}")
            return None
        texts, files, images = openai_client.ask_about_file(full_file_paths=full_file_paths,
                                                            query_string=query_string,
                                                            interpretation_temperature=self.connection_object.interpretation_temperature,
                                                            interpretation_maximum_tokens=self.connection_object.interpretation_maximum_tokens)
        # Save the files
        full_uris = self.save_files_and_provide_full_uris(files)
        # Save the images
        full_image_uris = self.save_images_and_provide_full_uris(images)
        # Prepare the response in the dictionary format
        response = {"response": texts, "file_uris": full_uris, "image_uris": full_image_uris}

        transaction = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection_object.assistant,
            encoding_engine="cl100k_base",
            llm_cost=ToolCostsMap.FileInterpreter.COST,
            transaction_type="system",
            transaction_source=TransactionSourcesNames.INTERPRET_FILE,
            is_tool_cost=True
        )
        transaction.save()

        return response

    def interpret_image(self, full_image_paths: list, query_string: str):
        from apps._services.llms.openai import InternalOpenAIClient

        try:
            openai_client = InternalOpenAIClient(assistant=self.connection_object.assistant,
                                                 multimodal_chat=self.chat)
        except Exception as e:
            print(f"Error occurred while creating the OpenAI client: {str(e)}")
            return None
        response = openai_client.ask_about_image(full_image_paths=full_image_paths, query_string=query_string,
                                                 interpretation_temperature=self.connection_object.interpretation_temperature,
                                                 interpretation_maximum_tokens=self.connection_object.interpretation_maximum_tokens)

        transaction = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection_object.assistant,
            encoding_engine="cl100k_base",
            llm_cost=ToolCostsMap.ImageInterpreter.COST,
            transaction_type="system",
            transaction_source=TransactionSourcesNames.INTERPRET_IMAGE,
            is_tool_cost=True
        )
        transaction.save()

        return response
