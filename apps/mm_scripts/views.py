from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.mm_scripts.forms import CustomScriptForm
from apps.mm_scripts.models import CUSTOM_SCRIPT_CATEGORIES, CustomScript, CustomScriptReference
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


# Create your views here.


class CreateCustomScriptView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = CustomScriptForm()
        context['CUSTOM_SCRIPT_CATEGORIES'] = CUSTOM_SCRIPT_CATEGORIES
        return context

    def post(self, request, *args, **kwargs):
        form = CustomScriptForm(request.POST, request.FILES)

        if form.is_valid():
            custom_script = form.save(commit=False)
            custom_script.created_by_user = request.user

            # Handle dynamic fields
            categories = request.POST.getlist('categories')

            # Process step guide
            step_guide = request.POST.getlist('script_step_guide[]')
            custom_script.script_step_guide = step_guide

            # Save the image
            if request.FILES.get('script_picture'):
                custom_script.script_picture = request.FILES.get('script_picture')

            custom_script.categories = categories

            # Process script content
            script_content = request.POST.get('code_text', '')
            custom_script.script_content = script_content

            custom_script.save()

            messages.success(request, "Custom Script created successfully!")
            return redirect('mm_scripts:list')
        else:
            messages.error(request, "There was an error creating the custom script.")

        return render(request, self.template_name, {
            'form': form,
            'CUSTOM_SCRIPT_CATEGORIES': CUSTOM_SCRIPT_CATEGORIES,
        })


