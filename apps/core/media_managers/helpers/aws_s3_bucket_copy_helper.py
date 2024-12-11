#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: aws_s3_bucket_copy_helper.py
#  Last Modified: 2024-12-04 23:27:12
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-04 23:27:13
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

from apps.datasource_media_storages.models import (
    DataSourceMediaStorageConnection,
    DataSourceMediaStorageItem
)

logger = logging.getLogger(__name__)


class MediaStorageCopyClient__AWSS3Bucket:
    def __init__(
        self,
        aws_access_key_id,
        aws_secret_access_key,
        region_name,
        media_storage_id
    ):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

        self.media_storage_id = media_storage_id

        self.media_storage = DataSourceMediaStorageConnection.objects.get(
            id=media_storage_id
        )

        if not self.media_storage:
            logger.error(
                f"Media storage with ID '{media_storage_id}' not found."
            )

            return

    def copy_file_to_media_storage(
        self,
        file_key,
        file_content
    ):
        # Extract file name from the key
        file_name = file_key.split('/')[-1]
        file_size = len(file_content)
        file_type = file_name.split('.')[-1]

        # Create a new media storage item
        media_item = DataSourceMediaStorageItem(
            storage_base=self.media_storage,
            media_file_name=file_name,
            media_file_type=file_type,
            media_file_size=file_size,
            file_bytes=file_content,
            description=f"Automatically copied file from AWS S3 bucket."
        )

        try:
            media_item.save()
            print(f"File '{file_name}' successfully copied to media storage.")
            logger.info(f"File '{file_name}' successfully copied to media storage.")

        except Exception as e:
            logger.error(f"Failed to copy file '{file_name}' to media storage: {str(e)}")
            raise e

    def execute_copy_process(
        self,
        bucket_name,
        prefix
    ):
        try:


            if prefix:
                if not prefix.endswith('/'):
                    prefix += '/'
            else:
                prefix = ''

            # Fetch objects in the specified bucket and prefix
            response = self.s3_client.list_objects_v2(
                Bucket=bucket_name,
                Prefix=prefix,
                Delimiter='/'
            )

            if 'Contents' not in response:
                print(f"No files found in bucket '{bucket_name}' under prefix '{prefix}'.")
                return []

            for obj in response['Contents']:

                file_key = obj['Key']

                try:

                    # Skip if the key is the prefix itself or contains further slashes
                    if file_key.endswith('/') or '/' in file_key[len(prefix):]:
                        continue

                    # Download the file content
                    file_content = self.s3_client.get_object(
                        Bucket=bucket_name,
                        Key=file_key
                    )['Body'].read()

                    # Store the file in your custom media storage
                    self.copy_file_to_media_storage(file_key, file_content)

                    logger.info(f"File '{file_key}' successfully copied to media storage.")

                except Exception as e:

                    logger.error(f"Failed to copy file '{file_key}' to media storage: {str(e)}")
                    continue

        except Exception as e:

            logger.error(f"Failed to copy files from AWS S3 bucket '{bucket_name}' under prefix '{prefix}': {str(e)}")
            return False

        return True
