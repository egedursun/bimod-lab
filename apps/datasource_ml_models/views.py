from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

from apps.assistants.models import Assistant
from apps.datasource_ml_models.forms import DataSourceMLModelConnectionForm, DataSourceMLModelItemForm
from apps.datasource_ml_models.models import DataSourceMLModelConnection, DataSourceMLModelItem
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


# Create your views here.

class DataSourceMLModelConnectionCreateView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = TemplateLayout.init(self, context)
        context['form'] = DataSourceMLModelConnectionForm()
        return context

    def post(self, request, *args, **kwargs):
        form = DataSourceMLModelConnectionForm(request.POST)
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - ML MODEL CONNECTION CREATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_ML_MODEL_CONNECTIONS not in user_permissions:
            messages.error(request, "You do not have permission to create ML Model Connections.")
            return redirect('datasource_ml_models:list')
        ##############################

        if form.is_valid():
            ml_model_connection = form.save(commit=False)
            ml_model_connection.created_by_user = request.user
            ml_model_connection.save()
            messages.success(request, 'ML Model Connection created successfully.')
            return redirect('datasource_ml_models:list')
        else:
            messages.error(request, 'There was an error creating the ML Model Connection.')
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)


class DataSourceMLModelConnectionUpdateView(LoginRequiredMixin, TemplateView):

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
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - ML MODEL CONNECTION UPDATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.UPDATE_ML_MODEL_CONNECTIONS not in user_permissions:
            messages.error(request, "You do not have permission to update ML Model Connections.")
            return redirect('datasource_ml_models:list')
        ##############################

        connection = DataSourceMLModelConnection.objects.get(id=kwargs['pk'])
        form = DataSourceMLModelConnectionForm(request.POST, instance=connection)
        if form.is_valid():
            form.save()
            messages.success(request, "ML Model Connection updated successfully.")
            return redirect('datasource_ml_models:list')
        else:
            messages.error(request, "Error updating ML Model Connection: " + str(form.errors))
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class DataSourceMLModelConnectionListView(LoginRequiredMixin, TemplateView):
    template_name = 'datasource_ml_models/base/list_datasource_ml_models.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
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
    model = DataSourceMLModelConnection
    success_url = 'datasource_ml_models:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        user = request.user

        ##############################
        # PERMISSION CHECK FOR - ML MODEL CONNECTION DELETE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_ML_MODEL_CONNECTIONS not in user_permissions:
            messages.error(request, "You do not have permission to delete ML Model Connections.")
            return redirect('datasource_ml_models:list')
        ##############################

        ml_model_connection = get_object_or_404(DataSourceMLModelConnection, id=kwargs['pk'])
        ml_model_connection.delete()
        return redirect(self.success_url)

    def get_queryset(self):
        user = self.request.user
        return DataSourceMLModelConnection.objects.filter(assistant__organization__in=user.organizations.all())


######################################################################################################################


class DataSourceMLModelItemCreateView(LoginRequiredMixin, TemplateView):
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
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - ML MODEL ITEM CREATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_ML_MODEL_CONNECTIONS not in user_permissions:
            messages.error(request, "You do not have permission to create ML Model Items.")
            return redirect('datasource_ml_models:item_list')
        ##############################

        if form.is_valid():
            ml_model_item = form.save(commit=False)
            uploaded_file = request.FILES['file']
            ml_model_item.file_bytes = uploaded_file.read()
            ml_model_item.ml_model_size = uploaded_file.size
            ml_model_item.created_by_user = request.user
            ml_model_item.save()
            messages.success(request, 'ML Model Item uploaded successfully.')
            return redirect('datasource_ml_models:item_list')
        else:
            messages.error(request, 'There was an error uploading the ML Model Item.')
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)


class DataSourceMLModelItemUpdateView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))


class DataSourceMLModelItemListView(LoginRequiredMixin, TemplateView):
    template_name = 'datasource_ml_models/models/list_datasource_ml_model_items.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
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

                    connections_data.append({
                        'connection': connection,
                        'items': paginated_items
                    })
                assistants_data.append({
                    'assistant': assistant,
                    'ml_model_connections': connections_data
                })
            connections_by_organization.append({
                'organization': organization,
                'assistants': assistants_data
            })

        context['connections_by_organization'] = connections_by_organization
        return context

    def post(self, request, *args, **kwargs):
        storage_id = request.POST.get('storage_id')
        selected_items = request.POST.getlist('selected_items')
        selected_items = [item for item in selected_items if item]  # Filter out any empty values

        if 'delete_all' in request.POST:
            DataSourceMLModelItem.objects.filter(ml_model_base__id=storage_id).delete()
            messages.success(request, 'All ML models in the selected connection have been deleted.')
        elif selected_items:
            DataSourceMLModelItem.objects.filter(id__in=selected_items).delete()
            messages.success(request, 'Selected ML models have been deleted.')

        return redirect('datasource_ml_models:item_list')


class DataSourceMLModelItemDeleteView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))
