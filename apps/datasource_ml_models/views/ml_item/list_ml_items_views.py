from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_ml_models.models import DataSourceMLModelConnection, DataSourceMLModelItem
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DataSourceMLModelItemListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of machine learning model items associated with the user's ML model connections.

    This view retrieves all ML model items within the user's ML model connections, organized by organization and assistant. It also allows users to delete selected ML model items.

    Attributes:
        template_name (str): The template used to render the ML model item list.

    Methods:
        get_context_data(self, **kwargs): Retrieves the ML model items for the user's connections and adds them to the context, including pagination and status information.
        post(self, request, *args, **kwargs): Handles the deletion of selected ML model items or all items in a connection.
    """

    template_name = 'datasource_ml_models/models/list_datasource_ml_model_items.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_ML_MODEL_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_ML_MODEL_FILES):
            messages.error(self.request, "You do not have permission to list ML Model files.")
            return context
        ##############################

        context_user = self.request.user
        connections_by_organization = []
        organizations = context_user.organizations.all()

        for organization in organizations:
            assistants_data = []
            assistants = Assistant.objects.filter(organization=organization)
            for assistant in assistants:
                connections_data = []
                connections = DataSourceMLModelConnection.objects.filter(assistant=assistant)
                for connection in connections:
                    items = DataSourceMLModelItem.objects.filter(ml_model_base=connection)
                    # Pagination
                    page = self.request.GET.get('page', 1)
                    paginator = Paginator(items, 5)  # Show 5 items per page
                    try:
                        paginated_items = paginator.page(page)
                    except PageNotAnInteger:
                        paginated_items = paginator.page(1)
                    except EmptyPage:
                        paginated_items = paginator.page(paginator.num_pages)

                    connections_data.append({'connection': connection, 'items': paginated_items})
                assistants_data.append({'assistant': assistant, 'ml_model_connections': connections_data})
            connections_by_organization.append({'organization': organization, 'assistants': assistants_data})
        context['connections_by_organization'] = connections_by_organization
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_ML_MODEL_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ML_MODEL_FILES):
            messages.error(self.request, "You do not have permission to delete ML Model files.")
            return redirect('datasource_ml_models:item_list')
        ##############################

        storage_id = request.POST.get('storage_id')
        selected_items = request.POST.getlist('selected_items')
        selected_items = [item for item in selected_items if item]  # Filter out any empty values

        if 'delete_all' in request.POST:
            DataSourceMLModelItem.objects.filter(ml_model_base__id=storage_id).delete()
            messages.success(request, 'All ML models in the selected connection have been deleted.')
            print('[DataSourceMLModelItemListView.post] All ML models in the selected connection have been deleted.')
        elif selected_items:
            DataSourceMLModelItem.objects.filter(id__in=selected_items).delete()
            messages.success(request, 'Selected ML models have been deleted.')
        return redirect('datasource_ml_models:item_list')
