import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.datasource_media_storages.models import MEDIA_CATEGORIES, DataSourceMediaStorageConnection, \
    DataSourceMediaStorageItem
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


# Create your views here.


class DataSourceMediaStorageConnectionCreateView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        user_organizations = Organization.objects.filter(
            users__in=[context_user]
        )
        context['assistants'] = Assistant.objects.filter(
            organization__in=user_organizations
        )
        context['media_categories'] = MEDIA_CATEGORIES
        context['user'] = context_user
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - MEDIA STORAGE / CREATE
        ##############################
        context_user = self.request.user
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_MEDIA_STORAGES not in user_permissions:
            messages.error(request, "You do not have permission to create media storages.")
            return redirect('datasource_media_storages:list')
        ##############################

        name = request.POST.get('name')
        description = request.POST.get('description')
        media_category = request.POST.get('media_category')
        assistant_id = request.POST.get('assistant')

        try:
            assistant = Assistant.objects.get(id=assistant_id)
            data_source = DataSourceMediaStorageConnection.objects.create(
                name=name,
                description=description,
                media_category=media_category,
                assistant=assistant
            )
            data_source.save()
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
                    storage_data_list.append({
                        'storage': storage,
                    })
                assistant_data_list.append({
                    'assistant': assistant,
                    'media_storages': storage_data_list,
                })
            data.append({
                'organization': org,
                'assistants': assistant_data_list,
            })
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

        ##############################
        # PERMISSION CHECK FOR - MEDIA STORAGE / UPDATE
        ##############################
        context_user = self.request.user
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.UPDATE_MEDIA_STORAGES not in user_permissions:
            messages.error(request, "You do not have permission to update media storages.")
            return redirect('datasource_media_storages:list')
        ##############################

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
        ##############################
        # PERMISSION CHECK FOR - MEDIA STORAGE / CREATE
        ##############################
        context_user = self.request.user
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_MEDIA_STORAGES not in user_permissions:
            messages.error(request, "You do not have permission to delete media storages.")
            return redirect('datasource_media_storages:list')
        ##############################

        media_storage = get_object_or_404(DataSourceMediaStorageConnection, pk=kwargs['pk'])
        media_storage.delete()
        messages.success(request, 'Media Storage Connection deleted successfully.')
        return redirect('datasource_media_storages:list')


##################################################################################################################


class DataSourceMediaStorageItemCreateView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        user_assistants = Assistant.objects.filter(organization__users__in=[request.user])
        media_storages = DataSourceMediaStorageConnection.objects.filter(
            assistant__in=user_assistants
        )
        organizations = Organization.objects.filter(users__in=[request.user])

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = list(organizations.values('id', 'name'))
        context['assistants'] = list(user_assistants.values('id', 'name', 'organization_id'))
        context['media_storages'] = list(media_storages.values('id', 'name', 'assistant_id'))
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        media_storage_id = request.POST.get('media_storage') or None

        ##############################
        # PERMISSION CHECK FOR - MEDIA ITEM / CREATE
        ##############################
        context_user = self.request.user
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_MEDIA_STORAGES not in user_permissions:
            messages.error(request, "You do not have permission to create media items.")
            return redirect('datasource_media_storages:list_items')
        ##############################

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

            messages.success(request, 'Files uploaded successfully.')
            return redirect('datasource_media_storages:list_items')
        else:
            messages.error(request, 'Please select a media storage and upload files.')
        return redirect('datasource_media_storages:create_item')


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
                        item_data_list.append({
                            'item': item, })
                    storage_data_list.append({
                        'storage': storage,
                        'items': page_obj,
                        'item_data': item_data_list, })
                assistant_data_list.append({
                    'assistant': assistant,
                    'media_storages': storage_data_list, })
            data.append({
                'organization': org,
                'assistants': assistant_data_list, })
        context['data'] = data
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - MEDIA ITEM / DELETE
        ##############################
        context_user = self.request.user
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_MEDIA_STORAGES not in user_permissions:
            messages.error(request, "You do not have permission to delete media items.")
            return redirect('datasource_media_storages:list_items')
        ##############################

        if 'selected_items' in request.POST:
            item_ids = request.POST.getlist('selected_items')
            items_to_be_deleted = DataSourceMediaStorageItem.objects.filter(id__in=item_ids)
            for item in items_to_be_deleted:
                if item.full_file_path is not None:
                    try:
                        os.system(f"rm -rf {item.full_file_path}")
                    except Exception as e:
                        print(f"Error deleting the file from the media storage path: {item.full_file_path} // {e}")
            DataSourceMediaStorageItem.objects.filter(id__in=item_ids).delete()
            messages.success(request, 'Selected media files deleted successfully.')
        return redirect('datasource_media_storages:list_items')


class DataSourceMediaStorageAllItemsDeleteView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        context = self.post(request, *args, **kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - MEDIA ITEM / DELETE
        ##############################
        context_user = self.request.user
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_MEDIA_STORAGES not in user_permissions:
            messages.error(request, "You do not have permission to delete media items.")
            return redirect('datasource_media_storages:list_items')
        ##############################

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
        return redirect('datasource_media_storages:list_items')
