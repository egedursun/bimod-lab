#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: download_file_from_url_tasks.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

import uuid

import filetype
from celery import shared_task


@shared_task
def download_file_from_url(storage_id: int, url: str):
    from apps.datasource_media_storages.models import DataSourceMediaStorageConnection, DataSourceMediaStorageItem
    import requests
    media_manager = DataSourceMediaStorageConnection.objects.get(id=storage_id)
    if not media_manager:
        print(f"Storage with ID: {storage_id} does not exist")
        return False
    file_format = url.split('.')[-1]
    f_generated = None
    try:
        f_generated = build_media_manager_file_name(file_extension=file_format, url=url)
    except Exception as e:
        pass
    try:
        output = requests.get(url)
        if output.status_code == 200:
            file_data = output.content
            if not f_generated:
                f_generated = f"{uuid.uuid4()}_{uuid.uuid4()}.{filetype.guess(file_data).extension}"
            media_item = DataSourceMediaStorageItem.objects.create(
                storage_base=media_manager, media_file_name=f_generated, media_file_size=len(file_data),
                media_file_type=file_format, file_bytes=file_data
            )
            media_item.save()
        else:
            return False
    except Exception as e:
        return False


def build_media_manager_file_name(url: str, file_extension: str):
    component = url.split('/')[-1]
    combined_file_name = f"{component}.{file_extension}"
    return combined_file_name
