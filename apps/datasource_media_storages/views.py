import os
import re

import boto3
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps._services.llms.helpers.helper_prompts import GENERATE_FILE_DESCRIPTION_QUERY
from apps._services.tools.execution_handlers.storage_query_execution_handler import execute_storage_query
from apps._services.tools.tool_executor import ExecutionTypesNames
from apps.assistants.models import Assistant
from apps.datasource_media_storages.models import MEDIA_CATEGORIES, DataSourceMediaStorageConnection, \
    DataSourceMediaStorageItem
from apps.datasource_media_storages.utils import decode_xlsx, decode_pptx, decode_docx
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission, PermissionNames
from config.settings import MEDIA_URL
from web_project import TemplateLayout

from .tasks import download_file_from_url
from ..multimodal_chat.models import MultimodalChat

FILE_TYPE_HIGHLIGHTING_DECODER = {
    "py": "python", "js": "javascript", "ts": "typescript", "php": "php", "css": "css", "html": "html",
    "java": "java", "c": "c", "cpp": "cpp", "h": "h", "sh": "shell", "go": "golang", "dart": "dart",
    "yml": "yaml", "yaml": "yaml", "sql": "sql", "pkl": "plaintext", "csv": "plaintext",
    "xlsx": "plaintext", "json": "json", "xml": "xml", "tsv": "plaintext", "docx": "plaintext",
    "pptx": "plaintext", "pdf": "plaintext", "txt": "plaintext",
}


class DataSourceMediaStorageConnectionCreateView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        user_organizations = Organization.objects.filter(users__in=[context_user])
        context['assistants'] = Assistant.objects.filter(organization__in=user_organizations)
        context['media_categories'] = MEDIA_CATEGORIES
        context['user'] = context_user
        return context

    def post(self, request, *args, **kwargs):
        # PERMISSION CHECK FOR - MEDIA STORAGE / CREATE
        context_user = self.request.user
        user_permissions = (UserPermission.active_permissions.filter(user=context_user)
                            .all().values_list('permission_type', flat=True))
        if PermissionNames.ADD_MEDIA_STORAGES not in user_permissions:
            messages.error(request, "You do not have permission to create media storages.")
            return redirect('datasource_media_storages:list')

        name = request.POST.get('name')
        description = request.POST.get('description')
        media_category = request.POST.get('media_category')
        assistant_id = request.POST.get('assistant')
        try:
            assistant = Assistant.objects.get(id=assistant_id)
            data_source = DataSourceMediaStorageConnection.objects.create(
                name=name, description=description, media_category=media_category, assistant=assistant
            )
            data_source.save()
            print('[DataSourceMediaStorageConnectionCreateView.post] Data Source Media Storage created successfully.')
            messages.success(request, 'Data Source Media Storage created successfully.')
            return redirect('datasource_media_storages:list')
        except Assistant.DoesNotExist:
            messages.error(request, 'Invalid assistant selected.')
            return redirect('datasource_media_storages:create')
        except Exception as e:
            messages.error(request, f'Error creating Data Source Media Storage: {e}')
            return redirect('datasource_media_storages:create')


class DataSourceListMediaStorageConnectionsView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        organizations = Organization.objects.filter(users__in=[self.request.user])
        data = []
        for org in organizations:
            assistants = Assistant.objects.filter(organization=org)
            assistant_data_list = []
            for assistant in assistants:
                media_storages = DataSourceMediaStorageConnection.objects.filter(assistant=assistant)
                storage_data_list = []
                for storage in media_storages:
                    storage_data_list.append({'storage': storage})
                assistant_data_list.append({'assistant': assistant, 'media_storages': storage_data_list})
            data.append({'organization': org, 'assistants': assistant_data_list})
        context['data'] = data
        return context

    def post(self, request, *args, **kwargs):
        storage_ids = request.POST.getlist('selected_storages')
        if storage_ids:
            DataSourceMediaStorageConnection.objects.filter(id__in=storage_ids).delete()
            messages.success(request, 'Selected storage connections deleted successfully.')
        return redirect('datasource_media_storages:list')


