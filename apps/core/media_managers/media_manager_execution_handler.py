#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: storage_executor.py
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

import io
import logging
import os
from typing import List, Dict
from uuid import uuid4

import boto3
import faiss
import filetype
import numpy as np
from PIL import Image

from apps.core.generative_ai.gpt_openai_manager import OpenAIGPTClientManager
from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.core.media_managers.helpers import MediaStorageCopyClient__AWSS3Bucket

from apps.core.media_managers.utils import (
    FILE_EXTENSION_BIN,
    GENERATED_FILES_ROOT_MEDIA_PATH,
    GENERATED_IMAGES_ROOT_MEDIA_PATH,
    MEDIA_PATH_FREEFORM_SKETCH,
    MEDIA_PATH_EDIT_IMAGE_BASE,
    MEDIA_PATH_EDIT_IMAGE_MASK,
    ImageModes,
    DEFAULT_IMAGE_COMPRESSION_JPEG,
    DEFAULT_SEARCH_RESULTS_MEDIA_ITEMS,
    OpenAIEmbeddingModels,
    VECTOR_INDEX_PATH_MEDIA_ITEMS,
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
)

from apps.datasource_media_storages.models import MediaItemVectorData

from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames
from config import settings
from config.settings import MEDIA_URL

logger = logging.getLogger(__name__)


