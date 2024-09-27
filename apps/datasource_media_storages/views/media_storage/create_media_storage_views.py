from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection
from apps.datasource_media_storages.utils import MEDIA_CATEGORIES
from apps.organization.models import Organization
from apps.user_permissions.models import PermissionNames
from web_project import TemplateLayout


class DataSourceMediaStorageConnectionCreateView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of new media storage connections.

    This view displays a form for creating a new media storage connection. Upon submission, it validates the input, checks user permissions, and saves the new connection to the database. If the user lacks the necessary permissions, an error message is displayed.

    Methods:
        get_context_data(self, **kwargs): Adds additional context to the template, including available assistants, media categories, and user details.
        post(self, request, *args, **kwargs): Handles form submission and media storage connection creation, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        user_organizations = Organization.objects.filter(users__in=[context_user])
        context['assistants'] = Assistant.objects.filter(organization__in=user_organizations)
        context['media_categories'] = MEDIA_CATEGORIES
        context['user'] = context_user
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_MEDIA_STORAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_MEDIA_STORAGES):
            messages.error(self.request, "You do not have permission to create media storages.")
            return redirect('datasource_media_storages:list')
        ##############################

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