class DataSourceMediaStorageConnectionUpdateView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        media_storage = get_object_or_404(DataSourceMediaStorageConnection, pk=kwargs['pk'])
        user_organizations = Organization.objects.filter(users__in=[context_user])
        context['assistants'] = Assistant.objects.filter(organization__in=user_organizations)
        context['media_categories'] = MEDIA_CATEGORIES
        context['user'] = context_user
        context['connection'] = media_storage
        return context

    def post(self, request, *args, **kwargs):
        # PERMISSION CHECK FOR - MEDIA STORAGE / UPDATE
        context_user = self.request.user
        user_permissions = (UserPermission.active_permissions.filter(user=context_user)
                            .all().values_list('permission_type', flat=True))
        if PermissionNames.UPDATE_MEDIA_STORAGES not in user_permissions:
            messages.error(request, "You do not have permission to update media storages.")
            return redirect('datasource_media_storages:list')

        media_storage = get_object_or_404(DataSourceMediaStorageConnection, pk=kwargs['pk'])
        name = request.POST.get('name')
        description = request.POST.get('description')
        media_category = request.POST.get('media_category')
        assistant_id = request.POST.get('assistant')

        try:
            assistant = Assistant.objects.get(id=assistant_id)
            media_storage.name = name
            media_storage.description = description
            media_storage.media_category = media_category
            media_storage.assistant = assistant
            media_storage.save()
            messages.success(request, 'Data Source Media Storage updated successfully.')
            print('[DataSourceMediaStorageConnectionUpdateView.post] Data Source Media Storage updated successfully.')
            return redirect('datasource_media_storages:list')
        except Assistant.DoesNotExist:
            messages.error(request, 'Invalid assistant selected.')
            return redirect('datasource_media_storages:update', pk=media_storage.pk)
        except Exception as e:
            messages.error(request, f'Error updating Data Source Media Storage: {e}')
            return redirect('datasource_media_storages:update', pk=media_storage.pk)


class DataSourceMediaStorageConnectionDeleteView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        media_storage = get_object_or_404(DataSourceMediaStorageConnection, pk=kwargs['pk'])
        context['user'] = context_user
        context['media_storage'] = media_storage
        return context

    def post(self, request, *args, **kwargs):
        # PERMISSION CHECK FOR - MEDIA STORAGE / CREATE
        context_user = self.request.user
        user_permissions = (UserPermission.active_permissions.filter(user=context_user)
                            .all().values_list('permission_type', flat=True))
        if PermissionNames.DELETE_MEDIA_STORAGES not in user_permissions:
            messages.error(request, "You do not have permission to delete media storages.")
            return redirect('datasource_media_storages:list')

        media_storage = get_object_or_404(DataSourceMediaStorageConnection, pk=kwargs['pk'])
        media_storage.delete()
        print('[DataSourceMediaStorageConnectionDeleteView.post] Data Source Media Storage deleted successfully.')
        messages.success(request, 'Media Storage Connection deleted successfully.')
        return redirect('datasource_media_storages:list')


class DataSourceMediaStorageItemCreateView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        user_assistants = Assistant.objects.filter(organization__users__in=[request.user])
        media_storages = DataSourceMediaStorageConnection.objects.filter(assistant__in=user_assistants)
        organizations = Organization.objects.filter(users__in=[request.user])

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = list(organizations.values('id', 'name'))
        context['assistants'] = list(user_assistants.values('id', 'name', 'organization_id'))
        context['media_storages'] = list(media_storages.values('id', 'name', 'assistant_id'))
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        media_storage_id = request.POST.get('media_storage') or None
        # PERMISSION CHECK FOR - MEDIA ITEM / CREATE
        context_user = self.request.user
        user_permissions = (UserPermission.active_permissions.filter(user=context_user)
                            .all().values_list('permission_type', flat=True))
        if PermissionNames.ADD_MEDIA_STORAGES not in user_permissions:
            messages.error(request, "You do not have permission to create media items.")
            return redirect('datasource_media_storages:list_items')

        if not media_storage_id:
            messages.error(request, 'Please select a media storage.')
            return redirect('datasource_media_storages:create_item')
        media_storage = DataSourceMediaStorageConnection.objects.get(pk=media_storage_id)
        files = request.FILES.getlist('media_files')
        descriptions = request.POST.getlist('file_descriptions[]')
        if media_storage_id and files:
            for file, description in zip(files, descriptions):
                try:
                    file_bytes = file.read()
                except Exception as e:
                    messages.error(request, f'Error reading file: {e}')
                    continue
                media_storage_item = DataSourceMediaStorageItem.objects.create(
                    storage_base=media_storage,
                    media_file_name=file.name.split('.')[0],
                    media_file_size=file.size,
                    media_file_type=file.name.split('.')[-1],
                    file_bytes=file_bytes,
                    description=description
                )
                media_storage_item.save()
            print('[DataSourceMediaStorageItemCreateView.post] Files uploaded successfully.')
            messages.success(request, 'Files uploaded successfully.')
            return redirect('datasource_media_storages:list_items')
        else:
            messages.error(request, 'Please select a media storage and upload files.')
        return redirect('datasource_media_storages:create_item')


