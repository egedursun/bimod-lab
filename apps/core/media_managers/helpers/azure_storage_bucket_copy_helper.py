#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: azure_storage_bucket_copy_helper.py
#  Last Modified: 2024-12-04 23:27:32
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-04 23:27:33
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

from azure.storage.blob import BlobServiceClient

from apps.datasource_media_storages.models import (
    DataSourceMediaStorageConnection,
    DataSourceMediaStorageItem
)

logger = logging.getLogger(__name__)


class MediaStorageCopyClient__AzureBlob:
    def __init__(
        self,
        account_name,
        account_key,
        container_name,
        media_storage_id
    ):
        self.account_name = account_name
        self.account_key = account_key
        self.container_name = container_name
        self.media_storage_id = media_storage_id

        connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"

        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)

        try:
            self.media_storage = DataSourceMediaStorageConnection.objects.get(
                id=media_storage_id
            )

        except DataSourceMediaStorageConnection.DoesNotExist:
            logger.error(
                f"Media storage with ID '{media_storage_id}' not found."
            )

    def copy_file_to_media_storage(self, blob_name, blob_content):
        file_name = blob_name.split('/')[-1]
        file_size = len(blob_content)
        file_type = file_name.split('.')[-1]

        media_item = DataSourceMediaStorageItem(
            storage_base=self.media_storage,
            media_file_name=file_name,
            media_file_type=file_type,
            media_file_size=file_size,
            file_bytes=blob_content,
            description="Automatically copied file from Azure blob."
        )

        try:
            media_item.save()
            logger.info(f"File '{file_name}' successfully copied to media storage.")
        except Exception as e:
            logger.error(f"Failed to copy file '{file_name}' to media storage: {str(e)}")

            raise e

    def execute_copy_process(self, prefix=''):
        try:
            blob_list = self.container_client.list_blobs(
                name_starts_with=prefix
            )

            for blob in blob_list:
                blob_client = self.container_client.get_blob_client(blob)
                blob_content = blob_client.download_blob().readall()

                self.copy_file_to_media_storage(blob.name, blob_content)
                logger.info(f"File '{blob.name}' successfully copied to media storage.")

        except Exception as e:
            logger.error(f"Failed to copy files from Azure blob container under prefix '{prefix}': {str(e)}")

            return False

        return True
