from uuid import uuid4

import boto3
import filetype

from apps._services.config.costs_map import ToolCostsMap
from apps._services.ml_models.utils import GENERATED_FILES_ROOT_PATH, GENERATED_IMAGES_ROOT_PATH, \
    UNCLASSIFIED_FILE_EXTENSION
from apps.datasource_ml_models.models import DataSourceMLModelItem
from apps.llm_transaction.models import LLMTransaction, TransactionSourcesNames
from config import settings


class MLModelExecutor:

    def __init__(self, connection, chat):
        self.connection_object = connection
        self.chat = chat

    @staticmethod
    def generate_save_name(extension):
        generated_uuid = str(uuid4())
        additional_uuid = str(uuid4())
        print(
            f"[MLModelExecutor.generate_save_name] Generated UUID: {generated_uuid}, Additional UUID: {additional_uuid}")
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

        save_name = MLModelExecutor.generate_save_name(extension=extension)
        s3_uri = f"{GENERATED_FILES_ROOT_PATH}{save_name}"
        full_uri = f"{settings.MEDIA_URL}{s3_uri}"
        print(f"[MLModelExecutor.save_file_and_provide_full_uri] Full URI: {full_uri}")
        print(f"[MLModelExecutor.save_file_and_provide_full_uri] S3 URI: {s3_uri}")
        try:
            # Save the file to s3
            boto3_client = boto3.client('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            boto3_client.put_object(Bucket=bucket_name, Key=s3_uri, Body=file_bytes)
            print(f"[MLModelExecutor.save_file_and_provide_full_uri] File saved successfully.")
        except Exception as e:
            print(f"[MLModelExecutor.save_file_and_provide_full_uri] Error occurred while saving file: {str(e)}")
            return None
        print(f"[MLModelExecutor.save_file_and_provide_full_uri] Returning full URI: {full_uri}")
        return full_uri

    @staticmethod
    def save_image_and_provide_full_uri(image_bytes):
        guess_file_type = filetype.guess(image_bytes)
        if guess_file_type is None:
            guess_file_type = ".bin"
        extension = guess_file_type.extension
        save_name = MLModelExecutor.generate_save_name(extension=extension)
        s3_uri = f"{GENERATED_IMAGES_ROOT_PATH}{save_name}"
        full_uri = f"{settings.MEDIA_URL}{s3_uri}"
        print(f"[MLModelExecutor.save_image_and_provide_full_uri] Full URI: {full_uri}")
        print(f"[MLModelExecutor.save_image_and_provide_full_uri] S3 URI: {s3_uri}")
        try:
            # save the image to the s3
            boto3_client = boto3.client('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            boto3_client.put_object(Bucket=bucket_name, Key=s3_uri, Body=image_bytes)
            print(f"[MLModelExecutor.save_image_and_provide_full_uri] Image saved successfully.")
        except Exception as e:
            print(f"[MLModelExecutor.save_image_and_provide_full_uri] Error occurred while saving image: {str(e)}")
            return None
        return full_uri

    @staticmethod
    def save_files_and_provide_full_uris(file_bytes_list: list[tuple]):
        full_uris = []
        for file_bytes, remote_name in file_bytes_list:
            full_uri = MLModelExecutor.save_file_and_provide_full_uri(file_bytes, remote_name)
            if full_uri is not None:
                full_uris.append(full_uri)
        print(f"[MLModelExecutor.save_files_and_provide_full_uris] Full URIs: {full_uris}")
        return full_uris

    @staticmethod
    def save_images_and_provide_full_uris(image_bytes_list):
        full_uris = []
        for image_bytes in image_bytes_list:
            full_uri = MLModelExecutor.save_image_and_provide_full_uri(image_bytes)
            if full_uri is not None:
                full_uris.append(full_uri)
        print(f"[MLModelExecutor.save_images_and_provide_full_uris] Full URIs: {full_uris}")
        return full_uris

    #################################################################################################################

    def execute_predict_with_ml_model(self, model_url, file_urls, input_data):
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
        from apps._services.llms.openai import InternalOpenAIClient
        try:
            openai_client = InternalOpenAIClient(
                assistant=self.connection_object.assistant,
                multimodal_chat=self.chat)
            print(f"[MLModelExecutor.execute_predict_with_ml_model] OpenAI client created successfully.")
        except Exception as e:
            print(
                f"[MLModelExecutor.execute_predict_with_ml_model] Error occurred while creating the OpenAI client: {str(e)}")
            return None
        retrieve_model_object = DataSourceMLModelItem.objects.get(full_file_path=model_url)
        model_temperature = retrieve_model_object.interpretation_temperature
        texts, files, images = openai_client.predict_with_ml_model(
            ml_model_path=model_url,
            input_data_urls=file_urls,
            query_string=input_data,
            interpretation_temperature=model_temperature)
        print(f"[MLModelExecutor.execute_predict_with_ml_model] Prediction completed successfully.")
        # Save the files and images
        full_uris = self.save_files_and_provide_full_uris(files)
        full_image_uris = self.save_images_and_provide_full_uris(images)
        # Prepare the response in the dictionary format
        response = {"response": texts, "file_uris": full_uris, "image_uris": full_image_uris}

        transaction = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection_object.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=ToolCostsMap.MLModelExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=TransactionSourcesNames.ML_MODEL_PREDICTION,
            is_tool_cost=True
        )
        transaction.save()
        print(f"[MLModelExecutor.execute_predict_with_ml_model] Transaction saved successfully.")
        return response