class DataSourceMediaStorageItemDetailAndUpdateView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        media_item = DataSourceMediaStorageItem.objects.get(id=kwargs['pk'])
        context['media_item'] = media_item
        # download file bytes from s3
        file_bytes = None
        if media_item.full_file_path is not None:
            try:
                boto3_client = boto3.client('s3')
                bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
                file_bytes = boto3_client.get_object(Bucket=bucket_name, Key=media_item.full_file_path.split(MEDIA_URL)[1])
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
        # PERMISSION CHECK FOR - MEDIA ITEM / UPDATE
        context_user = self.request.user
        user_permissions = (UserPermission.active_permissions.filter(user=context_user)
                            .all().values_list('permission_type', flat=True))
        if PermissionNames.UPDATE_MEDIA_STORAGES not in user_permissions:
            messages.error(request, "You do not have permission to update media items.")
            return redirect('datasource_media_storages:list_items')

        media_item = DataSourceMediaStorageItem.objects.get(id=kwargs['pk'])
        description = request.POST.get('description')
        media_item.description = description
        media_item.save()
        messages.success(request, 'Media item updated successfully.')
        print('[DataSourceMediaStorageItemDetailAndUpdateView.post] Media item updated successfully.')
        return redirect('datasource_media_storages:list_items')


class DataSourceMediaStorageItemListView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        organizations = Organization.objects.filter(users__in=[self.request.user])
        data = []
        for org in organizations:
            assistants = Assistant.objects.filter(organization=org)
            assistant_data_list = []
            for assistant in assistants:
                media_storages = DataSourceMediaStorageConnection.objects.filter(assistant=assistant)
                storage_data_list = []
                for storage in media_storages:
                    items = DataSourceMediaStorageItem.objects.filter(storage_base=storage).order_by('-created_at')
                    paginator = Paginator(items, 5)  # 5 items per page
                    page_number = self.request.GET.get('page')
                    page_obj = paginator.get_page(page_number)

                    item_data_list = []
                    for item in page_obj:
                        item_data_list.append({'item': item, })
                    storage_data_list.append({'storage': storage, 'items': page_obj, 'item_data': item_data_list, })
                assistant_data_list.append({'assistant': assistant, 'media_storages': storage_data_list, })
            data.append({'organization': org, 'assistants': assistant_data_list, })
        context['data'] = data
        return context

    def post(self, request, *args, **kwargs):
        # PERMISSION CHECK FOR - MEDIA ITEM / DELETE
        context_user = self.request.user
        user_permissions = (UserPermission.active_permissions.filter(user=context_user)
                            .all().values_list('permission_type', flat=True))
        if PermissionNames.DELETE_MEDIA_STORAGES not in user_permissions:
            messages.error(request, "You do not have permission to delete media items.")
            return redirect('datasource_media_storages:list_items')

        if 'selected_items' in request.POST:
            item_ids = request.POST.getlist('selected_items')
            items_to_be_deleted = DataSourceMediaStorageItem.objects.filter(id__in=item_ids)
            for item in items_to_be_deleted:
                if item.full_file_path is not None:
                    try:
                        pass
                    except Exception as e:
                        print(f"Error deleting the file from the media storage path: {item.full_file_path} // {e}")
            DataSourceMediaStorageItem.objects.filter(id__in=item_ids).delete()
            messages.success(request, 'Selected media files deleted successfully.')
            print('[DataSourceMediaStorageItemListView.post] Selected media files deleted successfully.')
        return redirect('datasource_media_storages:list_items')


