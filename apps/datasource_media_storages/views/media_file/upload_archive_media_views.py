#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: upload_zip_media_views.py
#  Last Modified: 2024-12-01 23:44:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-01 23:44:39
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
import tarfile
import zipfile
from io import BytesIO

import rarfile
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_media_storages.models import DataSourceMediaStorageItem, DataSourceMediaStorageConnection
from apps.datasource_media_storages.utils import SUPPORTED_ARCHIVE_TYPES
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class MediaView_ItemArchiveRetrieval(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_STORAGE_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_STORAGE_FILES):
            messages.error(self.request, "You do not have permission to add media files.")
            return redirect('datasource_media_storages:list_items')
        ##############################

        mm_id = request.POST.get('storage_id') or None
        archive_file_data = request.FILES.get('archive_file')

        if not mm_id:
            logger.error('Invalid media storage ID.')
            messages.error(request, 'Invalid media storage ID: [Null]')
            return redirect('datasource_media_storages:create_item')

        try:
            mm_id_int = int(mm_id)

            if not archive_file_data:
                logger.error('No archive file uploaded.')
                messages.error(request, 'No archive file uploaded.')
                return redirect('datasource_media_storages:list_items')

            # Validate the uploaded file type
            if not any(archive_file_data.name.endswith(ext) for ext in SUPPORTED_ARCHIVE_TYPES):
                logger.error('Unsupported file type uploaded.')
                messages.error(
                    request,

                    'The uploaded file type is not supported. Supported types: ZIP, TAR, TAR.GZ, RAR.'
                )
                return redirect('datasource_media_storages:create_item')

            # Process the archive file
            success = retrieve_from_archive_file(
                file_data=archive_file_data,
                storage_id=mm_id_int
            )

            if not success:
                messages.error(request, 'Error while retrieving files from the uploaded archive.')
                return redirect('datasource_media_storages:create_item')

            logger.info('File download from URL initiated.')

        except Exception as e:
            logger.error(f'Error while initiating retrieval from ZIP file: {e}')
            messages.error(request, 'Error while initiating retrieval from ZIP file.')
            return redirect('datasource_media_storages:list_items')

        messages.success(request, 'File retrieval from ZIP file initiated.')
        return redirect('datasource_media_storages:list_items')


def retrieve_from_archive_file(file_data, storage_id):
    try:
        archive_data_files = []
        file_name = file_data.name

        # Handling ZIP files
        if file_name.endswith('.zip'):
            with zipfile.ZipFile(BytesIO(file_data.read())) as archive:
                for file_name in archive.namelist():
                    if not file_name.endswith('/'):
                        archive_data_files.append({
                            'name': file_name,
                            'size': archive.getinfo(file_name).file_size,
                            'content': archive.read(file_name),
                        })

        # Handling TAR and TAR.GZ files
        elif file_name.endswith('.tar') or file_name.endswith('.tar.gz'):
            with tarfile.open(fileobj=BytesIO(file_data.read()), mode='r:*') as archive:
                for member in archive.getmembers():
                    if member.isfile():
                        archive_data_files.append({
                            'name': member.name,
                            'size': member.size,
                            'content': archive.extractfile(member).read(),
                        })

        # Handling RAR files
        elif file_name.endswith('.rar'):
            with rarfile.RarFile(BytesIO(file_data.read())) as archive:
                for member in archive.infolist():
                    if not member.isdir():
                        archive_data_files.append({
                            'name': member.filename,
                            'size': member.file_size,
                            'content': archive.read(member),
                        })

        else:
            logger.error(f"Unsupported file type: {file_name}")
            return False

        # Save extracted files to storage
        storage_manager = DataSourceMediaStorageConnection.objects.get(id=storage_id)

        for item in archive_data_files:
            try:
                DataSourceMediaStorageItem.objects.create(
                    storage_base=storage_manager,
                    media_file_name=item["name"].split('.')[0],
                    media_file_size=item["size"],
                    media_file_type=item["name"].split('.')[-1],
                    file_bytes=item["content"],
                    description=f"File from uploaded archive: {item['name']}"
                )

            except Exception as e:
                logger.error(f'Error while saving file: {e}')
                continue

    except (
        zipfile.BadZipFile,
        tarfile.TarError,
        rarfile.BadRarFile
    ) as e:
        logger.error(f'Bad archive file: {e}')
        return False

    except Exception as e:
        logger.error(f'Error while retrieving files from archive: {e}')
        return False

    logger.info('Files are retrieved from the specified archive file.')
    return True
