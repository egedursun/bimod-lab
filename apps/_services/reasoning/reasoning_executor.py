#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#


from uuid import uuid4

import boto3
import filetype

from apps._services.code_interpreter.utils import UNCATEGORIZED_FILE_FORMAT_EXTENSION
from apps._services.config.costs_map import ToolCostsMap
from apps._services.storages.utils import GENERATED_IMAGES_ROOT_PATH, GENERATED_FILES_ROOT_PATH
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import TransactionSourcesNames
from config import settings
from config.settings import MEDIA_URL


class ReasoningExecutor:

    def __init__(self, assistant, chat):
        self.assistant = assistant
        self.chat = chat

    def execute_process_reasoning(self, query_string: str):
        from apps._services.llms.openai import InternalOpenAIClient
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
        try:
            openai_client = InternalOpenAIClient(
                assistant=self.assistant,
                multimodal_chat=self.chat)
            print(f"[ReasoningExecutor.execute_process_reasoning] OpenAI client created successfully.")
        except Exception as e:
            print(
                f"[ReasoningExecutor.execute_process_reasoning] Error occurred while creating the OpenAI client: {str(e)}")
            return f"Failed to create the OpenAI client. The cause of the error is as follows: {str(e)}"
        try:
            texts = openai_client.process_reasoning(query=query_string)
            print(f"[ReasoningExecutor.execute_process_reasoning] Reasoning operation completed successfully.")
        except Exception as e:
            print(f"[ReasoningExecutor.execute_process_reasoning] Error occurred while processing the reasoning: {str(e)}")
            return f"Failed to process the reasoning. The cause of the error is as follows: {str(e)}"

        # Prepare the response in the dictionary format
        response = texts
        print(f"[ReasoningExecutor.execute_process_reasoning] Response prepared successfully.")
        try:
            transaction = LLMTransaction(
                organization=self.chat.assistant.organization,
                model=self.chat.assistant.llm_model,
                responsible_user=self.chat.user,
                responsible_assistant=self.chat.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=ToolCostsMap.Reasoning.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=TransactionSourcesNames.REASONING,
                is_tool_cost=True
            )
            transaction.save()
        except Exception as e:
            print(f"[ReasoningExecutor.execute_process_reasoning] Error occurred while saving the transaction: {str(e)}")
            return f"Failed to save the user transaction. The cause of the error is as follows: {str(e)}"
        print(f"[ReasoningExecutor.execute_process_reasoning] Transaction saved successfully.")
        return response

    @staticmethod
    def generate_save_name(extension):
        try:
            generated_uuid = str(uuid4())
            additional_uuid = str(uuid4())
            print(f"[ReasoningExecutor.generate_save_name] Save name generated successfully.")
        except Exception as e:
            print(
                f"[ReasoningExecutor.generate_save_name] Error occurred while generating the save name: {str(e)}")
            return None
        print(
            f"[ReasoningExecutor.generate_save_name] Save name generated successfully: {generated_uuid}_{additional_uuid}.{extension}")
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
        save_name = ReasoningExecutor.generate_save_name(extension=extension)
        s3_path = f"{GENERATED_FILES_ROOT_PATH}{save_name}"
        full_uri = f"{MEDIA_URL}{s3_path}"
        try:
            # Save the file to s3
            boto3_client = boto3.client('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            boto3_client.put_object(Bucket=bucket_name, Key=s3_path, Body=file_bytes)
            print(f"[ReasoningExecutor.save_file_and_provide_full_uri] File saved successfully.")
        except Exception as e:
            print(
                f"[ReasoningExecutor.save_file_and_provide_full_uri] Error occurred while saving the file: {str(e)}")
            return None
        return full_uri

    @staticmethod
    def save_image_and_provide_full_uri(image_bytes):
        guess_file_type = filetype.guess(image_bytes)
        if guess_file_type is None:
            guess_file_type = UNCATEGORIZED_FILE_FORMAT_EXTENSION
        extension = guess_file_type.extension
        save_name = ReasoningExecutor.generate_save_name(extension=extension)
        s3_path = f"{GENERATED_IMAGES_ROOT_PATH}{save_name}"
        full_uri = f"{MEDIA_URL}{s3_path}"
        try:
            boto3_client = boto3.client('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            boto3_client.put_object(Bucket=bucket_name, Key=s3_path, Body=image_bytes)
            print(f"[ReasoningExecutor.save_image_and_provide_full_uri] Image saved successfully.")
        except Exception as e:
            print(
                f"[ReasoningExecutor.save_image_and_provide_full_uri] Error occurred while saving image: {str(e)}")
            return None
        return full_uri

    @staticmethod
    def save_files_and_provide_full_uris(file_bytes_list: list[tuple]):
        full_uris = []
        for file_bytes, remote_name in file_bytes_list:
            try:
                full_uri = ReasoningExecutor.save_file_and_provide_full_uri(file_bytes, remote_name)
                if full_uri is not None:
                    full_uris.append(full_uri)
            except Exception as e:
                print(
                    f"[ReasoningExecutor.save_files_and_provide_full_uris] Error occurred while saving the files: {str(e)}")
        print(f"[ReasoningExecutor.save_files_and_provide_full_uris] Full URIs: {full_uris}")
        return full_uris

    @staticmethod
    def save_images_and_provide_full_uris(image_bytes_list):
        full_uris = []
        for image_bytes in image_bytes_list:
            try:
                full_uri = ReasoningExecutor.save_image_and_provide_full_uri(image_bytes)
                if full_uri is not None:
                    full_uris.append(full_uri)
            except Exception as e:
                print(
                    f"[ReasoningExecutor.save_images_and_provide_full_uris] Error occurred while saving the images: {str(e)}")
        print(f"[ReasoningExecutor.save_images_and_provide_full_uris] Full URIs: {full_uris}")
        return full_uris
