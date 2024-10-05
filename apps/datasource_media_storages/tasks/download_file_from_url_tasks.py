#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: download_file_from_url_tasks.py
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
#  File: download_file_from_url_tasks.py
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

import uuid

import filetype
from celery import shared_task


@shared_task
def download_file_from_url(storage_id: int, url: str):
    from apps.datasource_media_storages.models import DataSourceMediaStorageConnection, DataSourceMediaStorageItem
    import requests
    storage = DataSourceMediaStorageConnection.objects.get(id=storage_id)
    if not storage:
        print(f"Storage with ID: {storage_id} does not exist")
        return False
    file_extension = url.split('.')[-1]
    f_generated = None
    try:
        f_generated = generate_file_name(file_extension=file_extension, url=url)
    except Exception as e:
        print(f"Error generating file name: {e}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_bytes = response.content

            if not f_generated:
                f_generated = f"{uuid.uuid4()}_{uuid.uuid4()}.{filetype.guess(file_bytes).extension}"

            media_storage_item = DataSourceMediaStorageItem.objects.create(
                storage_base=storage,
                media_file_name=f_generated,
                media_file_size=len(file_bytes),
                media_file_type=file_extension,
                file_bytes=file_bytes
            )
            media_storage_item.save()
        else:
            print(f"Error downloading file from URL: {url}")
            return False
    except Exception as e:
        print(f"Error downloading file from URL: {url}, {e}")
        return False


def generate_file_name(url: str, file_extension: str):
    extracted_file_name = url.split('/')[-1]
    combined_file_name = f"{extracted_file_name}.{file_extension}"
    return combined_file_name
