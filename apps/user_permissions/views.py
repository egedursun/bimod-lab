from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.organization.models import Organization
from apps.user_permissions.models import PermissionNames, UserPermission, PERMISSION_TYPES
from web_project import TemplateLayout


# Create your views here.


class AddPermissionsView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        context['users'] = []
        context['permissions'] = self.get_permissions_grouped()
        if 'organization' in self.request.GET:
            organization_id = self.request.GET.get('organization')
            organization = get_object_or_404(Organization, id=organization_id)
            context['selected_organization'] = organization
            context['users'] = organization.users.all()
        if 'user' in self.request.GET:
            user_id = self.request.GET.get('user')
            user = get_object_or_404(User, id=user_id)
            context['selected_user'] = user
            context['existing_permissions'] = list(user.permissions.values_list('permission_type', flat=True))
            context['available_permissions'] = [
                perm for perm in PERMISSION_TYPES if perm[0] not in context['existing_permissions']
            ]
        return context

    def post(self, request, *args, **kwargs):
        organization_id = request.POST.get('organization')
        user_id = request.POST.get('user')
        selected_permissions = request.POST.getlist('permissions')

        if organization_id and user_id and selected_permissions:
            user = get_object_or_404(User, id=user_id)
            for perm in selected_permissions:
                UserPermission.objects.get_or_create(user=user, permission_type=perm)
            return redirect('user_permissions:list_permissions')

        context = self.get_context_data(**kwargs)
        context['error_messages'] = "All fields are required."
        return render(request, self.template_name, context)

    def get_permissions_grouped(self):
        permissions_grouped = {
            "Organization Permissions": [
                ('add_organizations', 'Add Organizations'),
                ('update_organizations', 'Update Organizations'),
                ('list_organizations', 'List Organizations'),
                ('delete_organizations', 'Delete Organizations')
            ],
            "LLM Core Permissions": [
                ('add_llm_cores', 'Add LLM Cores'),
                ('update_llm_cores', 'Update LLM Cores'),
                ('list_llm_cores', 'List LLM Cores'),
                ('delete_llm_cores', 'Delete LLM Cores')
            ],
            "Transaction Permissions": [
                ('list_transactions', 'List Transactions')
            ],
            "User Permissions": [
                ('add_users', 'Add Users'),
                ('update_users', 'Update Users'),
                ('list_users', 'List Users'),
                ('delete_users', 'Delete Users')
            ],
            "User Role Modification and Read Permissions": [
                ('modify_user_permissions', 'Modify User Permissions'),
                ('list_user_permissions', 'List User Permissions')
            ],
            "Assistant Permissions": [
                ('add_assistants', 'Add Assistants'),
                ('update_assistants', 'Update Assistants'),
                ('list_assistants', 'List Assistants'),
                ('delete_assistants', 'Delete Assistants')
            ],
            "Chat Permissions": [
                ('create_and_use_chats', 'Create and Use Chats'),
                ('remove_chats', 'Remove Chats')
            ],
            "Memory Permissions": [
                ('add_assistant_memories', 'Add Assistant Memories'),
                ('list_assistant_memories', 'List Assistant Memories'),
                ('delete_assistant_memories', 'Delete Assistant Memories')
            ],
            "Assistant Exportation Permissions": [
                ('export_assistant', 'Export Assistant')
            ],
            "Orchestration Permissions": [
                ('add_orchestrations', 'Add Orchestrations'),
                ('update_orchestrations', 'Update Orchestrations'),
                ('list_orchestrations', 'List Orchestrations'),
                ('delete_orchestrations', 'Delete Orchestrations')
            ],
            "File System Permissions": [
                ('add_file_systems', 'Add File Systems'),
                ('update_file_systems', 'Update File Systems'),
                ('list_file_systems', 'List File Systems'),
                ('delete_file_systems', 'Delete File Systems')
            ],
            "Web Browsers": [
                ('add_web_browsers', 'Add Web Browsers'),
                ('update_web_browsers', 'Update Web Browsers'),
                ('list_web_browsers', 'List Web Browsers'),
                ('delete_web_browsers', 'Delete Web Browsers')
            ],
            "SQL Databases": [
                ('add_sql_databases', 'Add SQL Databases'),
                ('update_sql_databases', 'Update SQL Databases'),
                ('list_sql_databases', 'List SQL Databases'),
                ('delete_sql_databases', 'Delete SQL Databases')
            ],
            "NoSQL Databases": [
                ('add_nosql_databases', 'Add NoSQL Databases'),
                ('update_nosql_databases', 'Update NoSQL Databases'),
                ('list_nosql_databases', 'List NoSQL Databases'),
                ('delete_nosql_databases', 'Delete NoSQL Databases')
            ],
            "Knowledge Bases": [
                ('add_knowledge_bases', 'Add Knowledge Bases'),
                ('update_knowledge_bases', 'Update Knowledge Bases'),
                ('list_knowledge_bases', 'List Knowledge Bases'),
                ('delete_knowledge_bases', 'Delete Knowledge Bases')
            ],
            "Image Storages": [
                ('add_image_storages', 'Add Image Storages'),
                ('update_image_storages', 'Update Image Storages'),
                ('list_image_storages', 'List Image Storages'),
                ('delete_image_storages', 'Delete Image Storages')
            ],
            "Video Storages": [
                ('add_video_storages', 'Add Video Storages'),
                ('update_video_storages', 'Update Video Storages'),
                ('list_video_storages', 'List Video Storages'),
                ('delete_video_storages', 'Delete Video Storages')
            ],
            "Audio Storages": [
                ('add_audio_storages', 'Add Audio Storages'),
                ('update_audio_storages', 'Update Audio Storages'),
                ('list_audio_storages', 'List Audio Storages'),
                ('delete_audio_storages', 'Delete Audio Storages')
            ],
            "Functions": [
                ('add_functions', 'Add Functions'),
                ('update_functions', 'Update Functions'),
                ('list_functions', 'List Functions'),
                ('delete_functions', 'Delete Functions')
            ],
            "APIs": [
                ('add_apis', 'Add APIs'),
                ('update_apis', 'Update APIs'),
                ('list_apis', 'List APIs'),
                ('delete_apis', 'Delete APIs')
            ],
            "Scheduled Jobs": [
                ('add_scheduled_jobs', 'Add Scheduled Jobs'),
                ('update_scheduled_jobs', 'Update Scheduled Jobs'),
                ('list_scheduled_jobs', 'List Scheduled Jobs'),
                ('delete_scheduled_jobs', 'Delete Scheduled Jobs')
            ],
            "Triggers": [
                ('add_triggers', 'Add Triggers'),
                ('update_triggers', 'Update Triggers'),
                ('list_triggers', 'List Triggers'),
                ('delete_triggers', 'Delete Triggers')
            ],
            "Image Generation": [
                ('can_generate_images', 'Can Generate Images')
            ],
            "Audio Generation": [
                ('can_generate_audio', 'Can Generate Audio')
            ],
            "Integrations": [
                ('add_integrations', 'Add Integrations'),
                ('update_integrations', 'Update Integrations'),
                ('list_integrations', 'List Integrations'),
                ('delete_integrations', 'Delete Integrations')
            ],
            "Meta Integrations": [
                ('add_meta_integrations', 'Add Meta Integrations'),
                ('update_meta_integrations', 'Update Meta Integrations'),
                ('list_meta_integrations', 'List Meta Integrations'),
                ('delete_meta_integrations', 'Delete Meta Integrations')
            ],
            "Starred Messages": [
                ('add_starred_messages', 'Add Starred Messages'),
                ('list_starred_messages', 'List Starred Messages'),
                ('remove_starred_messages', 'Remove Starred Messages'),
            ],
        }
        return permissions_grouped


class ListPermissionsView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        user = self.request.user
        organizations = Organization.objects.filter(users__in=[user])
        org_users_permissions = {
            org: {
                "users": {
                    user: user.permissions.all()
                    for user in org.users.all()
                }
            }
            for org in organizations
        }
        context['org_users_permissions'] = org_users_permissions
        return context

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - PERMISSIONS/UPDATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.MODIFY_USER_PERMISSIONS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to update or modify user permissions."}
            return self.render_to_response(context)
        ##############################

        user = get_object_or_404(User, id=user_id)
        permissions_data = request.POST.getlist('permissions')
        delete_requests = request.POST.getlist('delete_requests')

        # Process active/deactivate toggles
        for permission in user.permissions.all():
            if str(permission.id) in permissions_data and not permission.is_active:
                permission.is_active = True
                permission.save()
            elif str(permission.id) not in permissions_data and permission.is_active:
                permission.is_active = False
                permission.save()

        # Process delete requests
        for permission_id in delete_requests:
            permission = get_object_or_404(UserPermission, id=permission_id)
            permission.delete()

        messages.success(request, 'Permissions updated successfully!')

        # Update only the relevant part of the page.
        return render(request, self.template_name, self.get_context_data(**kwargs))
