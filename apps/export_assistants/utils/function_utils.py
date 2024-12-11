#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import hashlib
import logging
import random
import string
from uuid import uuid4

import boto3
import filetype

from apps.assistants.models import Assistant

from apps.core.code_analyst.utils import (
    BIN_FILE_FORMAT
)

from apps.core.media_managers.utils import (
    GENERATED_FILES_ROOT_MEDIA_PATH,
    GENERATED_IMAGES_ROOT_MEDIA_PATH
)

from config import settings
from config.settings import MEDIA_URL

logger = logging.getLogger(__name__)


def generate_endpoint(
    assistant: Assistant,
    export_id: int
):
    logger.info(f"Generating endpoint for assistant {assistant.id}")

    org_id = assistant.organization.id
    assistant_id = assistant.id
    export_id = export_id

    endpoint_str = f"{str(org_id)}/{str(assistant_id)}/{str(export_id)}/"

    return endpoint_str


def generate_assistant_custom_api_key(assistant: Assistant):
    logger.info(f"Generating custom API key for assistant {assistant.id}")
    agent_id = assistant.id

    org_id = assistant.organization.id
    org_name = assistant.organization.name
    agent_name = assistant.name
    desc = assistant.description

    instructions = assistant.instructions
    llm_name = assistant.llm_model.model_name
    llm_temperature = assistant.llm_model.temperature
    llm_max_tokens = assistant.llm_model.maximum_tokens

    salt = settings.ENCRYPTION_SALT

    randomness_constraint = [
        random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase)
        for _ in range(64)
    ]

    merged_string = (f"{agent_id}{agent_name}{desc}{instructions}{llm_name}"
                     f"{llm_temperature}{llm_max_tokens}{llm_temperature}{salt}{randomness_constraint}")

    encrypted_string = ("bimod/" +
                        f"{str(org_id)}/" +
                        f"{''.join(ch for ch in org_name if ch.isalnum())}/" +
                        f"{str(agent_id)}/" +
                        f"{''.join(ch for ch in agent_name if ch.isalnum())}/" +
                        f"{''.join(ch for ch in llm_name if ch.isalnum())}/" +
                        hashlib.sha256(merged_string.encode()).hexdigest())

    return str(encrypted_string)


def generate_save_name(extension):
    try:
        generated_uuid = str(uuid4())
        additional_uuid = str(uuid4())

    except Exception as e:
        return None

    return f"{generated_uuid}_{additional_uuid}.{extension}"


def save_file_and_provide_full_uri(file_bytes, remote_name):
    logger.info(f"[ReasoningExecutor.save_file_and_provide_full_uri] Saving the file to S3.")

    if not remote_name:
        guess_file_type = filetype.guess(file_bytes)

        if guess_file_type is None:
            guess_file_type = BIN_FILE_FORMAT

        extension = guess_file_type.extension

    else:
        extension = remote_name.split(".")[-1]

    save_name = generate_save_name(
        extension=extension
    )

    s3_path = f"{GENERATED_FILES_ROOT_MEDIA_PATH}{save_name}"
    full_uri = f"{MEDIA_URL}{s3_path}"

    try:
        s3c = boto3.client('s3')
        bucket = settings.AWS_STORAGE_BUCKET_NAME

        s3c.put_object(
            Bucket=bucket,
            Key=s3_path,
            Body=file_bytes
        )

        logger.info(f"[save_file_and_provide_full_uri] File saved to S3 with URI: {full_uri}")

    except Exception as e:
        logger.error(f"[save_file_and_provide_full_uri] Error occurred while saving the file to S3: {e}")

        return None

    return full_uri


def save_image_and_provide_full_uri(image_bytes):
    guess_file_type = filetype.guess(image_bytes)

    if guess_file_type is None:
        guess_file_type = BIN_FILE_FORMAT

    extension = guess_file_type.extension

    save_name = generate_save_name(
        extension=extension
    )

    s3_path = f"{GENERATED_IMAGES_ROOT_MEDIA_PATH}{save_name}"
    full_uri = f"{MEDIA_URL}{s3_path}"

    try:
        s3c = boto3.client('s3')
        bucket = settings.AWS_STORAGE_BUCKET_NAME

        s3c.put_object(
            Bucket=bucket,
            Key=s3_path,
            Body=image_bytes
        )

        logger.info(f"[save_image_and_provide_full_uri] Image saved to S3 with URI: {full_uri}")

    except Exception as e:
        logger.error(f"[save_image_and_provide_full_uri] Error occurred while saving the image to S3: {e}")

        return None

    return full_uri


def save_files_and_provide_full_uris(file_bytes_list: list[tuple]):
    f_uris = []

    for f_bytes, remote in file_bytes_list:

        try:
            f_uri = save_file_and_provide_full_uri(f_bytes, remote)

            if f_uri is not None:
                f_uris.append(f_uri)

            logger.info(f"[save_files_and_provide_full_uris] File saved successfully.")

        except Exception as e:
            logger.error(f"[save_files_and_provide_full_uris] Error occurred while saving the file: {e}")
            pass

    return f_uris


def save_images_and_provide_full_uris(image_bytes_list):
    f_uris = []

    for img_bytes in image_bytes_list:

        try:
            f_uri = save_image_and_provide_full_uri(img_bytes)

            if f_uri is not None:
                f_uris.append(f_uri)

            logger.info(f"[save_images_and_provide_full_uris] Image saved successfully.")

        except Exception as e:
            logger.error(f"[save_images_and_provide_full_uris] Error occurred while saving the image: {e}")

            pass

    return f_uris