class ListCustomScriptsView(LoginRequiredMixin, TemplateView):
    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        connected_organizations = Organization.objects.filter(users__in=[context_user])
        users_of_connected_organizations = User.objects.filter(
            profile__user__in=[user for org in connected_organizations for user in org.users.all()])
        scripts_list = CustomScript.objects.filter(created_by_user__in=users_of_connected_organizations)
        search_query = self.request.GET.get('search', '')
        if search_query:
            scripts_list = scripts_list.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        paginator = Paginator(scripts_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['scripts'] = page_obj.object_list
        context['total_scripts'] = CustomScript.objects.count()
        context['public_scripts'] = CustomScript.objects.filter(is_public=True).count()
        context['private_scripts'] = CustomScript.objects.filter(is_public=False).count()
        context['search_query'] = search_query
        return context


class ManageCustomScriptAssistantConnectionsView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        connected_organizations = Organization.objects.filter(users__in=[user])

        # Retrieve all users of the connected organizations
        users_of_connected_organizations = [user for org in connected_organizations for user in org.users.all()]

        # Fetch internal scripts created by users of connected organizations
        scripts = CustomScript.objects.filter(created_by_user__in=users_of_connected_organizations)

        # Fetch external script references
        external_script_references = CustomScriptReference.objects.filter(
            assistant__organization__in=connected_organizations
        ).exclude(custom_script__created_by_user__in=users_of_connected_organizations)

        # Fetch all assistants in connected organizations
        assistants = Assistant.objects.filter(organization__in=connected_organizations).select_related('organization')

        # Create a dictionary mapping assistants to their custom script references
        assistant_script_map = {
            assistant.id: CustomScriptReference.objects.filter(
                assistant=assistant,
                custom_script__created_by_user__in=users_of_connected_organizations
            )
            for assistant in assistants
        }

        external_script_references_map = {
            assistant.id: set(reference for reference in external_script_references if reference.assistant.id == assistant.id)
            for assistant in assistants
        }

        context.update({
            'connected_organizations': connected_organizations,
            'scripts': scripts,
            'assistants': assistants,
            'assistant_script_map': assistant_script_map,
            'external_script_references_map': external_script_references_map
        })
        return context

    def post(self, request, *args, **kwargs):
        assistant_id = request.POST.get('assistant_id')
        script_id = request.POST.get('script_id')
        action = request.POST.get('action')

        ##############################
        # PERMISSION CHECK FOR - ADD_SCRIPTS
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=request.user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_SCRIPTS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to add script connections."}
            return self.render_to_response(context)
        ##############################

        if not assistant_id or not action:
            messages.error(request, "Invalid input. Please try again.")
            return redirect('mm_scripts:connect')

        try:
            assistant = Assistant.objects.get(id=assistant_id)
            if action == 'add' and script_id:
                custom_script = CustomScript.objects.get(id=script_id)
                CustomScriptReference.objects.create(
                    assistant=assistant,
                    custom_script=custom_script,
                    created_by_user=request.user
                )
                messages.success(request, f"Script '{custom_script.name}' assigned to assistant '{assistant.name}'.")
            elif action == 'remove':
                reference_id = request.POST.get('reference_id')
                if reference_id:
                    reference = CustomScriptReference.objects.get(id=reference_id)
                    reference.delete()
                    messages.success(request, f"Script reference removed from assistant '{assistant.name}'.")
        except Assistant.DoesNotExist:
            messages.error(request, "Assistant not found.")
        except CustomScript.DoesNotExist:
            messages.error(request, "Custom Script not found.")
        except CustomScriptReference.DoesNotExist:
            messages.error(request, "Custom Script Reference not found.")

        return redirect('mm_scripts:connect')


class DeleteCustomScriptView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        custom_script_id = self.kwargs.get('pk')
        custom_script = CustomScript.objects.get(id=custom_script_id)
        context['custom_script'] = custom_script
        return context

    def post(self, request, *args, **kwargs):
        custom_script_id = self.kwargs.get('pk')

        ##############################
        # PERMISSION CHECK FOR - DELETE_SCRIPTS
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=request.user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_SCRIPTS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to delete scripts."}
            return self.render_to_response(context)
        ##############################

        custom_script = CustomScript.objects.get(id=custom_script_id)
        custom_script.delete()
        messages.success(request, "Custom Script deleted successfully.")
        return redirect('mm_scripts:list')


class ScriptStoreView(LoginRequiredMixin, TemplateView):
    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        search_query = self.request.GET.get('search', '')
        selected_categories = self.request.GET.getlist('categories')

        scripts_list = CustomScript.objects.filter(is_public=True)
        if search_query:
            scripts_list = scripts_list.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query))
        if selected_categories:
            scripts_list = scripts_list.filter(
                *[Q(categories__icontains=category) for category in selected_categories])

        # for each of the scripts, we must only offer the assistants that currently do not have a script
        # reference for that script
        script_assistant_map = {
            script.id: Assistant.objects.exclude(customscriptreference__custom_script=script)
            for script in scripts_list
        }

        paginator = Paginator(scripts_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['scripts'] = page_obj.object_list
        context['total_scripts'] = CustomScript.objects.count()
        context['public_scripts'] = CustomScript.objects.filter(is_public=True).count()
        context['private_scripts'] = CustomScript.objects.filter(is_public=False).count()
        context['CUSTOM_SCRIPT_CATEGORIES'] = CUSTOM_SCRIPT_CATEGORIES
        context['search_query'] = search_query
        context['selected_categories'] = selected_categories
        context['script_assistant_map'] = script_assistant_map
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        assistant_id = request.POST.get('assistant_id')

        ##############################
        # PERMISSION CHECK FOR - ADD_SCRIPTS
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=request.user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_SCRIPTS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to add script connections."}
            return self.render_to_response(context)
        ##############################

        if action and action == "add" and assistant_id:
            script_id = request.POST.get('script_id')
            if script_id:
                custom_script = CustomScript.objects.get(id=script_id)
                assistant = Assistant.objects.get(id=assistant_id)
                CustomScriptReference.objects.create(
                    assistant=assistant,
                    custom_script=custom_script,
                    created_by_user=request.user
                )
                messages.success(request, f"Script '{custom_script.name}' assigned to assistant '{assistant.name}'.")
        else:
            messages.error(request, "Invalid input. Please try again.")

        return redirect('mm_scripts:store')
