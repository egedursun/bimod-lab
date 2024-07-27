from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.mm_functions.forms import CustomFunctionForm, CustomFunctionReferenceForm
from apps.mm_functions.models import CustomFunction, CustomFunctionReference, CUSTOM_FUNCTION_CATEGORIES
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission, PermissionNames
from auth.models import Profile
from web_project import TemplateLayout


# Create your views here.

class CreateCustomFunctionView(LoginRequiredMixin, TemplateView):
    template_name = "mm_functions/create_custom_function.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = CustomFunctionForm()
        context['CUSTOM_FUNCTION_CATEGORIES'] = CUSTOM_FUNCTION_CATEGORIES
        return context

    def post(self, request, *args, **kwargs):
        form = CustomFunctionForm(request.POST, request.FILES)

        ##############################
        # PERMISSION CHECK FOR - ADD_FUNCTIONS
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=request.user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_FUNCTIONS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to add functions."}
            return self.render_to_response(context)
        ##############################

        if form.is_valid():
            custom_function = form.save(commit=False)
            custom_function.created_by_user = request.user

            # Handle dynamic fields
            packages = []
            for name, version in zip(request.POST.getlist('packages[][name]'),
                                     request.POST.getlist('packages[][version]')):
                if name:  # Only add if name is not empty
                    packages.append({'name': name, 'version': version})
            custom_function.packages = packages
            categories = request.POST.getlist('categories')

            # Process input fields
            input_field_names = request.POST.getlist('input_fields[][name]')
            input_field_descriptions = request.POST.getlist('input_fields[][description]')
            input_field_types = request.POST.getlist('input_fields[][type]')
            input_field_requireds = request.POST.getlist('input_fields[][required]')

            input_fields = []
            for i in range(len(input_field_names)):
                input_fields.append({
                    'name': input_field_names[i] if i < len(input_field_names) else '',
                    'description': input_field_descriptions[i] if i < len(input_field_descriptions) else '',
                    'type': input_field_types[i] if i < len(input_field_types) else '',
                    'required': bool(input_field_requireds[i]) if i < len(input_field_requireds) else False
                })
            custom_function.input_fields = input_fields

            # Process output fields
            output_field_names = request.POST.getlist('output_fields[][name]')
            output_field_descriptions = request.POST.getlist('output_fields[][description]')
            output_field_types = request.POST.getlist('output_fields[][type]')

            output_fields = []
            for i in range(len(output_field_names)):
                output_fields.append({
                    'name': output_field_names[i] if i < len(output_field_names) else '',
                    'description': output_field_descriptions[i] if i < len(output_field_descriptions) else '',
                    'type': output_field_types[i] if i < len(output_field_types) else ''
                })
            custom_function.output_fields = output_fields

            # Process secrets fields
            secret_field_names = request.POST.getlist('secrets[][name]')
            secret_field_keys = request.POST.getlist('secrets[][key]')

            secrets = []
            for i in range(len(secret_field_names)):
                secrets.append({
                    'name': secret_field_names[i] if i < len(secret_field_names) else '',
                    'key': secret_field_keys[i] if i < len(secret_field_keys) else ''
                })
            custom_function.secrets = secrets

            # Save the image
            if request.FILES.get('function_picture'):
                custom_function.function_picture = request.FILES.get('function_picture')

            custom_function.categories = categories
            custom_function.save()

            return redirect('mm_functions:list')
        return render(request, self.template_name, {'form': form,
                                                    'assistants': Assistant.objects.filter(
                                                        organization__users__in=[request.user]
                                                    )})


