#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: reasoning_executor.py
#  Last Modified: 2024-10-06 19:55:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-06 19:55:09
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

from apps.core.code_analyst.utils import BIN_FILE_FORMAT
from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.core.media_managers.utils import GENERATED_IMAGES_ROOT_MEDIA_PATH, GENERATED_FILES_ROOT_MEDIA_PATH
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames
from config import settings
from config.settings import MEDIA_URL


logger = logging.getLogger(__name__)


class ReasoningExecutor:

    def __init__(self, assistant, chat):
        self.assistant = assistant
        self.chat = chat

    def execute_process_reasoning(self, query_string: str):
        from apps.core.generative_ai.auxiliary_clients.auxiliary_reasoning_client import ReasoningAuxiliaryLLMManager
        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles
        try:
            llm_c = ReasoningAuxiliaryLLMManager(
                assistant=self.assistant,
                chat_object=self.chat)
            logger.info(f"[ReasoningExecutor.execute_process_reasoning] OpenAI client created successfully.")
        except Exception as e:
            logger.error(f"[ReasoningExecutor.execute_process_reasoning] Failed to create the OpenAI client.")
            return f"Failed to create the OpenAI client. The cause of the error is as follows: {str(e)}"
        try:
            texts = llm_c.process_reasoning(query=query_string)
            logger.info(f"[ReasoningExecutor.execute_process_reasoning] Reasoning processed successfully.")
        except Exception as e:
            logger.error(f"[ReasoningExecutor.execute_process_reasoning] Failed to process the reasoning. ")
            return f"Failed to process the reasoning. The cause of the error is as follows: {str(e)}"

        response = texts
        try:
            tx = LLMTransaction(
                organization=self.chat.assistant.organization, model=self.chat.assistant.llm_model,
                responsible_user=self.chat.user, responsible_assistant=self.chat.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, llm_cost=InternalServiceCosts.Reasoning.COST,
                transaction_type=ChatRoles.SYSTEM, transaction_source=LLMTransactionSourcesTypesNames.REASONING,
                is_tool_cost=True)
            tx.save()
            logger.info(f"[ReasoningExecutor.execute_process_reasoning] User transaction saved successfully.")
        except Exception as e:
            logger.error(f"[ReasoningExecutor.execute_process_reasoning] Failed to save the user transaction. ")
            return f"Failed to save the user transaction. The cause of the error is as follows: {str(e)}"
        return response

    @staticmethod
    def generate_save_name(extension):
        try:
            generated_uuid = str(uuid4())
            additional_uuid = str(uuid4())
        except Exception as e:
            return None
        return f"{generated_uuid}_{additional_uuid}.{extension}"

    @staticmethod
    def save_file_and_provide_full_uri(file_bytes, remote_name):
        logger.info(f"[ReasoningExecutor.save_file_and_provide_full_uri] Saving the file to S3.")
        if not remote_name:
            guess_file_type = filetype.guess(file_bytes)
            if guess_file_type is None:
                guess_file_type = BIN_FILE_FORMAT
            extension = guess_file_type.extension
        else:
            extension = remote_name.split(".")[-1]

        save_name = ReasoningExecutor.generate_save_name(extension=extension)
        s3_path = f"{GENERATED_FILES_ROOT_MEDIA_PATH}{save_name}"
        full_uri = f"{MEDIA_URL}{s3_path}"
        try:
            s3c = boto3.client('s3')
            bucket = settings.AWS_STORAGE_BUCKET_NAME
            s3c.put_object(Bucket=bucket, Key=s3_path, Body=file_bytes)
            logger.info(f"[ReasoningExecutor.save_file_and_provide_full_uri] File saved to S3 with URI: {full_uri}")
        except Exception as e:
            logger.error(f"[ReasoningExecutor.save_file_and_provide_full_uri] Error occurred while saving the file to S3: {e}")
            return None
        return full_uri

    @staticmethod
    def save_image_and_provide_full_uri(image_bytes):
        guess_file_type = filetype.guess(image_bytes)
        if guess_file_type is None:
            guess_file_type = BIN_FILE_FORMAT
        extension = guess_file_type.extension
        save_name = ReasoningExecutor.generate_save_name(extension=extension)
        s3_path = f"{GENERATED_IMAGES_ROOT_MEDIA_PATH}{save_name}"
        full_uri = f"{MEDIA_URL}{s3_path}"
        try:
            s3c = boto3.client('s3')
            bucket = settings.AWS_STORAGE_BUCKET_NAME
            s3c.put_object(Bucket=bucket, Key=s3_path, Body=image_bytes)
            logger.info(f"[ReasoningExecutor.save_image_and_provide_full_uri] Image saved to S3 with URI: {full_uri}")
        except Exception as e:
            logger.error(f"[ReasoningExecutor.save_image_and_provide_full_uri] Error occurred while saving the image to S3: {e}")
            return None
        return full_uri

    @staticmethod
    def save_files_and_provide_full_uris(file_bytes_list: list[tuple]):
        f_uris = []
        for f_bytes, remote in file_bytes_list:
            try:
                f_uri = ReasoningExecutor.save_file_and_provide_full_uri(f_bytes, remote)
                if f_uri is not None:
                    f_uris.append(f_uri)
                logger.info(f"[ReasoningExecutor.save_files_and_provide_full_uris] File saved successfully.")
            except Exception as e:
                logger.error(f"[ReasoningExecutor.save_files_and_provide_full_uris] Error occurred while saving the file: {e}")
                pass
        return f_uris

    @staticmethod
    def save_images_and_provide_full_uris(image_bytes_list):
        f_uris = []
        for img_bytes in image_bytes_list:
            try:
                f_uri = ReasoningExecutor.save_image_and_provide_full_uri(img_bytes)
                if f_uri is not None:
                    f_uris.append(f_uri)
                logger.info(f"[ReasoningExecutor.save_images_and_provide_full_uris] Image saved successfully.")
            except Exception as e:
                logger.error(f"[ReasoningExecutor.save_images_and_provide_full_uris] Error occurred while saving the image: {e}")
                pass
        return f_uris
