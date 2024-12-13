#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging
import uuid

import filetype

logger = logging.getLogger(__name__)


def download_file_from_url(storage_id: int, url: str):
    from apps.datasource_media_storages.models import (
        DataSourceMediaStorageConnection,
        DataSourceMediaStorageItem
    )

    import requests

    media_manager = DataSourceMediaStorageConnection.objects.get(
        id=storage_id
    )

    if not media_manager:
        logger.error(f"[tasks.download_file_from_url] Media manager not found: {storage_id}")

        return False

    try:
        file_format = url.split('.')[-1]

        if len(file_format) > 8:
            logger.error(f"[tasks.download_file_from_url] Invalid file format: {file_format}")
            file_format = 'webp'  # Assume WEBP in case of error

    except Exception as e:
        logger.error(f"[tasks.download_file_from_url] Error extracting file format: {e}")
        file_format = 'webp'  # Assume WEBP in case of error

    f_generated = None

    try:
        f_generated = build_media_manager_file_name(
            file_extension=file_format,
            url=url
        )

    except Exception as e:
        logger.error(f"[tasks.download_file_from_url] Error generating file name: {e}")
        pass

    try:
        output = requests.get(url)

        if output.status_code == 200:
            file_data = output.content

            if not f_generated:
                f_generated = f"{uuid.uuid4()}_{uuid.uuid4()}.{filetype.guess(file_data).extension}"

            media_item = DataSourceMediaStorageItem.objects.create(
                storage_base=media_manager,
                media_file_name=f_generated,
                media_file_size=len(file_data),
                media_file_type=file_format,
                file_bytes=file_data
            )

            media_item.save()

        else:
            logger.error(f"[tasks.download_file_from_url] Error downloading file from URL: {url}")

            return False

    except Exception as e:
        logger.error(f"[tasks.download_file_from_url] Error downloading file from URL: {url} - {e}")

        return False

    logger.info(f"[tasks.download_file_from_url] File downloaded successfully from URL: {url}")

    return True


def build_media_manager_file_name(url: str, file_extension: str):
    component = url.split('/')[-1]
    combined_file_name = f"{component}.{file_extension}"

    return combined_file_name
