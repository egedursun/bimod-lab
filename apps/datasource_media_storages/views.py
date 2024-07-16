import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.datasource_media_storages.models import MEDIA_CATEGORIES, DataSourceMediaStorageConnection, \
    DataSourceMediaStorageItem
from apps.organization.models import Organization
from web_project import TemplateLayout


# Create your views here.


# TODO: create the views for the media storages here


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

        if not media_storage_id:
            messages.error(request, 'Please select a media storage.')
            return redirect('datasource_media_storages:create_item')
        media_storage = DataSourceMediaStorageConnection.objects.get(pk=media_storage_id)
        files = request.FILES.getlist('media_files')
        if media_storage_id and files:
            for file in files:
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
                    file_bytes=file_bytes
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
        context['user'] = self.request.user
        return context


class DataSourceMediaStorageAllItemsDeleteView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['user'] = self.request.user
        return context