class MediaManager:
    def __init__(self, connection, chat):
        self.connection_object = connection
        self.chat = chat

        self.media_items_index_path = os.path.join(
            VECTOR_INDEX_PATH_MEDIA_ITEMS,
            f'media_items_index_{self.connection_object.id}.index'
        )

        if os.path.exists(self.media_items_index_path):
            self.media_items_index = faiss.read_index(
                self.media_items_index_path
            )

        else:
            self.media_items_index = faiss.IndexIDMap(
                faiss.IndexFlatL2(
                    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
                )
            )
            faiss.write_index(self.media_items_index, self.media_items_index_path)

    @staticmethod
    def file_name_generator(file_format):
        uuid_1 = str(uuid4())
        uuid_2 = str(uuid4())
        return f"{uuid_1}_{uuid_2}.{file_format}"

    def _generate_query_embedding(self, query: str) -> List[float]:
        c = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.connection_object.assistant.llm_model
        )

        response = c.embeddings.create(
            input=query,
            model=OpenAIEmbeddingModels.TEXT_EMBEDDING_3_LARGE
        )

        return response.data[0].embedding

    def search_media_items(
        self,
        query: str,
        n_results: int = DEFAULT_SEARCH_RESULTS_MEDIA_ITEMS
    ) -> List[Dict]:

        query_vector = np.array([
            self._generate_query_embedding(query)
        ],
            dtype=np.float32
        )

        if self.media_items_index is None:
            raise ValueError("[search_media_items] FAISS index not initialized or loaded properly.")

        distances, ids = self.media_items_index.search(query_vector, n_results)
        results = []

        for item_id, distance in zip(ids[0], distances[0]):
            if item_id == -1:
                continue
            try:
                instance = MediaItemVectorData.objects.get(id=item_id)
                results.append({
                    "id": instance.id,
                    "data": instance.raw_data,
                    "distance": distance,
                })

            except MediaItemVectorData.DoesNotExist:
                print(f"Warning: Media Item Instance with ID {item_id} not found in the vector database.")
                logger.error(f"Media Item Instance with ID {item_id} not found in the vector database.")

        return results

    @staticmethod
    def save_file_and_return_uri(data, remote):

        if not remote:
            estimate_format = filetype.guess(data)

            if estimate_format is None:
                estimate_format = FILE_EXTENSION_BIN

            file_format = estimate_format.extension

        else:
            file_format = remote.split(".")[-1]

        file_name = MediaManager.file_name_generator(file_format=file_format)

        bucket_path = f"{GENERATED_FILES_ROOT_MEDIA_PATH}{file_name}"
        uri = f"{MEDIA_URL}{bucket_path}"

        try:
            s3c = boto3.client('s3')
            bucket = settings.AWS_STORAGE_BUCKET_NAME

            s3c.put_object(
                Bucket=bucket,
                Key=bucket_path,
                Body=data
            )

            logger.info(f"File saved to the storage with uri: {uri}")

        except Exception as e:
            logger.error(f"Error occurred while saving the file to the storage: {e}")
            return None

        return uri

    @staticmethod
    def save_sketch(sketch_data_map):
        img_bytes = sketch_data_map.get("sketch_image")

        file_name = MEDIA_PATH_FREEFORM_SKETCH + str(uuid4()) + "." + "jpeg"
        bucket_path = f"{GENERATED_IMAGES_ROOT_MEDIA_PATH}{file_name}"
        uri_sketch = f"{MEDIA_URL}{bucket_path}"

        try:
            s3c = boto3.client('s3')
            bucket = settings.AWS_STORAGE_BUCKET_NAME
            img = Image.open(io.BytesIO(img_bytes))

            if img.mode == ImageModes.RGBA:
                img = img.convert(ImageModes.RGB)

            output_io = io.BytesIO()

            img.save(
                output_io,
                format=ImageModes.JPEG,
                quality=DEFAULT_IMAGE_COMPRESSION_JPEG
            )

            compressed_image_bytes = output_io.getvalue()
            s3c.put_object(
                Bucket=bucket,
                Key=bucket_path,
                Body=compressed_image_bytes
            )
            logger.info(f"Sketch saved to the storage with uri: {uri_sketch}")

        except Exception as e:
            logger.error(f"Error occurred while saving the sketch to the storage: {e}")
            return None, None

        return [uri_sketch]

    @staticmethod
    def save_edit_image_and_masked_image(edit_img_map):
        data = edit_img_map.get("edit_image")
        data_mask = edit_img_map.get("edit_image_mask")

        estimate_format = filetype.guess(data)
        estimate_format_mask = filetype.guess(data_mask)

        if estimate_format is None:
            estimate_format = FILE_EXTENSION_BIN

        if estimate_format_mask is None:
            estimate_format_mask = FILE_EXTENSION_BIN

        format_edit = estimate_format.extension
        format_edit_mask = estimate_format_mask.extension
        file_name_edit = MEDIA_PATH_EDIT_IMAGE_BASE + str(uuid4()) + "." + format_edit
        file_name_edit_mask = MEDIA_PATH_EDIT_IMAGE_MASK + str(uuid4()) + "." + format_edit_mask

        s3_path_edit = f"{GENERATED_IMAGES_ROOT_MEDIA_PATH}{file_name_edit}"
        s3_path_edit_mask = f"{GENERATED_IMAGES_ROOT_MEDIA_PATH}{file_name_edit_mask}"
        uri_edit = f"{MEDIA_URL}{s3_path_edit}"
        uri_edit_mask = f"{MEDIA_URL}{s3_path_edit_mask}"

        try:
            s3c = boto3.client('s3')
            bucket = settings.AWS_STORAGE_BUCKET_NAME

            s3c.put_object(
                Bucket=bucket,
                Key=s3_path_edit,
                Body=data
            )

            s3c.put_object(
                Bucket=bucket,
                Key=s3_path_edit_mask,
                Body=data_mask
            )

            logger.info(f"Edit image saved to the storage with uri: {uri_edit}")

        except Exception as e:
            logger.error(f"Error occurred while saving the edit image to the storage: {e}")
            return None, None

        return [uri_edit, uri_edit_mask]

    @staticmethod
    def save_image_and_return_uri(data):

        estimate_format = filetype.guess(data)

        if estimate_format is None:
            estimate_format = FILE_EXTENSION_BIN

        file_format = estimate_format.extension
        file_name = MediaManager.file_name_generator(file_format=file_format)

        s3_uri = f"{GENERATED_IMAGES_ROOT_MEDIA_PATH}{file_name}"
        direct_uri = f"{MEDIA_URL}{s3_uri}"

        try:
            s3c = boto3.client('s3')
            bucket = settings.AWS_STORAGE_BUCKET_NAME

            s3c.put_object(
                Bucket=bucket,
                Key=s3_uri,
                Body=data
            )

            logger.info(f"Image saved to the storage with uri: {direct_uri}")

        except Exception as e:
            logger.error(f"Error occurred while saving the image to the storage: {e}")
            return None

        return direct_uri

    @staticmethod
    def save_files_and_return_uris(data_list: list[tuple]):
        uris = []

        for binary, remote in data_list:
            uri = MediaManager.save_file_and_return_uri(binary, remote)

            if uri is not None:
                uris.append(uri)

        logger.info(f"Files saved to the storage with uris: {uris}")
        return uris

    @staticmethod
    def save_images_and_return_uris(img_data_list):

        uris = []
        for binary in img_data_list:
            uri = MediaManager.save_image_and_return_uri(binary)

            if uri is not None:
                uris.append(uri)

        logger.info(f"Images saved to the storage with uris: {uris}")
        return uris

    def interpretation_handler_method(
        self,
        full_file_paths: list,
        query_string: str
    ):

        from apps.core.generative_ai.auxiliary_clients.auxiliary_llm_analyst_client import (
            AuxiliaryLLMAnalystClient
        )
        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles

        try:
            llm_c = AuxiliaryLLMAnalystClient(
                assistant=self.connection_object.assistant,
                chat_object=self.chat
            )
            logger.info("LLM Analyst Client initialized.")

        except Exception as e:
            logger.error(f"Error occurred while initializing LLM Analyst Client: {e}")
            return None

        txt, fs, imgs = llm_c.interrogate_file(
            full_file_paths=full_file_paths,
            query_string=query_string,
            interpretation_temperature=self.connection_object.interpretation_temperature
        )

        f_uris = self.save_files_and_return_uris(fs)
        img_uris = self.save_images_and_return_uris(imgs)

        final_output = {
            "response": txt,
            "file_uris": f_uris,
            "image_uris": img_uris
        }

        logger.info("Interpretation completed.")

        tx = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection_object.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.FileInterpreter.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.INTERPRET_FILE,
            is_tool_cost=True
        )
        tx.save()

        logger.info(f"Transaction saved successfully: {tx.id}")
        return final_output

    def interpretation_image_handler_method(
        self,
        full_image_paths: list,
        query_string: str
    ):
        from apps.core.generative_ai.auxiliary_clients.auxiliary_llm_vision_client import (
            AuxiliaryLLMVisionClient
        )

        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles

        try:
            llm_c = AuxiliaryLLMVisionClient(assistant=self.connection_object.assistant,
                                             chat_object=self.chat)
            logger.info("LLM Vision Client initialized.")

        except Exception as e:
            logger.error(f"Error occurred while initializing LLM Vision Client: {e}")
            return None

        response = llm_c.interpret_image_content(
            full_image_paths=full_image_paths,
            query_string=query_string,
            interpretation_temperature=self.connection_object.interpretation_temperature,
            interpretation_maximum_tokens=self.connection_object.interpretation_maximum_tokens
        )

        tx = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=self.connection_object.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.ImageInterpreter.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.INTERPRET_IMAGE,
            is_tool_cost=True
        )
        tx.save()

        logger.info(f"Transaction saved successfully: {tx.id}")

        return response

    @staticmethod
    def copy_aws_s3_bucket_into_storage(
        media_storage_id,
        aws_access_key_id,
        aws_secret_access_key,
        region_name,
        bucket_name,
        prefix
    ):

        try:

            xc_helper = MediaStorageCopyClient__AWSS3Bucket(
                media_storage_id=media_storage_id,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name
            )

            success = xc_helper.execute_copy_process(
                bucket_name=bucket_name,
                prefix=prefix
            )

            if success is False:
                logger.error("Error occurred while copying AWS S3 bucket into the storage.")
                return False

        except Exception as e:
            logger.error(f"Error occurred while copying AWS S3 bucket into the storage: {e}")
            return False

        logger.info("AWS S3 bucket copied into the storage successfully.")
        return True

    def copy_gcp_bucket_into_storage(self):
        pass

    def copy_azure_bucket_into_storage(self):
        pass

    def copy_google_drive_folder_items_into_storage(self):
        pass

    def copy_dropbox_folder_items_into_storage(self):
        pass

    def copy_onedrive_folder_items_into_storage(self):
        pass
