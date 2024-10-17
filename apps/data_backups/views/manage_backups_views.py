#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.data_backups.data_backup_executor import DataBackupExecutor
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.data_backups.models import DataBackup
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout
from apps.data_backups.utils import BACKUP_TYPES, BackupTypesNames


logger = logging.getLogger(__name__)

class DataBackupView_BackupManage(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_DATA_BACKUPS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_DATA_BACKUPS):
            messages.error(self.request, "You do not have permission to list backups.")
            return context
        ##############################

        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        backups_list = DataBackup.objects.filter(
            Q(responsible_user=self.request.user) | Q(organization__in=user_orgs)
        ).order_by('-created_at')
        paginator = Paginator(backups_list, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['organizations'] = user_orgs
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

        org_id = request.POST.get('organization')
        org = Organization.objects.get(id=org_id)
        backup_name = request.POST.get('backup_name')
        backup_password = request.POST.get('backup_password')
        backup_model = request.POST.get('backup_model')
        if org and backup_name and backup_password and backup_model:

            e = None
            if backup_model == BackupTypesNames.LLM_MODELS:
                executor = DataBackupExecutor.BackupLLMModel(responsible_user=request.user, organization=org)
                e = executor.backup_llm_models(backup_name=backup_name, password=backup_password)
            elif backup_model == BackupTypesNames.NER_INSTANCES:
                executor = DataBackupExecutor.BackupNERInstance(responsible_user=request.user, organization=org)
                e = executor.backup_ner_instances(backup_name=backup_name, password=backup_password)
            elif backup_model == BackupTypesNames.ASSISTANTS:
                executor = DataBackupExecutor.BackupAssistant(responsible_user=request.user, organization=org)
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
            if e is None:
                logger.info(f"User: {request.user} - Backup created successfully.")
                messages.success(request, "Backup created successfully!")
            else:
                logger.error(f"User: {request.user} - Backup creation failed. Error: {e}")
                messages.error(request, "An error occurred while creating the backup.")
        else:
            logger.error("User: {request.user} - Backup creation failed.")
            messages.error(request, "Please provide all the required fields.")
        return redirect('data_backups:manage')