class DataSourceMediaStorageAllItemsDeleteView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        context = self.post(request, *args, **kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # PERMISSION CHECK FOR - MEDIA ITEM / DELETE
        context_user = self.request.user
        user_permissions = (UserPermission.active_permissions.filter(user=context_user)
                            .all().values_list('permission_type', flat=True))
        if PermissionNames.DELETE_MEDIA_STORAGES not in user_permissions:
            messages.error(request, "You do not have permission to delete media items.")
            return redirect('datasource_media_storages:list_items')

        base_id = kwargs.get('id')
        all_items = DataSourceMediaStorageItem.objects.filter(storage_base_id=base_id)
        for item in all_items:
            if item.full_file_path is not None:
                try:
                    os.system(f"rm -rf {item.full_file_path}")
                except Exception as e:
                    print(f"Error deleting the file from the media storage path: {item.full_file_path} // {e}")
        DataSourceMediaStorageItem.objects.filter(storage_base_id=base_id).delete()
        messages.success(request, 'All media files deleted successfully.')
        print('[DataSourceMediaStorageAllItemsDeleteView.post] All media files deleted successfully.')
        return redirect('datasource_media_storages:list_items')


class DataSourceMediaStorageItemGenerateDescription(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        if 'generated_description' in kwargs:
            context['generated_description'] = kwargs['generated_description']
            print(f"Generated Description: {kwargs['generated_description']}")
        return context

    @staticmethod
    def decode_media_item_type(media_item_type):
        class MediaFileTypesNamesLists:
            IMAGE = ['jpg', 'png', 'gif', 'svg', 'bmp', 'tiff']
            AUDIO = ['mp3', 'wav', 'flac', 'aac', 'ogg']
            VIDEO = ['mp4', 'avi', 'mkv', 'mov']
            COMPRESSED = ['zip', 'rar', 'tar']
            CODE = ['py', 'js', 'ts', 'php', 'css', 'html', 'java', 'c', 'cpp', 'h', 'sh', 'go', 'dart']
            DATA = ['yml', 'yaml', 'sql', 'pkl', 'csv', 'xlsx', 'json', 'xml', 'tsv', 'docx', 'pptx', 'pdf', 'txt']

        if media_item_type in MediaFileTypesNamesLists.IMAGE:
            return ExecutionTypesNames.IMAGE_INTERPRETATION
        elif media_item_type in (MediaFileTypesNamesLists.COMPRESSED or
                                 media_item_type in MediaFileTypesNamesLists.DATA or
                                 media_item_type in MediaFileTypesNamesLists.CODE):
            return ExecutionTypesNames.FILE_INTERPRETATION
        else:
            # assume file interpretation
            return ExecutionTypesNames.FILE_INTERPRETATION

    @staticmethod
    def normalize_whitespace(text):
        # Remove leading and trailing whitespace
        text = text.strip()
        text = text.replace('\n', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\t', ' ')
        text = text.replace('\v', ' ')
        text = text.replace('\f', ' ')
        text = text.replace('\0', ' ')
        text = text.strip()
        # Replace all sequences of whitespace (including newlines, tabs, etc.) with a single space
        text = re.sub(r'\s+', ' ', text, flags=re.UNICODE)
        return text

    def post(self, request, *args, **kwargs):
        # PERMISSION CHECK FOR - MEDIA ITEM / UPDATE
        context_user = self.request.user
        user_permissions = (UserPermission.active_permissions.filter(user=context_user)
                            .all().values_list('permission_type', flat=True))
        if PermissionNames.UPDATE_MEDIA_STORAGES not in user_permissions:
            messages.error(request, "You do not have permission to update media items.")
            return redirect('datasource_media_storages:list_items')

        media_item_id = kwargs.get('pk')
        media_item = DataSourceMediaStorageItem.objects.get(id=media_item_id)
        execution_type = self.decode_media_item_type(media_item.media_file_type)
        texts, _, _ = execute_storage_query(chat_id=None,
                                            connection_id=media_item.storage_base.id,
                                            execution_type=execution_type,
                                            file_paths=[media_item.full_file_path],
                                            query=(GENERATE_FILE_DESCRIPTION_QUERY + f"""
                                                    File Type Information:
                                                    - Format: {media_item.media_file_type}
                                               """),
                                            without_chat=True)
        kwargs['pk'] = media_item_id
        if execution_type == ExecutionTypesNames.IMAGE_INTERPRETATION:
            generated_description = texts
            media_item.description = generated_description
            media_item.save()
        elif execution_type == ExecutionTypesNames.FILE_INTERPRETATION:
            try:
                response = texts["response"]
                generated_description = ""
                if response:
                    generated_description = response[0]
                # remove everything except a single space
                generated_description = self.normalize_whitespace(generated_description)
                media_item.description = generated_description
                media_item.save()
            except Exception as e:
                print(f"Error parsing generated description: {e}")
        return redirect('datasource_media_storages:item_detail', **kwargs)


class DataSourceMediaStorageItemFetchFileFromUrl(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # PERMISSION CHECK FOR - MEDIA ITEM / CREATE
        context_user = self.request.user
        user_permissions = (UserPermission.active_permissions.filter(user=context_user)
                            .all().values_list('permission_type', flat=True))
        if PermissionNames.ADD_MEDIA_STORAGES not in user_permissions:
            messages.error(request, "You do not have permission to create media items.")
            return redirect('datasource_media_storages:list_items')
        media_storage_id = request.POST.get('storage_id') or None
        if not media_storage_id:
            messages.error(request, 'Invalid media storage ID.')
            return redirect('datasource_media_storages:create_item')
        download_url = request.POST.get('download_url') or None
        if not download_url:
            messages.error(request, 'Invalid download URL.')
            return redirect('datasource_media_storages:create_item')
        media_storage_id_int = int(media_storage_id)
        download_file_from_url.delay(storage_id=media_storage_id_int, url=download_url)
        messages.success(request, 'File download from URL initiated.')
        print('[DataSourceMediaStorageItemFetchFileFromUrl.post] File download from URL initiated.')
        return redirect('datasource_media_storages:list_items')


class DataSourceMediaStorageGeneratedItemsListView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        organizations = Organization.objects.filter(users__in=[self.request.user])
        data = []
        for org in organizations:
            assistants = Assistant.objects.filter(organization=org)
            assistant_data_list = []
            for assistant in assistants:
                multimodal_chats_of_assistants = MultimodalChat.objects.filter(assistant=assistant)
                messages_with_images = []
                messages_with_files = []
                for chat in multimodal_chats_of_assistants:
                    file_or_image_messages = chat.chat_messages.filter(Q(message_image_contents__isnull=False) |
                                                                       Q(message_file_contents__isnull=False))
                    for m in file_or_image_messages:
                        if m.message_image_contents:
                            for img in m.message_image_contents:
                                message_data = {'message': m, 'image': img}
                                messages_with_images.append(message_data)
                        if m.message_file_contents:
                            for file in m.message_file_contents:
                                message_data = {'message': m, 'file': file}
                                messages_with_files.append(message_data)
                # prepare paginated images
                paginator_images = Paginator(messages_with_images, 5)  # 5 items per page
                page_number_images = self.request.GET.get('page_images')
                page_obj_images = paginator_images.get_page(page_number_images)
                # prepare paginated files
                paginator_files = Paginator(messages_with_files, 5)
                page_number_files = self.request.GET.get('page_files')
                page_obj_files = paginator_files.get_page(page_number_files)
                assistant_data_list.append({'assistant': assistant, 'messages_with_images': page_obj_images,
                                            'messages_with_files': page_obj_files})
            data.append({'organization': org, 'assistants': assistant_data_list, })
        context['data'] = data
        print(data)
        context['base_url'] = MEDIA_URL
        return context

    def post(self, request, *args, **kwargs):
        # PERMISSION CHECK FOR - MEDIA ITEM / DELETE
        context_user = self.request.user
        user_permissions = (UserPermission.active_permissions.filter(user=context_user)
                            .all().values_list('permission_type', flat=True))
        if PermissionNames.DELETE_MEDIA_STORAGES not in user_permissions:
            messages.error(request, "You do not have permission to delete generated media items.")
            return redirect('datasource_media_storages:list_items')

        if 'selected_items' in request.POST:
            item_ids = request.POST.getlist('selected_items')
            items_to_be_deleted = DataSourceMediaStorageItem.objects.filter(id__in=item_ids)
            for item in items_to_be_deleted:
                if item.full_file_path is not None:
                    try:
                        # delete from s3
                        boto3_client = boto3.client('s3')
                        bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
                        boto3_client.delete_object(Bucket=bucket_name, Key=item.full_file_path.split(MEDIA_URL)[1])
                    except Exception as e:
                        print(
                            f"Error deleting the generated file from the media storage path: {item.full_file_path} // {e}")
            DataSourceMediaStorageItem.objects.filter(id__in=item_ids).delete()
            messages.success(request, 'Selected generated media files deleted successfully.')
            print('[DataSourceMediaStorageGeneratedItemsListView.post] Selected generated media files deleted successfully.')
        return redirect('datasource_media_storages:list_items')
