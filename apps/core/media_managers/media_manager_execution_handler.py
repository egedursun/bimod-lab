#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#

import io
from uuid import uuid4

import boto3
import filetype
from PIL import Image

from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.core.media_managers.utils import FILE_EXTENSION_BIN, GENERATED_FILES_ROOT_MEDIA_PATH, \
    GENERATED_IMAGES_ROOT_MEDIA_PATH, MEDIA_PATH_FREEFORM_SKETCH, MEDIA_PATH_EDIT_IMAGE_BASE, \
    MEDIA_PATH_EDIT_IMAGE_MASK, ImageModes, DEFAULT_IMAGE_COMPRESSION_JPEG
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames
from config import settings
from config.settings import MEDIA_URL


class MediaManager:
    def __init__(self, connection, chat):
        self.connection_object = connection
        self.chat = chat

    @staticmethod
    def file_name_generator(file_format):
        uuid_1 = str(uuid4())
        uuid_2 = str(uuid4())
        return f"{uuid_1}_{uuid_2}.{file_format}"

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
            s3c.put_object(Bucket=bucket, Key=bucket_path, Body=data)
        except Exception as e:
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
            img.save(output_io, format=ImageModes.JPEG, quality=DEFAULT_IMAGE_COMPRESSION_JPEG)
            compressed_image_bytes = output_io.getvalue()
            s3c.put_object(Bucket=bucket, Key=bucket_path, Body=compressed_image_bytes)
        except Exception as e:
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
            s3c.put_object(Bucket=bucket, Key=s3_path_edit, Body=data)
            s3c.put_object(Bucket=bucket, Key=s3_path_edit_mask, Body=data_mask)
        except Exception as e:
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
            s3c.put_object(Bucket=bucket, Key=s3_uri, Body=data)
        except Exception as e:
            return None
        return direct_uri

    @staticmethod
    def save_files_and_return_uris(data_list: list[tuple]):
        uris = []
        for binary, remote in data_list:
            uri = MediaManager.save_file_and_return_uri(binary, remote)
            if uri is not None:
                uris.append(uri)
        return uris

    @staticmethod
    def save_images_and_return_uris(img_data_list):
        uris = []
        for binary in img_data_list:
            uri = MediaManager.save_image_and_return_uri(binary)
            if uri is not None:
                uris.append(uri)
        return uris

    def interpretation_handler_method(self, full_file_paths: list, query_string: str):
        from apps.core.generative_ai.auxiliary_clients.auxiliary_llm_analyst_client import AuxiliaryLLMAnalystClient
        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles
        try:
            llm_c = AuxiliaryLLMAnalystClient(
                assistant=self.connection_object.assistant,
                chat_object=self.chat
            )
        except Exception as e:
            return None
        txt, fs, imgs = llm_c.interrogate_file(full_file_paths=full_file_paths,
                                               query_string=query_string,
                                               interpretation_temperature=self.connection_object.interpretation_temperature)
        f_uris = self.save_files_and_return_uris(fs)
        img_uris = self.save_images_and_return_uris(imgs)
        final_output = {"response": txt, "file_uris": f_uris, "image_uris": img_uris}

        tx = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model, responsible_user=None,
            responsible_assistant=self.connection_object.assistant, encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.FileInterpreter.COST, transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.INTERPRET_FILE, is_tool_cost=True)
        tx.save()
        return final_output

    def interpretation_image_handler_method(self, full_image_paths: list, query_string: str):
        from apps.core.generative_ai.auxiliary_clients.auxiliary_llm_vision_client import AuxiliaryLLMVisionClient
        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles

        try:
            llm_c = AuxiliaryLLMVisionClient(assistant=self.connection_object.assistant,
                                             chat_object=self.chat)
        except Exception as e:
            return None
        response = llm_c.interpret_image_content(full_image_paths=full_image_paths, query_string=query_string,
                                                 interpretation_temperature=self.connection_object.interpretation_temperature,
                                                 interpretation_maximum_tokens=self.connection_object.interpretation_maximum_tokens)
        tx = LLMTransaction(
            organization=self.connection_object.assistant.organization,
            model=self.connection_object.assistant.llm_model, responsible_user=None,
            responsible_assistant=self.connection_object.assistant, encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.ImageInterpreter.COST, transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.INTERPRET_IMAGE, is_tool_cost=True)
        tx.save()
        return response
