from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.mm_apis.forms import CustomAPIForm
from apps.mm_apis.models import CUSTOM_API_CATEGORIES, CUSTOM_API_AUTHENTICATION_TYPES, CustomAPI, CustomAPIReference
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


# Create your views here.


class CreateCustomAPIView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = CustomAPIForm()
        context['CUSTOM_API_CATEGORIES'] = CUSTOM_API_CATEGORIES
        context['CUSTOM_API_AUTHENTICATION_TYPES'] = CUSTOM_API_AUTHENTICATION_TYPES
        return context

    def post(self, request, *args, **kwargs):
        form = CustomAPIForm(request.POST, request.FILES)

        ##############################
        # PERMISSION CHECK FOR - ADD_APIS
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=request.user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_APIS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to add APIs."}
            return self.render_to_response(context)
        ##############################

        if form.is_valid():
            custom_api = form.save(commit=False)
            custom_api.created_by_user = request.user

            # Handle dynamic fields
            endpoints = {}
            endpoint_keys = [key for key in request.POST.keys() if key.startswith('endpoints[')]
            endpoint_indices = set(key.split('[')[1].split(']')[0] for key in endpoint_keys)

            for i in endpoint_indices:
                name = request.POST.get(f'endpoints[{i}][name]')
                if name:  # Only add if name is not empty
                    endpoint_data = {
                        'description': request.POST.get(f'endpoints[{i}][description]', ''),
                        'path': request.POST.get(f'endpoints[{i}][path]', ''),
                        'method': request.POST.get(f'endpoints[{i}][method]', ''),
                        'header_params': request.POST.getlist(f'endpoints[{i}][header_params][]'),
                        'path_params': request.POST.getlist(f'endpoints[{i}][path_params][]'),
                        'query_params': request.POST.getlist(f'endpoints[{i}][query_params][]'),
                        'body_params': request.POST.getlist(f'endpoints[{i}][body_params][]')
                    }
                    endpoints[name] = endpoint_data
            custom_api.endpoints = endpoints

            # Save the image
            if request.FILES.get('api_picture'):
                custom_api.api_picture = request.FILES.get('api_picture')

            custom_api.categories = request.POST.getlist('categories')
            custom_api.save()

            return redirect('mm_apis:list')
        return render(request, self.template_name, {'form': form, 'assistants': Assistant.objects.filter(
            organization__users__in=[request.user]
        )})


