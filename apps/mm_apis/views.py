from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.mm_apis.forms import CustomAPIForm
from apps.mm_apis.models import CUSTOM_API_CATEGORIES, CUSTOM_API_AUTHENTICATION_TYPES, CustomAPI
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
        return context


class DeleteCustomAPIView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class APIStoreView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


