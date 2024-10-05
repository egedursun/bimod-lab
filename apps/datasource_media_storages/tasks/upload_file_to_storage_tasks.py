#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: upload_file_to_storage_tasks.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: upload_file_to_storage_tasks.py
#  Last Modified: 2024-09-27 12:19:22
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:46:21
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import boto3
from celery import shared_task

from apps.datasource_media_storages.utils import MEDIA_FILE_TYPES, MediaCategoriesNames, MediaFileTypesNamesLists
from config import settings


@shared_task
def upload_file_to_storage(file_bytes: bytes, full_path: str, media_category: str):
    file_format = full_path.split('.')[-1]
    if file_format not in [file_type[0] for file_type in MEDIA_FILE_TYPES]:
        print(f"Invalid file format: {file_format}, skipping file...")
        return False

    if media_category == MediaCategoriesNames.Image:
        if file_format not in MediaFileTypesNamesLists.IMAGE:
            print(f"Invalid IMAGE file format: {file_format}, skipping file...")
            return False
    elif media_category == MediaCategoriesNames.Audio:
        if file_format not in MediaFileTypesNamesLists.AUDIO:
            print(f"Invalid AUDIO file format: {file_format}, skipping file...")
            return False
    elif media_category == MediaCategoriesNames.Video:
        if file_format not in MediaFileTypesNamesLists.VIDEO:
            print(f"Invalid VIDEO file format: {file_format}, skipping file...")
            return False
    elif media_category == MediaCategoriesNames.Compressed:
        if file_format not in MediaFileTypesNamesLists.COMPRESSED:
            print(f"Invalid COMPRESSED file format: {file_format}, skipping file...")
            return False
    elif media_category == MediaCategoriesNames.Code:
        if file_format not in MediaFileTypesNamesLists.CODE:
            print(f"Invalid CODE file format: {file_format}, skipping file...")
            return False
    elif media_category == MediaCategoriesNames.Data:
        if file_format not in MediaFileTypesNamesLists.DATA:
            print(f"Invalid DATA file format: {file_format}, skipping file...")
            return False
    else:
        print(f"Invalid media category: {media_category}, skipping file...")
        return False

    try:
        # here
        s3_client = boto3.client('s3')
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        s3_client.put_object(Bucket=bucket_name, Key=full_path, Body=file_bytes)
    except Exception as e:
        print(f"Error uploading file to storage: {e}")
        return False
    return True
