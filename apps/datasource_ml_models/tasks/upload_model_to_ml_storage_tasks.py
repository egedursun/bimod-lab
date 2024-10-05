#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: upload_model_to_ml_storage_tasks.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

import boto3
from celery import shared_task

from apps.datasource_ml_models.utils import MODEL_OBJECT_CATEGORIES
from config import settings
from config.settings import MEDIA_URL


@shared_task
def upload_model_to_ml_model_base(file_bytes: bytes, full_path: str):
    file_format = full_path.split('.')[-1]
    if file_format not in [file_type[0] for file_type in MODEL_OBJECT_CATEGORIES]:
        print(f"[tasks.upload_model_to_ml_model_base] Invalid file format: {file_format}, skipping file...")
        return False

    try:
        # upload to s3
        boto3_client = boto3.client('s3')
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        s3_path = full_path.split(MEDIA_URL)[-1]
        boto3_client.put_object(Bucket=bucket_name, Key=s3_path, Body=file_bytes)
    except Exception as e:
        print(f"[tasks.upload_model_to_ml_model_base] Error uploading file to storage: {e}")
        return False
    return True
