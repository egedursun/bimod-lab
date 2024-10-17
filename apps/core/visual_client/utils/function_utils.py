#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-05 02:20:19
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
import os
from uuid import uuid4

import boto3
from filetype import filetype

from apps.core.media_managers.utils import GENERATED_IMAGES_ROOT_MEDIA_PATH
from apps.core.visual_client.utils import FILE_FORMAT_BIN
from config import settings
from config.settings import MEDIA_URL


logger = logging.getLogger(__name__)


def generator_save_images_and_return_uris(datas):
    logger.info("Saving images and returning URIs")
    uris = []
    for data in datas:
        try:
            uri = generator_save_image_and_return_uri(data)
            if uri is not None:
                uris.append(uri)
            logger.info(f"URI: {uri}")
        except Exception as e:
            logger.error(f"Error saving image and returning URI: {e}")
            continue
    return uris


def generator_save_image_and_return_uri(img_data):
    estimate_format = filetype.guess(img_data)
    if estimate_format is None:
        estimate_format = FILE_FORMAT_BIN
    file_format = estimate_format.extension
    file_name = generator_generate_save_name(extension=file_format)
    bucket_path = f"{GENERATED_IMAGES_ROOT_MEDIA_PATH}{file_name}"
    uri = f"{MEDIA_URL}{bucket_path}"
    try:
        s3c = boto3.client('s3')
        bucket = os.getenv('AWS_STORAGE_BUCKET_NAME')
        s3c.put_object(Bucket=bucket, Key=bucket_path, Body=img_data)
        logger.info(f"URI: {uri}")
    except Exception as e:
        logger.error(f"Error saving image and returning URI: {e}")
        return None
    return uri


def generator_generate_save_name(extension):
    try:
        uuid_1 = str(uuid4())
        uuid_2 = str(uuid4())
    except Exception as e:
        logger.error(f"Error generating save name: {e}")
        return None
    return f"{uuid_1}_{uuid_2}.{extension}"


def edit_save_images_and_return_uris(datas):
    uris = []
    for data in datas:
        try:
            uri = edit_save_image_and_return_uri(data)
            if uri is not None:
                uris.append(uri)
        except Exception as e:
            logger.error(f"Error saving image and returning URI: {e}")
            continue
    return uris


def edit_save_image_and_return_uri(img_data):
    estimate_format = filetype.guess(img_data)
    if estimate_format is None:
        estimate_format = FILE_FORMAT_BIN
    file_format = estimate_format.extension
    file_name = edit_generate_save_name(extension=file_format)
    bucket_path = f"{GENERATED_IMAGES_ROOT_MEDIA_PATH}{file_name}"
    uri = f"{MEDIA_URL}{bucket_path}"
    try:
        s3c = boto3.client("s3")
        bucket = os.getenv("AWS_STORAGE_BUCKET_NAME")
        s3c.put_object(Bucket=bucket, Key=bucket_path, Body=img_data)
        logger.info(f"URI: {uri}")
    except Exception as e:
        logger.error(f"Error saving image and returning URI: {e}")
        return None
    return uri


def edit_generate_save_name(extension):
    try:
        uuid_1 = str(uuid4())
        uuid_2 = str(uuid4())
    except Exception as e:
        logger.error(f"Error generating save name: {e}")
        return None
    return f"{uuid_1}_{uuid_2}.{extension}"


def dream_save_images_and_return_uris(datas):
    uris = []
    for data in datas:
        try:
            uri = dream_save_image_and_return_uri(data)
            if uri is not None:
                uris.append(uri)
        except Exception as e:
            logger.error(f"Error saving image and returning URI: {e}")
            return None
    return uris


def dream_save_image_and_return_uri(img_data):
    estimate_format = filetype.guess(img_data)
    if estimate_format is None:
        estimate_format = FILE_FORMAT_BIN
    file_format = estimate_format.extension
    file_name = dream_generate_save_name(extension=file_format)
    bucket_path = f"{GENERATED_IMAGES_ROOT_MEDIA_PATH}{file_name}"
    uri = f"{MEDIA_URL}{bucket_path}"
    try:
        s3c = boto3.client('s3')
        bucket = settings.AWS_STORAGE_BUCKET_NAME
        s3c.put_object(Bucket=bucket, Key=bucket_path, Body=img_data)
        logger.info(f"URI: {uri}")
    except Exception as e:
        logger.error(f"Error saving image and returning URI: {e}")
        return None
    return uri


def dream_generate_save_name(extension):
    try:
        uuid_1 = str(uuid4())
        uuid_2 = str(uuid4())
    except Exception as e:
        logger.error(f"Error generating save name: {e}")
        return None
    return f"{uuid_1}_{uuid_2}.{extension}"
