#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: gcp_storage_bucket_copy_helper.py
#  Last Modified: 2024-12-05 14:24:29
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-05 14:26:01
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
from google.cloud import storage
from google.oauth2 import service_account

from apps.datasource_media_storages.models import (
    DataSourceMediaStorageConnection, DataSourceMediaStorageItem
)

logger = logging.getLogger(__name__)


class MediaStorageCopyClient__GCSBucket:
    def __init__(self, service_account_info, media_storage_id):

        credentials = service_account.Credentials.from_service_account_info(
            service_account_info
        )

        self.gcs_client = storage.Client(
            credentials=credentials,
            project=service_account_info['project_id']
        )

        self.media_storage_id = media_storage_id

        try:
            self.media_storage = DataSourceMediaStorageConnection.objects.get(
                id=media_storage_id
            )

        except DataSourceMediaStorageConnection.DoesNotExist:
            logger.error(
                f"Media storage with ID '{media_storage_id}' not found."
            )
            return

    def copy_file_to_media_storage(self, file_blob):
        file_name = file_blob.name.split('/')[-1]
        file_content = file_blob.download_as_bytes()
        file_size = len(file_content)
        file_type = file_name.split('.')[-1]

        media_item = DataSourceMediaStorageItem(
            storage_base=self.media_storage,
            media_file_name=file_name,
            media_file_type=file_type,
            media_file_size=file_size,
            file_bytes=file_content,
            description=f"Automatically copied file from GCS bucket."
        )

        try:
            media_item.save()
            print(f"File '{file_name}' successfully copied to media storage.")
            logger.info(f"File '{file_name}' successfully copied to media storage.")

        except Exception as e:
            logger.error(f"Failed to copy file '{file_name}' to media storage: {str(e)}")
            raise e

    def execute_copy_process(self, bucket_name, prefix=''):
        try:
            bucket = self.gcs_client.get_bucket(bucket_name)
            blobs = list(bucket.list_blobs(prefix=prefix))  # Convert iterator to list immediately

            if not blobs:
                print(f"No files found in bucket '{bucket_name}' under prefix '{prefix}'.")
                return []

            for blob in blobs:
                if blob.name.endswith('/') or '/' in blob.name[len(prefix):]:
                    continue

                self.copy_file_to_media_storage(blob)
                logger.info(f"File '{blob.name}' successfully copied to media storage.")

        except Exception as e:
            logger.error(f"Failed to copy files from GCS bucket '{bucket_name}' under prefix '{prefix}': {str(e)}")
            return False

        return True

