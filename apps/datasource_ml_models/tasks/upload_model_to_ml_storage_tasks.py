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

from apps.datasource_ml_models.utils import ML_MODEL_ITEM_CATEGORIES
from config import settings
from config.settings import MEDIA_URL


@shared_task
def upload_model_to_ml_model_base(file_bytes: bytes, full_path: str):
    f_format = full_path.split('.')[-1]
    if f_format not in [file_type[0] for file_type in ML_MODEL_ITEM_CATEGORIES]:
        return False
    try:
        s3c = boto3.client('s3')
        bucket = settings.AWS_STORAGE_BUCKET_NAME
        bucket_path = full_path.split(MEDIA_URL)[-1]
        s3c.put_object(Bucket=bucket, Key=bucket_path, Body=file_bytes)
    except Exception as e:
        return False
    return True
