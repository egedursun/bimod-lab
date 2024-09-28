import os

import boto3
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_media_storages.models import DataSourceMediaStorageItem
from apps.datasource_media_storages.utils import decode_docx, decode_pptx, decode_xlsx, FILE_TYPE_HIGHLIGHTING_DECODER
from apps.user_permissions.utils import PermissionNames
from config.settings import MEDIA_URL
from web_project import TemplateLayout


class DataSourceMediaStorageItemDetailAndUpdateView(LoginRequiredMixin, TemplateView):
    """
    Displays and updates the details of a specific media storage item.

    This view allows users with the appropriate permissions to view and update the details of a media storage item. It also retrieves the file contents from the storage (e.g., S3) and decodes them for display.

    Methods:
        get_context_data(self, **kwargs): Retrieves the media storage item details and decodes the file contents for display.
        post(self, request, *args, **kwargs): Handles the update of the media storage item's description.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_STORAGE_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_STORAGE_FILES):
            messages.error(self.request, "You do not have permission to see media files.")
            return context
        ##############################

        media_item = DataSourceMediaStorageItem.objects.get(id=kwargs['pk'])
        context['media_item'] = media_item
        # download file bytes from s3
        file_bytes = None
        if media_item.full_file_path is not None:
            try:
                boto3_client = boto3.client('s3')
                bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
                file_bytes = boto3_client.get_object(Bucket=bucket_name,
                                                     Key=media_item.full_file_path.split(MEDIA_URL)[1])
                file_bytes = file_bytes['Body'].read()
            except Exception as e:
                print(f"[DataSourceMediaStorageItemDetailAndUpdateView.get_context_data] Error downloading file: {e}")
        # decode binary data to string
        media_item_contents = "File contents could not be decoded."
        try:
            if media_item.media_file_type == 'txt':
                media_item_contents = file_bytes.decode('utf-8')
            elif media_item.media_file_type == 'docx':
                media_item_contents = decode_docx(file_bytes)
            elif media_item.media_file_type == 'pptx':
                media_item_contents = decode_pptx(file_bytes)
            elif media_item.media_file_type == 'xlsx':
                media_item_contents = decode_xlsx(file_bytes)
            else:
                media_item_contents = file_bytes.decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"[DataSourceMediaStorageItemDetailAndUpdateView.get_context_data] Error decoding binary data: {e}")
        context['media_item_contents'] = media_item_contents
        context['file_type_highlighting'] = FILE_TYPE_HIGHLIGHTING_DECODER.get(media_item.media_file_type, 'plaintext')
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - UPDATE_STORAGE_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_STORAGE_FILES):
            messages.error(self.request, "You do not have permission to update media files.")
            return redirect('datasource_media_storages:list_items')
        ##############################

        media_item = DataSourceMediaStorageItem.objects.get(id=kwargs['pk'])
        description = request.POST.get('description')
        media_item.description = description
        media_item.save()
        messages.success(request, 'Media item updated successfully.')
        print('[DataSourceMediaStorageItemDetailAndUpdateView.post] Media item updated successfully.')
        return redirect('datasource_media_storages:list_items')
