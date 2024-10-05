#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: manage_backups_views.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.data_backups.data_backup_executor import DataBackupExecutor
from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.data_backups.models import DataBackup
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout
from apps.data_backups.utils import BACKUP_TYPES, BackupTypesNames


class ManageDataBackupsView(LoginRequiredMixin, TemplateView):
    template_name = 'data_backups/manage_backups.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_DATA_BACKUPS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_DATA_BACKUPS):
            messages.error(self.request, "You do not have permission to list backups.")
            return context
        ##############################

        user_organizations = Organization.objects.filter(
            users__in=[self.request.user]
        )
        backups_list = DataBackup.objects.filter(
            Q(responsible_user=self.request.user) | Q(organization__in=user_organizations)
        ).order_by('-created_at')  # Retrieve backups

        # Initialize the paginator with 10 items per page
        paginator = Paginator(backups_list, 10)

        # Get the current page number from the request
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Pass the page object to the context
        context['page_obj'] = page_obj
        context['organizations'] = user_organizations
        context['backup_types'] = BACKUP_TYPES
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - CREATE_DATA_BACKUPS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CREATE_DATA_BACKUPS):
            messages.error(self.request, "You do not have permission to create backups.")
            return redirect('data_backups:manage')
        ##############################

        organization_id = request.POST.get('organization')
        organization = Organization.objects.get(id=organization_id)
        backup_name = request.POST.get('backup_name')
        backup_password = request.POST.get('backup_password')
        backup_model = request.POST.get('backup_model')

        if organization and backup_name and backup_password and backup_model:

            e = None
            if backup_model == BackupTypesNames.LLM_MODELS:
                executor = DataBackupExecutor.BackupLLMModel(responsible_user=request.user, organization=organization)
                e = executor.backup_llm_models(backup_name=backup_name, password=backup_password)
            elif backup_model == BackupTypesNames.NER_INSTANCES:
                executor = DataBackupExecutor.BackupNERInstance(responsible_user=request.user,
                                                                organization=organization)
                e = executor.backup_ner_instances(backup_name=backup_name, password=backup_password)
            elif backup_model == BackupTypesNames.ASSISTANTS:
                executor = DataBackupExecutor.BackupAssistant(responsible_user=request.user, organization=organization)
                e = executor.backup_assistants(backup_name=backup_name, password=backup_password)
            elif backup_model == BackupTypesNames.CUSTOM_FUNCTIONS:
                executor = DataBackupExecutor.BackupCustomFunction(responsible_user=request.user, organization=None)
                e = executor.backup_custom_functions(backup_name=backup_name, password=backup_password)
            elif backup_model == BackupTypesNames.CUSTOM_APIS:
                executor = DataBackupExecutor.BackupCustomAPI(responsible_user=request.user, organization=None)
                e = executor.backup_custom_apis(backup_name=backup_name, password=backup_password)
            elif backup_model == BackupTypesNames.CUSTOM_SCRIPTS:
                executor = DataBackupExecutor.BackupCustomScript(responsible_user=request.user, organization=None)
                e = executor.backup_custom_scripts(backup_name=backup_name, password=backup_password)
            else:
                e = "Invalid backup model selected."
                messages.error(request, e)

            # Check the result and display appropriate messages
            if e is None:
                messages.success(request, "Backup created successfully!")
            else:
                messages.error(request, "An error occurred while creating the backup.")
        else:
            messages.error(request, "Please provide all the required fields.")
        return redirect('data_backups:manage')
