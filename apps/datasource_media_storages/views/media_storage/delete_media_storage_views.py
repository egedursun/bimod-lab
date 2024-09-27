from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection
from apps.user_permissions.models import PermissionNames
from web_project import TemplateLayout


class DataSourceMediaStorageConnectionDeleteView(LoginRequiredMixin, TemplateView):
    """
    Handles the deletion of a media storage connection.

    This view allows users with the appropriate permissions to delete a media storage connection. It ensures that the user has the necessary permissions before performing the deletion.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for rendering the confirmation of the deletion.
        post(self, request, *args, **kwargs): Deletes the media storage connection if the user has the required permissions.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        media_storage = get_object_or_404(DataSourceMediaStorageConnection, pk=kwargs['pk'])
        context['user'] = context_user
        context['media_storage'] = media_storage
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_MEDIA_STORAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_MEDIA_STORAGES):
            messages.error(self.request, "You do not have permission to delete media storages.")
            return redirect('datasource_media_storages:list')
        ##############################

        media_storage = get_object_or_404(DataSourceMediaStorageConnection, pk=kwargs['pk'])
        media_storage.delete()
        print('[DataSourceMediaStorageConnectionDeleteView.post] Data Source Media Storage deleted successfully.')
        messages.success(request, 'Media Storage Connection deleted successfully.')
        return redirect('datasource_media_storages:list')
