"""
Module for managing user permissions within the web application.

This module contains views that handle the assignment, listing, and management of user permissions within the application. It allows administrators to:
- Assign specific permissions to users.
- View and update existing permissions for users within different organizations.
- Remove permissions from users as necessary.

Views:
    - AddPermissionsView: Facilitates the addition of new permissions to users.
    - ListPermissionsView: Displays and manages the permissions assigned to users.

Permissions:
    The views in this module enforce permission checks to ensure that only authorized users can assign, update, or remove permissions.

Models:
    - Organization: Represents an organization that can have multiple users with various permissions.
    - UserPermission: Represents the permissions assigned to a user.
    - User: Django's built-in user model.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_permissions.models import PermissionNames, UserPermission, PERMISSION_TYPES
from web_project import TemplateLayout


class AddPermissionsView(TemplateView):
    """
    View to handle adding permissions to users.

    This view allows administrators to assign specific permissions to users within an organization. The permissions are grouped by categories like 'Organization Permissions', 'LLM Core Permissions', etc.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with organizations, users, and grouped permissions. If an organization and/or user is selected, it filters the context accordingly.
        post(self, request, *args, **kwargs): Handles the logic to assign selected permissions to a user.
        get_permissions_grouped(self): Returns a dictionary of permissions grouped by categories.
    """

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

        ##############################
        # PERMISSION CHECK FOR - MODIFY_USER_PERMISSIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.MODIFY_USER_PERMISSIONS):
            messages.error(self.request, "You do not have permission to add/modify permissions.")
            return redirect('user_permissions:list_permissions')
        ##############################

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
                ('delete_organizations', 'Delete Organizations'),
                ('add_balance_to_organization', 'Add Balance to Organization'),
                ('transfer_balance_between_organizations', 'Transfer Balance Between Organizations'),
            ],
            "LLM Core Permissions": [
                ('add_llm_cores', 'Add LLM Cores'),
                ('update_llm_cores', 'Update LLM Cores'),
                ('list_llm_cores', 'List LLM Cores'),
                ('delete_llm_cores', 'Delete LLM Cores')
            ],
            "Fine-Tuning Model Permissions": [
                ('add_finetuning_model', 'Add Finetuning Model'),
                ('update_finetuning_model', 'Update Finetuning Model'),
                ('list_finetuning_model', 'List Finetuning Model'),
                ('delete_finetuning_model', 'Delete Finetuning Model'),
            ],
            "Transaction Permissions": [
                ('list_transactions', 'List Transactions')
            ],
            "Data Security Permissions": [
                ('add_data_security', 'Add Data Security'),
                ('update_data_security', 'Update Data Security'),
                ('list_data_security', 'List Data Security'),
                ('delete_data_security', 'Delete Data Security'),
            ],
            "User Permissions": [
                ('add_users', 'Add Users'),
                ('update_users', 'Update Users'),
                ('list_users', 'List Users'),
                ('delete_users', 'Delete Users'),
                ('connect_user_to_organization', 'Connect User to Organization'),
                ('remove_user_from_organization', 'Remove User from Organization'),
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
            "Assistant Exportation Permissions": [
                ('add_export_assistant', 'Add Export Assistants'),
                ('update_export_assistant', 'Update Export Assistants'),
                ('list_export_assistant', 'List Export Assistants'),
                ('delete_export_assistant', 'Delete Export Assistants')
            ],
            "LeanMod Assistant Permissions": [
                ('add_lean_assistant', 'Add Lean Assistant'),
                ('update_lean_assistant', 'Update Lean Assistant'),
                ('list_lean_assistant', 'List Lean Assistant'),
                ('delete_lean_assistant', 'Delete Lean Assistant'),
            ],
            "Expert Networks Permissions": [
                ('add_expert_networks', 'Add Expert Networks'),
                ('update_expert_networks', 'Update Expert Networks'),
                ('list_expert_networks', 'List Expert Networks'),
                ('delete_expert_networks', 'Delete Expert Networks'),
            ],
            "LeanMod Assistant Export Permissions": [
                ('add_export_leanmod', 'Add Export LeanMod'),
                ('update_export_leanmod', 'Update Export LeanMod'),
                ('list_export_leanmod', 'List Export LeanMod'),
                ('delete_export_leanmod', 'Delete Export LeanMod'),
            ],
            "Chat Permissions": [
                ('create_and_use_chats', 'Create and Use Chats'),
                ('remove_chats', 'Remove Chats'),
                ('archive_chats', 'Archive Chats'),
                ('unarchive_chats', 'Unarchive Chats'),
            ],
            "LeanMod Chat Permissions": [
                ('create_and_use_lean_chats', 'Create and Use Lean Chats'),
                ('remove_lean_chats', 'Remove Lean Chats'),
                ('archive_lean_chats', 'Archive Lean Chats'),
                ('unarchive_lean_chats', 'Unarchive Lean Chats'),
            ],
            "Starred Messages Permissions": [
                ('add_starred_messages', 'Add Starred Messages'),
                ('list_starred_messages', 'List Starred Messages'),
                ('remove_starred_messages', 'Remove Starred Messages'),
            ],
            "Message Templates Permissions": [
                ('add_template_messages', 'Add Message Templates'),
                ('update_template_messages', 'Update Message Templates'),
                ('list_template_messages', 'List Message Templates'),
                ('remove_template_messages', 'Remove Message Templates'),
            ],
            "Memory Permissions": [
                ('add_assistant_memories', 'Add Assistant Memories'),
                ('list_assistant_memories', 'List Assistant Memories'),
                ('delete_assistant_memories', 'Delete Assistant Memories')
            ],
            "Orchestration Permissions": [
                ('add_orchestrations', 'Add Orchestrations'),
                ('update_orchestrations', 'Update Orchestrations'),
                ('list_orchestrations', 'List Orchestrations'),
                ('delete_orchestrations', 'Delete Orchestrations')
            ],
            "Orchestration Export Permissions": [
                ('add_export_orchestration', 'Add Export Orchestration'),
                ('update_export_orchestration', 'Update Export Orchestration'),
                ('list_export_orchestration', 'List Export Orchestration'),
                ('delete_export_orchestration', 'Delete Export Orchestration'),
            ],
            "Orchestration Chat Permissions": [
                ('create_and_use_orchestration_chats', 'Create and Use Orchestration Chats'),
                ('remove_orchestration_chats', 'Remove Orchestration Chats'),
            ],
            "File System Permissions": [
                ('add_file_systems', 'Add File Systems'),
                ('update_file_systems', 'Update File Systems'),
                ('list_file_systems', 'List File Systems'),
                ('delete_file_systems', 'Delete File Systems')
            ],
            "Web Browser Permissions": [
                ('add_web_browsers', 'Add Web Browsers'),
                ('update_web_browsers', 'Update Web Browsers'),
                ('list_web_browsers', 'List Web Browsers'),
                ('delete_web_browsers', 'Delete Web Browsers')
            ],
            "SQL Database Permissions": [
                ('add_sql_databases', 'Add SQL Databases'),
                ('update_sql_databases', 'Update SQL Databases'),
                ('list_sql_databases', 'List SQL Databases'),
                ('delete_sql_databases', 'Delete SQL Databases')
            ],
            "Custom SQL Queries Permissions": [
                ('add_custom_sql_queries', 'Add Custom SQL Queries'),
                ('update_custom_sql_queries', 'Update Custom SQL Queries'),
                ('list_custom_sql_queries', 'List Custom SQL Queries'),
                ('delete_custom_sql_queries', 'Delete Custom SQL Queries'),
            ],
            "NoSQL Database Permissions": [
                ('add_nosql_databases', 'Add NoSQL Databases'),
                ('update_nosql_databases', 'Update NoSQL Databases'),
                ('list_nosql_databases', 'List NoSQL Databases'),
                ('delete_nosql_databases', 'Delete NoSQL Databases')
            ],
            "Knowledge Base Permissions": [
                ('add_knowledge_bases', 'Add Knowledge Bases'),
                ('update_knowledge_bases', 'Update Knowledge Bases'),
                ('list_knowledge_bases', 'List Knowledge Bases'),
                ('delete_knowledge_bases', 'Delete Knowledge Bases')
            ],
            "Knowledge Base Documents Permissions": [
                ('add_knowledge_base_docs', 'Add Knowledge Base Docs'),
                ('update_knowledge_base_docs', 'Update Knowledge Base Docs'),
                ('list_knowledge_base_docs', 'List Knowledge Base Docs'),
                ('delete_knowledge_base_docs', 'Delete Knowledge Base Docs'),
            ],
            "Code Base Permissions": [
                ('add_code_base', 'Add Code Base'),
                ('update_code_base', 'Update Code Base'),
                ('list_code_base', 'List Code Base'),
                ('delete_code_base', 'Delete Code Base'),
            ],
            "Code Repository Permissions": [
                ('add_code_repository', 'Add Code Repository'),
                ('update_code_repository', 'Update Code Repository'),
                ('list_code_repository', 'List Code Repository'),
                ('delete_code_repository', 'Delete Code Repository'),
            ],
            "Media Storage Permissions": [
                ('add_media_storages', 'Add Media Storages'),
                ('update_media_storages', 'Update Media Storages'),
                ('list_media_storages', 'List Media Storages'),
                ('delete_media_storages', 'Delete Media Storages')
            ],
            "Media Storage Documents Permissions": [
                ('add_storage_files', 'Add Storage Files'),
                ('update_storage_files', 'Update Storage Files'),
                ('list_storage_files', 'List Storage Files'),
                ('delete_storage_files', 'Delete Storage Files'),
            ],
            "ML Model Permissions": [
                ('add_ml_model_connections', 'Add ML Model Connections'),
                ('update_ml_model_connections', 'Update ML Model Connections'),
                ('list_ml_model_connections', 'List ML Model Connections'),
                ('delete_ml_model_connections', 'Delete ML Model Connections'),
            ],
            "ML Model Items Permissions": [
                ('add_ml_model_files', 'Add ML Model Files'),
                ('update_ml_model_files', 'Update ML Model Files'),
                ('list_ml_model_files', 'List ML Model Files'),
                ('delete_ml_model_files', 'Delete ML Model Files'),
            ],
            "Function Permissions": [
                ('add_functions', 'Add Functions'),
                ('update_functions', 'Update Functions'),
                ('list_functions', 'List Functions'),
                ('delete_functions', 'Delete Functions')
            ],
            "API Permissions": [
                ('add_apis', 'Add APIs'),
                ('update_apis', 'Update APIs'),
                ('list_apis', 'List APIs'),
                ('delete_apis', 'Delete APIs')
            ],
            "Script Permissions": [
                ('add_scripts', 'Add Scripts'),
                ('update_scripts', 'Update Scripts'),
                ('list_scripts', 'List Scripts'),
                ('delete_scripts', 'Delete Scripts')
            ],
            "Scheduled Job Permissions": [
                ('add_scheduled_jobs', 'Add Scheduled Jobs'),
                ('update_scheduled_jobs', 'Update Scheduled Jobs'),
                ('list_scheduled_jobs', 'List Scheduled Jobs'),
                ('delete_scheduled_jobs', 'Delete Scheduled Jobs')
            ],
            "Trigger Permissions": [
                ('add_triggers', 'Add Triggers'),
                ('update_triggers', 'Update Triggers'),
                ('list_triggers', 'List Triggers'),
                ('delete_triggers', 'Delete Triggers')
            ],
            "Image Generation Permissions": [
                ('can_generate_images', 'Can Generate Images')
            ],
            "Audio Generation Permissions": [
                ('can_generate_audio', 'Can Generate Audio')
            ],
            "Integration Permissions": [
                ('add_integrations', 'Add Integrations'),
                ('update_integrations', 'Update Integrations'),
                ('list_integrations', 'List Integrations'),
                ('delete_integrations', 'Delete Integrations')
            ],
            "Meta Integration Permissions": [
                ('add_meta_integrations', 'Add Meta Integrations'),
                ('update_meta_integrations', 'Update Meta Integrations'),
                ('list_meta_integrations', 'List Meta Integrations'),
                ('delete_meta_integrations', 'Delete Meta Integrations')
            ],
            "Support Ticket Permissions": [
                ('create_support_tickets', 'Create Support Tickets'),
                ('list_support_tickets', 'List Support Tickets'),
                ('update_support_tickets', 'Update Support Tickets'),
            ]
        }
        return permissions_grouped


class ListPermissionsView(LoginRequiredMixin, TemplateView):
    """
    View to list and manage user permissions within organizations.

    This view displays a list of permissions assigned to users in each organization that the logged-in user is associated with. It also allows for updating and deleting these permissions.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with organizations, users, and their associated permissions.
        post(self, request, *args, **kwargs): Handles the logic to update or delete permissions for a user.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_USER_PERMISSIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_USER_PERMISSIONS):
            messages.error(self.request, "You do not have permission to view user permissions.")
            return context
        ##############################

        user = self.request.user
        organizations = Organization.objects.filter(users__in=[user])
        org_users_permissions = {
            org: {"users": {user: user.permissions.all() for user in org.users.all()}} for org in organizations
        }
        context['org_users_permissions'] = org_users_permissions
        return context

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - MODIFY_USER_PERMISSIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.MODIFY_USER_PERMISSIONS):
            messages.error(self.request, "You do not have permission to add/modify permissions.")
            return redirect('user_permissions:list_permissions')
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
        deletion_names = []
        for permission_id in delete_requests:
            permission = get_object_or_404(UserPermission, id=permission_id)
            deletion_names.append(permission.get_permission_type_code())
            permission.delete()
        print('[ListPermissionsView.post] Permissions updated successfully.')
        messages.success(request, 'Permissions updated successfully!')

        # if the user is superuser, add back the permissions to modify and list permissions
        modify_permissions = PermissionNames.MODIFY_USER_PERMISSIONS
        list_permissions = PermissionNames.LIST_USER_PERMISSIONS

        if user.is_superuser:
            UserPermission.objects.get_or_create(user=user, permission_type=modify_permissions)
            UserPermission.objects.get_or_create(user=user, permission_type=list_permissions)
            # set the permissions to be active
            modify_object = UserPermission.objects.get(user=user, permission_type=modify_permissions)
            list_object = UserPermission.objects.get(user=user, permission_type=list_permissions)

            if not modify_object.is_active or not list_object.is_active or modify_permissions in deletion_names or list_permissions in deletion_names:
                # provide information to the user
                messages.warning(request, 'You have removed your permission rights as an administrator, '
                                          'which would have prevented you from granting them back to yourself. '
                                          'We have automatically granted these permissions back to your account.')

            modify_object.is_active = True
            list_object.is_active = True
            modify_object.save()
            list_object.save()

        # Update only the relevant part of the page.
        return render(request, self.template_name, self.get_context_data(**kwargs))
