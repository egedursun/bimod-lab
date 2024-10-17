#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ml_model_executor.py
#  Last Modified: 2024-10-05 02:25:59
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
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
from uuid import uuid4

import boto3
import filetype

from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.core.ml_models.utils import GENERATED_FILES_ROOT_PATH, GENERATED_IMAGES_ROOT_PATH, \
    UNCLASSIFIED_FILE_EXTENSION
from apps.datasource_ml_models.models import DataSourceMLModelItem
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames
from config import settings


logger = logging.getLogger(__name__)


class MLModelExecutor:

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
                guess_file_type = UNCLASSIFIED_FILE_EXTENSION
            extension = guess_file_type.extension
            logger.info(f"Guessed extension for the file is: {extension}")
        else:
            logger.info(f"Remote name provided for the file is: {remote_name}")
            extension = remote_name.split(".")[-1]

        save_name = MLModelExecutor.generate_save_name(extension=extension)
        s3_uri = f"{GENERATED_FILES_ROOT_PATH}{save_name}"
        full_uri = f"{settings.MEDIA_URL}{s3_uri}"
        try:
            s3c = boto3.client('s3')
            bucket = settings.AWS_STORAGE_BUCKET_NAME
            s3c.put_object(Bucket=bucket, Key=s3_uri, Body=file_bytes)
            logger.info(f"File saved to S3 with URI: {full_uri}")
        except Exception as e:
            logger.error(f"Error occurred while saving the file to S3: {e}")
            return None
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
        try:
            s3c = boto3.client('s3')
            bucket = settings.AWS_STORAGE_BUCKET_NAME
            s3c.put_object(Bucket=bucket, Key=s3_uri, Body=image_bytes)
            logger.info(f"Image saved to S3 with URI: {full_uri}")
        except Exception as e:
            logger.error(f"Error occurred while saving the image to S3: {e}")
            return None
        return full_uri

    @staticmethod
    def save_files_and_provide_full_uris(file_bytes_list: list[tuple]):
        full_uris = []
        for file_bytes, remote_name in file_bytes_list:
            full_uri = MLModelExecutor.save_file_and_provide_full_uri(file_bytes, remote_name)
            if full_uri is not None:
                full_uris.append(full_uri)
        logger.info(f"Full URIs for the files: {full_uris}")
        return full_uris

    @staticmethod
    def save_images_and_provide_full_uris(image_bytes_list):
        full_uris = []
        for image_bytes in image_bytes_list:
            full_uri = MLModelExecutor.save_image_and_provide_full_uri(image_bytes)
            if full_uri is not None:
                full_uris.append(full_uri)
        logger.info(f"Full URIs for the images: {full_uris}")
        return full_uris

    def execute_predict_with_ml_model(self, model_url, file_urls, input_data):
        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles
        from apps.core.generative_ai.auxiliary_clients.auxiliary_llm_machine_learning_client import \
            AuxiliaryLLMMachineLearningClient
        try:
            openai_client = AuxiliaryLLMMachineLearningClient(
                assistant=self.connection_object.assistant,
                chat_object=self.chat)
            logger.info(f"ML model client created for the assistant: {self.connection_object.assistant}")
        except Exception as e:
            logger.error(f"Error occurred while creating the ML model client: {e}")
            return None

        retrieve_model_object = DataSourceMLModelItem.objects.get(full_file_path=model_url)
        model_temperature = retrieve_model_object.interpretation_temperature
        txts, fs, imgs = openai_client.infer_prediction_with_ml(
            ml_model_path=model_url, input_data_urls=file_urls, query_string=input_data,
            interpretation_temperature=model_temperature)

        f_uris = self.save_files_and_provide_full_uris(fs)
        f_img_uris = self.save_images_and_provide_full_uris(imgs)
        response = {"response": txts, "file_uris": f_uris, "image_uris": f_img_uris}

        tx = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model, responsible_user=None,
            responsible_assistant=self.connection_object.assistant, encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.MLModelExecutor.COST, transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.ML_MODEL_PREDICTION, is_tool_cost=True)
        tx.save()
        logger.info(f"Transaction saved successfully: {tx.id}")
        return response
