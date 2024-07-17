from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.datasource_file_systems.models import DataSourceFileSystem, DataSourceFileSystemsOsTypeNames, \
    DATASOURCE_FILE_SYSTEMS_OS_TYPES
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


# Create your views here.


class DataSourceFileSystemListCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'datasource_file_systems/create_datasource_file_system.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        organizations = context_user.organizations.filter(
            users__in=[context_user]
        )
        context['assistants'] = Assistant.objects.filter(
            organization__in=organizations
        )
        context['os_choices'] = DATASOURCE_FILE_SYSTEMS_OS_TYPES
        context['user'] = context_user
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - FILE SYSTEMS / CREATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_FILE_SYSTEMS not in user_permissions:
            messages.error(request, "You do not have permission to create a file system connection.")
            return redirect('datasource_file_systems:list')
        ##############################

        name = request.POST.get('name')
        description = request.POST.get('description')
        os_type = request.POST.get('os_type')
        assistant_id = request.POST.get('assistant')
        host_url = request.POST.get('host_url')
        port = request.POST.get('port', 22)
        username = request.POST.get('username')
        password = request.POST.get('password')
        os_read_limit_tokens = request.POST.get('os_read_limit_tokens', 5_000)
        is_read_only = request.POST.get('is_read_only') == 'on'
        created_by_user = request.user

        try:
            assistant = Assistant.objects.get(id=assistant_id)
            data_source = DataSourceFileSystem.objects.create(
                name=name,
                description=description,
                os_type=os_type,
                assistant=assistant,
                host_url=host_url,
                port=port,
                username=username,
                password=password,
                os_read_limit_tokens=os_read_limit_tokens,
                is_read_only=is_read_only,
                created_by_user=created_by_user
            )
            data_source.save()
            messages.success(request, 'Data Source File System created successfully.')
            return redirect('datasource_file_systems:list')
        except Assistant.DoesNotExist:
            messages.error(request, 'Invalid assistant selected.')
            return redirect('datasource_file_systems:create')
        except Exception as e:
            messages.error(request, f'Error creating Data Source File System: {e}')
            return redirect('datasource_file_systems:create')


class DataSourceFileSystemUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'datasource_file_systems/update_datasource_file_system.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        organizations = context_user.organizations.filter(
            users__in=[context_user]
        )
        context['assistants'] = Assistant.objects.filter(
            organization__in=organizations
        )
        context['os_choices'] = DATASOURCE_FILE_SYSTEMS_OS_TYPES
        context['user'] = context_user
        try:
            connection = DataSourceFileSystem.objects.get(pk=kwargs['pk'])
            context['connection'] = connection
        except DataSourceFileSystem.DoesNotExist:
            messages.error(self.request, 'Data Source File System not found.')
            return redirect('datasource_file_systems:list')
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - FILE SYSTEMS / UPDATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.UPDATE_FILE_SYSTEMS not in user_permissions:
            messages.error(request, "You do not have permission to update a file system connection.")
            return redirect('datasource_file_systems:list')
        ##############################

        try:
            connection = get_object_or_404(DataSourceFileSystem, pk=kwargs['pk'])
        except DataSourceFileSystem.DoesNotExist:
            messages.error(request, 'Data Source File System not found.')
            return redirect('datasource_file_systems:list')

        connection.name = request.POST.get('name')
        connection.description = request.POST.get('description')
        connection.os_type = request.POST.get('os_type')
        assistant_id = request.POST.get('assistant')
        connection.host_url = request.POST.get('host_url')
        connection.port = request.POST.get('port', 22)
        connection.username = request.POST.get('username')
        connection.password = request.POST.get('password')
        connection.os_read_limit_tokens = request.POST.get('os_read_limit_tokens', 5_000)
        connection.is_read_only = request.POST.get('is_read_only') == 'on'

        try:
            assistant = Assistant.objects.get(id=assistant_id)
            connection.assistant = assistant
        except Assistant.DoesNotExist:
            messages.error(request, 'Invalid assistant selected.')
            return redirect('datasource_file_systems:update', kwargs={'pk': kwargs['pk']})

        try:
            connection.save()
            messages.success(request, 'Data Source File System updated successfully.')
            return redirect('datasource_file_systems:list')
        except Exception as e:
            messages.error(request, f'Error updating Data Source File System: {e}')
            return redirect('datasource_file_systems:update', kwargs={'pk': kwargs['pk']})


class DataSourceFileSystemsListView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        connections_by_organization = {}
        assistants = Assistant.objects.all()

        for assistant in assistants:
            organization = assistant.organization
            if organization not in connections_by_organization:
                connections_by_organization[organization] = {}
            if assistant not in connections_by_organization[organization]:
                connections_by_organization[organization][assistant] = []

            connections = DataSourceFileSystem.objects.filter(assistant=assistant)
            connections_by_organization[organization][assistant].extend(connections)

        context['connections_by_organization'] = connections_by_organization
        context['user'] = context_user
        return context


class DataSourceFileSystemDeleteView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - FILE SYSTEMS / UPDATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_FILE_SYSTEMS not in user_permissions:
            messages.error(request, "You do not have permission to delete a file system connection.")
            return redirect('datasource_file_systems:list')
        ##############################

        data_source = get_object_or_404(DataSourceFileSystem, pk=kwargs['pk'])
        data_source.delete()
        return redirect('datasource_file_systems:list')
