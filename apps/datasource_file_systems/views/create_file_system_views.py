from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_file_systems.models import DataSourceFileSystem
from apps.datasource_file_systems.utils import DATASOURCE_FILE_SYSTEMS_OS_TYPES
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DataSourceFileSystemListCreateView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of new data source file system connections.

    This view displays a form for creating a new file system connection. Upon submission, it validates the input, checks user permissions, and saves the new connection to the database. If the user lacks the necessary permissions, an error message is displayed.

    Attributes:
        template_name (str): The template used to render the file system creation form.

    Methods:
        get_context_data(self, **kwargs): Adds additional context to the template, including available assistants, OS choices, and user details.
        post(self, request, *args, **kwargs): Handles form submission and file system connection creation, including permission checks and validation.
    """

    template_name = 'datasource_file_systems/create_datasource_file_system.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        organizations = context_user.organizations.filter(users__in=[context_user])
        context['assistants'] = Assistant.objects.filter(organization__in=organizations)
        context['os_choices'] = DATASOURCE_FILE_SYSTEMS_OS_TYPES
        context['user'] = context_user
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - ADD_FILE_SYSTEMS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_FILE_SYSTEMS):
            messages.error(self.request, "You do not have permission to create a file system connection.")
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
                name=name, description=description, os_type=os_type, assistant=assistant, host_url=host_url,
                port=port, username=username, password=password, os_read_limit_tokens=os_read_limit_tokens,
                is_read_only=is_read_only, created_by_user=created_by_user
            )
            data_source.save()
            messages.success(request, 'Data Source File System created successfully.')
            print('[DataSourceFileSystemListCreateView.post] Data Source File System created successfully.')
            return redirect('datasource_file_systems:list')
        except Assistant.DoesNotExist:
            messages.error(request, 'Invalid assistant selected.')
            return redirect('datasource_file_systems:create')
        except Exception as e:
            messages.error(request, f'Error creating Data Source File System: {e}')
            return redirect('datasource_file_systems:create')
