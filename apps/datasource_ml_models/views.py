"""
This module contains views for managing machine learning model connections and items within the Bimod.io platform.

The views include creating, updating, deleting, and listing ML model connections and their associated items. These views also handle uploading ML models and pagination of listed models. Access to these views is restricted to authenticated users, with additional permission checks for specific actions.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_ml_models.forms import DataSourceMLModelConnectionForm, DataSourceMLModelItemForm
from apps.datasource_ml_models.models import DataSourceMLModelConnection, DataSourceMLModelItem
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


class DataSourceMLModelConnectionCreateView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of new machine learning model connections.

    This view displays a form for creating a new ML model connection. Upon submission, it validates the input, checks user permissions, and saves the new connection to the database. If the user lacks the necessary permissions, an error message is displayed.

    Methods:
        get_context_data(self, **kwargs): Adds additional context to the template, including the form for creating an ML model connection.
        post(self, request, *args, **kwargs): Handles form submission and ML model connection creation, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = TemplateLayout.init(self, context)
        context['form'] = DataSourceMLModelConnectionForm()
        return context

    def post(self, request, *args, **kwargs):
        form = DataSourceMLModelConnectionForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD_ML_MODEL_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_ML_MODEL_CONNECTIONS):
            messages.error(self.request, "You do not have permission to create ML Model Connections.")
            return redirect('datasource_ml_models:list')
        ##############################

        if form.is_valid():
            ml_model_connection = form.save(commit=False)
            ml_model_connection.created_by_user = request.user
            ml_model_connection.save()
            messages.success(request, 'ML Model Connection created successfully.')
            print('[DataSourceMLModelConnectionCreateView.post] ML Model Connection created successfully.')
            return redirect('datasource_ml_models:list')
        else:
            messages.error(request, 'There was an error creating the ML Model Connection.')
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)


class DataSourceMLModelConnectionUpdateView(LoginRequiredMixin, TemplateView):
    """
    Handles updating an existing machine learning model connection.

    This view allows users with the appropriate permissions to modify an ML model connection's attributes. It also handles the form submission and validation for updating the connection.

    Methods:
        get_context_data(self, **kwargs): Retrieves the current ML model connection details and adds them to the context, along with other relevant data such as available assistants and the form for updating the connection.
        post(self, request, *args, **kwargs): Handles form submission for updating the ML model connection, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        connection = DataSourceMLModelConnection.objects.get(id=kwargs['pk'])
        user_organizations = context_user.organizations.all()
        assistants = Assistant.objects.filter(organization__in=user_organizations)
        context['form'] = DataSourceMLModelConnectionForm(instance=connection)
        context['assistants'] = assistants
        context['connection'] = connection
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_ML_MODEL_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_ML_MODEL_CONNECTIONS):
            messages.error(self.request, "You do not have permission to update ML Model Connections.")
            return redirect('datasource_ml_models:list')
        ##############################

        connection = DataSourceMLModelConnection.objects.get(id=kwargs['pk'])
        form = DataSourceMLModelConnectionForm(request.POST, instance=connection)
        if form.is_valid():
            form.save()
            messages.success(request, "ML Model Connection updated successfully.")
            print('[DataSourceMLModelConnectionUpdateView.post] ML Model Connection updated successfully.')
            return redirect('datasource_ml_models:list')
        else:
            messages.error(request, "Error updating ML Model Connection: " + str(form.errors))
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class DataSourceMLModelConnectionListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of machine learning model connections associated with the user's organizations and assistants.

    This view retrieves all ML model connections organized by organization and assistant, and displays them in a structured list.

    Attributes:
        template_name (str): The template used to render the ML model connection list.

    Methods:
        get_context_data(self, **kwargs): Retrieves the ML model connections organized by organization and assistant, and adds them to the context.
    """

    template_name = 'datasource_ml_models/base/list_datasource_ml_models.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_ML_MODEL_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_ML_MODEL_CONNECTIONS):
            messages.error(self.request, "You do not have permission to list ML Model Connections.")
            return context
        ##############################

        context_user = self.request.user
        connections = DataSourceMLModelConnection.objects.filter(
            assistant__in=Assistant.objects.filter(organization__in=context_user.organizations.all())
        ).select_related('assistant__organization')

        connections_by_organization = {}
        for connection in connections:
            organization = connection.assistant.organization
            assistant = connection.assistant

            if organization not in connections_by_organization:
                connections_by_organization[organization] = {}
            if assistant not in connections_by_organization[organization]:
                connections_by_organization[organization][assistant] = []
            connections_by_organization[organization][assistant].append(connection)
        context['connections_by_organization'] = connections_by_organization
        return context


class DataSourceMLModelConnectionDeleteView(LoginRequiredMixin, DeleteView):
    """
    Handles the deletion of a machine learning model connection.

    This view allows users with the appropriate permissions to delete an ML model connection. It ensures that the user has the necessary permissions before performing the deletion.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for rendering the confirmation of the deletion.
        post(self, request, *args, **kwargs): Deletes the ML model connection if the user has the required permissions.
        get_queryset(self): Filters the queryset to include only the ML model connections that belong to the user's assistants.
    """

    model = DataSourceMLModelConnection
    success_url = 'datasource_ml_models:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_ML_MODEL_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ML_MODEL_CONNECTIONS):
            messages.error(self.request, "You do not have permission to delete ML Model Connections.")
            return redirect('datasource_ml_models:list')
        ##############################

        ml_model_connection = get_object_or_404(DataSourceMLModelConnection, id=kwargs['pk'])
        ml_model_connection.delete()
        print('[DataSourceMLModelConnectionDeleteView.post] ML Model Connection deleted successfully.')
        return redirect(self.success_url)

    def get_queryset(self):
        user = self.request.user
        return DataSourceMLModelConnection.objects.filter(assistant__organization__in=user.organizations.all())


class DataSourceMLModelItemCreateView(LoginRequiredMixin, TemplateView):
    """
    Handles uploading machine learning model files to a selected ML model connection.

    This view displays a form for selecting an ML model connection and uploading ML model files to it. Upon form submission, it validates the input, reads the file contents, and saves the ML model items to the database. If the user lacks the necessary permissions, an error message is displayed.

    Attributes:
        template_name (str): The template used to render the ML model item creation form.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the available ML model connections and the form for uploading ML model items.
        post(self, request, *args, **kwargs): Handles the ML model file upload process, including validation and saving the ML model items.
    """

    template_name = 'datasource_ml_models/models/create_datasource_ml_model_item.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        user_organizations = context_user.organizations.all()
        user_assistants = Assistant.objects.filter(organization__in=user_organizations)
        ml_model_connections = DataSourceMLModelConnection.objects.filter(
            assistant__in=user_assistants
        ).all()
        context['ml_model_connections'] = ml_model_connections
        context['form'] = DataSourceMLModelItemForm()
        return context

    def post(self, request, *args, **kwargs):
        form = DataSourceMLModelItemForm(request.POST, request.FILES)

        ##############################
        # PERMISSION CHECK FOR - ADD_ML_MODEL_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_ML_MODEL_FILES):
            messages.error(self.request, "You do not have permission to add ML Model files.")
            return redirect('datasource_ml_models:item_list')
        ##############################

        if form.is_valid():
            ml_model_item = form.save(commit=False)
            uploaded_file = request.FILES['file']
            ml_model_item.file_bytes = uploaded_file.read()
            ml_model_item.ml_model_size = uploaded_file.size
            ml_model_item.created_by_user = request.user
            ml_model_item.save()
            print('[DataSourceMLModelItemCreateView.post] ML Model Item uploaded successfully.')
            messages.success(request, 'ML Model Item uploaded successfully.')
            return redirect('datasource_ml_models:item_list')
        else:
            messages.error(request, 'There was an error uploading the ML Model Item.')
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)


class DataSourceMLModelItemUpdateView(LoginRequiredMixin, TemplateView):
    """
    Displays and updates the details of a specific machine learning model item.

    This view allows users with the appropriate permissions to view and update the details of an ML model item.

    Methods:
        get_context_data(self, **kwargs): Retrieves the ML model item details and adds them to the context.
        post(self, request, *args, **kwargs): Handles the update of the ML model item's details.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - UPDATE_ML_MODEL_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_ML_MODEL_FILES):
            messages.error(self.request, "You do not have permission to update ML Model files.")
            return redirect('datasource_ml_models:item_list')
        ##############################

        return self.render_to_response(self.get_context_data(**kwargs))


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


class DataSourceMLModelItemDeleteView(LoginRequiredMixin, TemplateView):
    """
    Handles the deletion of a specific machine learning model item.

    This view allows users with the appropriate permissions to delete an ML model item.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for rendering the confirmation of the deletion.
        post(self, request, *args, **kwargs): Deletes the ML model item if the user has the required permissions.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_ML_MODEL_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ML_MODEL_FILES):
            messages.error(self.request, "You do not have permission to delete ML Model files.")
            return redirect('datasource_ml_models:item_list')
        ##############################

        print('[DataSourceMLModelItemDeleteView.post] Deleting ML Model Item')
        return self.render_to_response(self.get_context_data(**kwargs))
