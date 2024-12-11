#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: upload_file_to_storage_tasks.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:48
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

import boto3
from celery import shared_task

from apps.datasource_media_storages.utils import (
    MEDIA_FILE_TYPES,
    MediaManagerItemCategoriesNames,
    MediaManagerItemFormatTypesNamesLists
)

from config import settings

logger = logging.getLogger(__name__)


@shared_task
def upload_file_to_storage(
    file_bytes: bytes,
    full_path: str,
    media_category: str
):
    f_format = full_path.split('.')[-1]

    if f_format not in [
        file_type[0] for file_type in MEDIA_FILE_TYPES
    ]:
        return False

    if media_category == MediaManagerItemCategoriesNames.Image:

        if f_format not in MediaManagerItemFormatTypesNamesLists.IMAGE:
            return False

    elif media_category == MediaManagerItemCategoriesNames.Audio:

        if f_format not in MediaManagerItemFormatTypesNamesLists.AUDIO:
            return False

    elif media_category == MediaManagerItemCategoriesNames.Video:

        if f_format not in MediaManagerItemFormatTypesNamesLists.VIDEO:
            return False

    elif media_category == MediaManagerItemCategoriesNames.Compressed:

        if f_format not in MediaManagerItemFormatTypesNamesLists.COMPRESSED:
            return False

    elif media_category == MediaManagerItemCategoriesNames.Code:

        if f_format not in MediaManagerItemFormatTypesNamesLists.CODE:
            return False

    elif media_category == MediaManagerItemCategoriesNames.Data:

        if f_format not in MediaManagerItemFormatTypesNamesLists.DATA:
            return False

    else:
        return False

    try:
        s3c = boto3.client('s3')

        bucket = settings.AWS_STORAGE_BUCKET_NAME

        s3c.put_object(
            Bucket=bucket,
            Key=full_path,
            Body=file_bytes
        )

    except Exception as e:
        logger.error(f"[tasks.upload_file_to_storage] Error uploading file to storage: {e}")

        return False

    logger.info(f"[tasks.upload_file_to_storage] File uploaded successfully to storage: {full_path}")

    return True
