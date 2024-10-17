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
#
#
import logging
from uuid import uuid4

import boto3
from filetype import filetype

from apps.core.code_analyst.utils import BIN_FILE_FORMAT
from apps.core.media_managers.utils import GENERATED_FILES_ROOT_MEDIA_PATH, GENERATED_IMAGES_ROOT_MEDIA_PATH
from config import settings
from config.settings import MEDIA_URL

logger = logging.getLogger(__name__)


def save_object_to_s3_bucket(file_format, f_data):
    logger.info(f"Saving file to S3 bucket with format: {file_format}")
    file_name = generate_file_object_name(file_format=file_format)
    bucket_path = f"{GENERATED_FILES_ROOT_MEDIA_PATH}{file_name}"
    uri = f"{MEDIA_URL}{bucket_path}"
    try:
        s3c = boto3.client('s3')
        bucket = settings.AWS_STORAGE_BUCKET_NAME
        s3c.put_object(Bucket=bucket, Key=bucket_path, Body=f_data)
        logger.info(f"File saved to S3 bucket with URI: {uri}")
    except Exception as e:
        logger.error(f"Error while saving file to S3 bucket: {str(e)}")
        return None
    return uri


def save_media_to_s3_bucket(file_format, img_data):
    logger.info(f"Saving image to S3 bucket with format: {file_format}")
    file_name = generate_file_object_name(file_format=file_format)
    bucket_path = f"{GENERATED_IMAGES_ROOT_MEDIA_PATH}{file_name}"
    uri = f"{MEDIA_URL}{bucket_path}"
    try:
        s3c = boto3.client('s3')
        bucket = settings.AWS_STORAGE_BUCKET_NAME
        s3c.put_object(Bucket=bucket, Key=bucket_path, Body=img_data)
        logger.info(f"Image saved to S3 bucket with URI: {uri}")
    except Exception as e:
        logger.error(f"Error while saving image to S3 bucket: {str(e)}")
        return None
    return uri


def generate_file_object_name(file_format):
    try:
        tmp_uuid_1 = str(uuid4())
        tmp_uuid_2 = str(uuid4())
        logger.info(f"Generated UUIDs: {tmp_uuid_1}, {tmp_uuid_2}")
    except Exception as e:
        logger.error(f"Error while generating UUIDs: {str(e)}")
        return None
    final_uuid = f"{tmp_uuid_1}_{tmp_uuid_2}.{file_format}"
    return final_uuid


def save_file_and_return_uri(file_data, remote):
    if not remote:
        estimate_file_type = filetype.guess(file_data)
        if estimate_file_type is None:
            estimate_file_type = BIN_FILE_FORMAT
        format_specifier = estimate_file_type.extension
    else:
        format_specifier = remote.split(".")[-1]
    logger.info(f"File format specifier: {format_specifier}")
    return save_object_to_s3_bucket(format_specifier, file_data)


def save_files_and_return_uris(file_data_list: list[tuple]):
    uris = []
    for data, remote in file_data_list:
        try:
            full_uri = save_file_and_return_uri(data, remote)
            if full_uri is not None:
                uris.append(full_uri)
            logger.info(f"File URI: {full_uri}")
        except Exception as e:
            logger.error(f"Error while saving file: {str(e)}")
            continue
    return uris


def save_image_and_return_uri(img_data):
    estimate_file_type = filetype.guess(img_data)
    if estimate_file_type is None:
        estimate_file_type = BIN_FILE_FORMAT
    format_specifier = estimate_file_type.extension
    logger.info(f"Image format specifier: {format_specifier}")
    return save_media_to_s3_bucket(format_specifier, img_data)


def save_images_and_return_uris(img_data_list):
    uris = []
    for data in img_data_list:
        try:
            full_uri = save_image_and_return_uri(data)
            if full_uri is not None:
                uris.append(full_uri)
            logger.info(f"Image URI: {full_uri}")
        except Exception as e:
            logger.error(f"Error while saving image: {str(e)}")
            continue
    return uris