class ListCustomAPIsView(LoginRequiredMixin, TemplateView):
    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        connected_organizations = Organization.objects.filter(users__in=[context_user])
        users_of_connected_organizations = User.objects.filter(
            profile__user__in=[user for org in connected_organizations for user in org.users.all()])
        apis_list = CustomAPI.objects.filter(created_by_user__in=users_of_connected_organizations)
        search_query = self.request.GET.get('search', '')
        if search_query:
            apis_list = apis_list.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        paginator = Paginator(apis_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['apis'] = page_obj.object_list
        context['total_apis'] = CustomAPI.objects.count()
        context['public_apis'] = CustomAPI.objects.filter(is_public=True).count()
        context['private_apis'] = CustomAPI.objects.filter(is_public=False).count()
        context['search_query'] = search_query
        return context


class ManageCustomAPIAssistantConnectionsView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        connected_organizations = Organization.objects.filter(users__in=[user])

        # Retrieve all users of the connected organizations
        users_of_connected_organizations = [user for org in connected_organizations for user in org.users.all()]

        # Fetch internal APIs created by users of connected organizations
        apis = CustomAPI.objects.filter(created_by_user__in=users_of_connected_organizations)

        # Fetch external API references
        external_api_references = CustomAPIReference.objects.filter(
            assistant__organization__in=connected_organizations
        ).exclude(custom_api__created_by_user__in=users_of_connected_organizations)

        # Fetch all assistants in connected organizations
        assistants = Assistant.objects.filter(organization__in=connected_organizations).select_related('organization')

        # Create a dictionary mapping assistants to their custom API references
        assistant_api_map = {
            assistant.id: CustomAPIReference.objects.filter(
                assistant=assistant,
                custom_api__created_by_user__in=users_of_connected_organizations
            )
            for assistant in assistants
        }

        external_api_references_map = {
            assistant.id: set(reference for reference in external_api_references if reference.assistant.id == assistant.id)
            for assistant in assistants
        }

        context.update({
            'connected_organizations': connected_organizations,
            'apis': apis,
            'assistants': assistants,
            'assistant_api_map': assistant_api_map,
            'external_api_references_map': external_api_references_map
        })
        return context

    def post(self, request, *args, **kwargs):
        assistant_id = request.POST.get('assistant_id')
        api_id = request.POST.get('api_id')
        action = request.POST.get('action')

        ##############################
        # PERMISSION CHECK FOR - ADD_APIS
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=request.user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_APIS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to add API connections."}
            return self.render_to_response(context)
        ##############################

        if not assistant_id or not action:
            messages.error(request, "Invalid input. Please try again.")
            return redirect('mm_apis:connect')

        try:
            assistant = Assistant.objects.get(id=assistant_id)
            if action == 'add' and api_id:
                custom_api = CustomAPI.objects.get(id=api_id)
                CustomAPIReference.objects.create(
                    assistant=assistant,
                    custom_api=custom_api,
                    created_by_user=request.user
                )
                messages.success(request, f"API '{custom_api.name}' assigned to assistant '{assistant.name}'.")
            elif action == 'remove':
                reference_id = request.POST.get('reference_id')
                if reference_id:
                    reference = CustomAPIReference.objects.get(id=reference_id)
                    reference.delete()
                    messages.success(request, f"API reference removed from assistant '{assistant.name}'.")
        except Assistant.DoesNotExist:
            messages.error(request, "Assistant not found.")
        except CustomAPI.DoesNotExist:
            messages.error(request, "Custom API not found.")
        except CustomAPIReference.DoesNotExist:
            messages.error(request, "Custom API Reference not found.")

        return redirect('mm_apis:connect')


class DeleteCustomAPIView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        custom_api_id = self.kwargs.get('pk')
        custom_api = CustomAPI.objects.get(id=custom_api_id)
        context['custom_api'] = custom_api
        return context

    def post(self, request, *args, **kwargs):
        custom_api_id = self.kwargs.get('pk')

        ##############################
        # PERMISSION CHECK FOR - DELETE_APIS
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=request.user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_APIS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to delete APIs."}
            return self.render_to_response(context)
        ##############################

        custom_api = CustomAPI.objects.get(id=custom_api_id)
        custom_api.delete()
        messages.success(request, "Custom API deleted successfully.")
        return redirect('mm_apis:list')


class APIStoreView(LoginRequiredMixin, TemplateView):
    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        search_query = self.request.GET.get('search', '')
        selected_categories = self.request.GET.getlist('categories')

        apis_list = CustomAPI.objects.filter(is_public=True)
        if search_query:
            apis_list = apis_list.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )
        if selected_categories:
            apis_list = apis_list.filter(
                *[Q(categories__icontains=category) for category in selected_categories]
            )

        # For each API, we must only offer the assistants that currently do not have an API reference for that API
        api_assistant_map = {
            api.id: Assistant.objects.exclude(customapireference__custom_api=api)
            for api in apis_list
        }

        paginator = Paginator(apis_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['apis'] = page_obj.object_list
        context['total_apis'] = CustomAPI.objects.count()
        context['public_apis'] = CustomAPI.objects.filter(is_public=True).count()
        context['private_apis'] = CustomAPI.objects.filter(is_public=False).count()
        context['search_query'] = search_query
        context['selected_categories'] = selected_categories
        context['CUSTOM_API_CATEGORIES'] = CUSTOM_API_CATEGORIES
        context['api_assistant_map'] = api_assistant_map
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        assistant_id = request.POST.get('assistant_id')

        ##############################
        # PERMISSION CHECK FOR - ADD_APIS
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=request.user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_APIS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to add API connections."}
            return self.render_to_response(context)
        ##############################

        if action and action == "add" and assistant_id:
            api_id = request.POST.get('api_id')
            if api_id:
                custom_api = CustomAPI.objects.get(id=api_id)
                assistant = Assistant.objects.get(id=assistant_id)
                CustomAPIReference.objects.create(
                    assistant=assistant,
                    custom_api=custom_api,
                    created_by_user=request.user
                )
                messages.success(request, f"API '{custom_api.name}' assigned to assistant '{assistant.name}'.")
        else:
            messages.error(request, "Invalid input. Please try again.")

        return redirect('mm_apis:store')

