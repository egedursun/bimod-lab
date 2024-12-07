#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: google_drive_folder_item_copy_helper.py
#  Last Modified: 2024-12-04 23:27:46
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-04 23:27:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import json
import logging
import io

from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from apps.datasource_media_storages.models import (
    DataSourceMediaStorageConnection, DataSourceMediaStorageItem
)

logger = logging.getLogger(__name__)


class MediaStorageCopyClient__GoogleDrive:
    def __init__(
        self,
        credentials_json,
        media_storage_id
    ):

        json_data = credentials_json.decode('utf-8')
        credentials_info = json.loads(json_data)

        creds = service_account.Credentials.from_service_account_info(
            credentials_info
        )

        self.drive_service = build(
            'drive',
            'v3',
            credentials=creds
        )

        self.media_storage_id = media_storage_id

        try:
            self.media_storage = DataSourceMediaStorageConnection.objects.get(
                id=media_storage_id
            )

        except DataSourceMediaStorageConnection.DoesNotExist:

            logger.error(f"Media storage with ID '{media_storage_id}' not found.")
            return

    def copy_file_to_media_storage(self, file_id, file_name):
        request = self.drive_service.files().get_media(
            fileId=file_id
        )

        file_io = io.BytesIO()
        downloader = MediaIoBaseDownload(
            file_io,
            request
        )

        done = False

        while done is False:
            status, done = downloader.next_chunk()

        file_content = file_io.getvalue()
        file_size = len(file_content)
        file_type = file_name.split('.')[-1]

        media_item = DataSourceMediaStorageItem(
            storage_base=self.media_storage,
            media_file_name=file_name,
            media_file_type=file_type,
            media_file_size=file_size,
            file_bytes=file_content,
            description="Automatically copied file from Google Drive."
        )

        try:
            media_item.save()
            logger.info(f"File '{file_name}' successfully copied to media storage.")

        except Exception as e:
            logger.error(f"Failed to copy file '{file_name}' to media storage: {str(e)}")
            raise e

    def execute_copy_process(
        self,
        folder_id
    ):

        query = f"'{folder_id}' in parents"

        response = self.drive_service.files().list(
            q=query,
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=None
        ).execute()

        for file in response.get(
            'files',
            []
        ):
            self.copy_file_to_media_storage(
                file['id'],
                file['name']
            )

        logger.info("File copying completed.")

        return True