class ListCustomFunctionsView(LoginRequiredMixin, TemplateView):
    template_name = "mm_functions/list_custom_functions.html"
    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        connected_organizations = Organization.objects.filter(users__in=[context_user])
        users_of_connected_organizations = User.objects.filter(
            profile__user__in=[user for org in connected_organizations for user in org.users.all()])
        functions_list = CustomFunction.objects.filter(created_by_user__in=users_of_connected_organizations)
        search_query = self.request.GET.get('search', '')
        if search_query:
            functions_list = functions_list.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        paginator = Paginator(functions_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['functions'] = page_obj.object_list
        context['total_functions'] = CustomFunction.objects.count()
        context['public_functions'] = CustomFunction.objects.filter(is_public=True).count()
        context['private_functions'] = CustomFunction.objects.filter(is_public=False).count()
        context['search_query'] = search_query
        return context


class ManageCustomFunctionAssistantConnectionsView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        connected_organizations = Organization.objects.filter(users__in=[user])

        # Retrieve all users of the connected organizations
        users_of_connected_organizations = [user for org in connected_organizations for user in org.users.all()]

        # Fetch internal functions created by users of connected organizations
        functions = CustomFunction.objects.filter(created_by_user__in=users_of_connected_organizations)

        # Fetch external functions
        external_function_references = CustomFunctionReference.objects.filter(
            assistant__organization__in=connected_organizations
        ).exclude(custom_function__created_by_user__in=users_of_connected_organizations)

        # Fetch all assistants in connected organizations
        assistants = Assistant.objects.filter(organization__in=connected_organizations).select_related('organization')

        # Create a dictionary mapping assistants to their custom function references
        assistant_function_map = {
            assistant.id: CustomFunctionReference.objects.filter(
                assistant=assistant,
                custom_function__created_by_user__in = users_of_connected_organizations
            )
            for assistant in assistants
        }

        external_function_references_map = {
            assistant.id: set(reference for reference in external_function_references if reference.assistant.id == assistant.id)
            for assistant in assistants
        }

        context.update({
            'connected_organizations': connected_organizations,
            'functions': functions,
            'assistants': assistants,
            'assistant_function_map': assistant_function_map,
            'external_function_references_map': external_function_references_map
        })
        return context

    def post(self, request, *args, **kwargs):
        assistant_id = request.POST.get('assistant_id')
        function_id = request.POST.get('function_id')
        action = request.POST.get('action')

        ##############################
        # PERMISSION CHECK FOR - ADD_FUNCTIONS
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=request.user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_FUNCTIONS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to add function connections."}
            return self.render_to_response(context)
        ##############################

        if not assistant_id or not action:
            messages.error(request, "Invalid input. Please try again.")
            return redirect('mm_functions:connect')

        try:
            assistant = Assistant.objects.get(id=assistant_id)
            if action == 'add' and function_id:
                custom_function = CustomFunction.objects.get(id=function_id)
                CustomFunctionReference.objects.create(
                    assistant=assistant,
                    custom_function=custom_function,
                    created_by_user=request.user
                )
                messages.success(request, f"Function '{custom_function.name}' assigned to assistant '{assistant.name}'.")
            elif action == 'remove':
                reference_id = request.POST.get('reference_id')
                if reference_id:
                    reference = CustomFunctionReference.objects.get(id=reference_id)
                    reference.delete()
                    messages.success(request, f"Function reference removed from assistant '{assistant.name}'.")
        except Assistant.DoesNotExist:
            messages.error(request, "Assistant not found.")
        except CustomFunction.DoesNotExist:
            messages.error(request, "Custom Function not found.")
        except CustomFunctionReference.DoesNotExist:
            messages.error(request, "Custom Function Reference not found.")

        return redirect('mm_functions:connect')


class DeleteCustomFunctionView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        custom_function_id = self.kwargs.get('pk')
        custom_function = CustomFunction.objects.get(id=custom_function_id)
        context['custom_function'] = custom_function
        return context

    def post(self, request, *args, **kwargs):
        custom_function_id = self.kwargs.get('pk')

        ##############################
        # PERMISSION CHECK FOR - DELETE_FUNCTIONS
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=request.user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_FUNCTIONS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to delete functions."}
            return self.render_to_response(context)
        ##############################

        custom_function = CustomFunction.objects.get(id=custom_function_id)
        custom_function.delete()
        messages.success(request, "Custom Function deleted successfully.")
        return redirect('mm_functions:list')


class FunctionStoreView(LoginRequiredMixin, TemplateView):
    template_name = "mm_functions/function_store.html"
    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        search_query = self.request.GET.get('search', '')
        selected_categories = self.request.GET.getlist('categories')

        functions_list = CustomFunction.objects.filter(is_public=True)
        if search_query:
            functions_list = functions_list.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query))
        if selected_categories:
            functions_list = functions_list.filter(
                *[Q(categories__icontains=category) for category in selected_categories])

        # for each of the functions, we must only offer the assistants that currently does not have a function
        # reference for that function
        function_assistant_map = {
            function.id: Assistant.objects.exclude(customfunctionreference__custom_function=function)
            for function in functions_list
        }

        paginator = Paginator(functions_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['functions'] = page_obj.object_list
        context['total_functions'] = CustomFunction.objects.count()
        context['public_functions'] = CustomFunction.objects.filter(is_public=True).count()
        context['private_functions'] = CustomFunction.objects.filter(is_public=False).count()
        context['search_query'] = search_query
        context['selected_categories'] = selected_categories
        context['CUSTOM_FUNCTION_CATEGORIES'] = CUSTOM_FUNCTION_CATEGORIES
        context['function_assistant_map'] = function_assistant_map
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        assistant_id = request.POST.get('assistant_id')

        ##############################
        # PERMISSION CHECK FOR - ADD_FUNCTIONS
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=request.user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_FUNCTIONS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to add function connections."}
            return self.render_to_response(context)
        ##############################

        if action and action == "add" and assistant_id:
            function_id = request.POST.get('function_id')
            if function_id:
                custom_function = CustomFunction.objects.get(id=function_id)
                assistant = Assistant.objects.get(id=assistant_id)
                CustomFunctionReference.objects.create(
                    assistant=assistant,
                    custom_function=custom_function,
                    created_by_user=request.user
                )
                messages.success(request, f"Function '{custom_function.name}' assigned to assistant '{assistant.name}'.")
        else:
            messages.error(request, "Invalid input. Please try again.")

        return redirect('mm_functions:store')
