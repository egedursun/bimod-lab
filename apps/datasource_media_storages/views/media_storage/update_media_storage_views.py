from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection
from apps.datasource_media_storages.utils import MEDIA_CATEGORIES
from apps.organization.models import Organization
from apps.user_permissions.models import PermissionNames
from web_project import TemplateLayout


class DataSourceMediaStorageConnectionUpdateView(LoginRequiredMixin, TemplateView):
    """
    Handles updating an existing media storage connection.

    This view allows users with the appropriate permissions to modify a media storage connection's attributes. It also handles the form submission and validation for updating the connection.

    Methods:
        get_context_data(self, **kwargs): Retrieves the current media storage connection details and adds them to the context, along with other relevant data such as available assistants and media categories.
        post(self, request, *args, **kwargs): Handles form submission for updating the media storage connection, including permission checks and validation.
    """

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
        # PERMISSION CHECK FOR - UPDATE_MEDIA_STORAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_MEDIA_STORAGES):
            messages.error(self.request, "You do not have permission to update media storages.")
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
            print('[DataSourceMediaStorageConnectionUpdateView.post] Data Source Media Storage updated successfully.')
            return redirect('datasource_media_storages:list')
        except Assistant.DoesNotExist:
            messages.error(request, 'Invalid assistant selected.')
            return redirect('datasource_media_storages:update', pk=media_storage.pk)
        except Exception as e:
            messages.error(request, f'Error updating Data Source Media Storage: {e}')
            return redirect('datasource_media_storages:update', pk=media_storage.pk)
