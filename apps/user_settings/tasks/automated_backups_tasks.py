#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: automated_backups_tasks.py
#  Last Modified: 2024-09-30 16:47:04
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: automated_backups_tasks.py
#  Last Modified: 2024-09-30 15:30:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-30 15:31:03
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#
import random

from celery import shared_task
from django.contrib.auth.models import User
from django.utils import timezone

from apps.organization.models import Organization
from apps.data_backups.utils import BackupTypesNames
from apps._services.data_backups.data_backup_executor import DataBackupExecutor


@shared_task
def initiate_automated_backups():
    # Retrieve all users that enabled automated backups
    users = User.objects.filter(
        profile__automated_data_backups=True
    )

    # Retrieve all organizations of all users (distinct)
    user_organizations = Organization.objects.filter(users__in=users).distinct()

    # Iterate over each organization
    for organization in user_organizations:
        # Retrieve the backup types as list
        backup_types = BackupTypesNames.as_list()
        # Iterate of the backup types
        for backup_type in backup_types:
            try:
                if backup_type == BackupTypesNames.LLM_MODELS:
                    sample_number = str(random.randint(10000000, 99999999))
                    backup_name = f"PW: {sample_number} | Auto-Backup | LLM Models | {timezone.now().strftime('%Y-%m-%d')}"
                    executor = DataBackupExecutor.BackupLLMModel(organization=organization,
                                                                 responsible_user=organization.users.first())
                    executor.backup_llm_models(backup_name=backup_name, password=sample_number)
                elif backup_type == BackupTypesNames.NER_INSTANCES:
                    sample_number = str(random.randint(10000000, 99999999))
                    backup_name = f"PW: {sample_number} | Auto-Backup | NER Instances | {timezone.now().strftime('%Y-%m-%d')}"
                    executor = DataBackupExecutor.BackupNERInstance(organization=organization,
                                                                    responsible_user=organization.users.first())
                    executor.backup_ner_instances(backup_name=backup_name, password=sample_number)
                elif backup_type == BackupTypesNames.ASSISTANTS:
                    sample_number = str(random.randint(10000000, 99999999))
                    backup_name = f"PW: {sample_number} | Auto-Backup | Assistants | {timezone.now().strftime('%Y-%m-%d')}"
                    executor = DataBackupExecutor.BackupAssistant(organization=organization,
                                                                  responsible_user=organization.users.first())
                elif backup_type == BackupTypesNames.CUSTOM_FUNCTIONS:
                    sample_number = str(random.randint(10000000, 99999999))
                    backup_name = f"PW: {sample_number} | Auto-Backup | Functions | {timezone.now().strftime('%Y-%m-%d')}"
                    executor = DataBackupExecutor.BackupCustomFunction(organization=organization,
                                                                       responsible_user=organization.users.first())
                    executor.backup_custom_functions(backup_name=backup_name, password=sample_number)
                elif backup_type == BackupTypesNames.CUSTOM_APIS:
                    sample_number = str(random.randint(10000000, 99999999))
                    backup_name = f"PW: {sample_number} | Auto-Backup | APIs | {timezone.now().strftime('%Y-%m-%d')}"
                    executor = DataBackupExecutor.BackupCustomAPI(organization=organization,
                                                                  responsible_user=organization.users.first())
                    executor.backup_custom_apis(backup_name=backup_name, password=sample_number)
                elif backup_type == BackupTypesNames.CUSTOM_SCRIPTS:
                    sample_number = str(random.randint(10000000, 99999999))
                    backup_name = f"PW: {sample_number} | Auto-Backup | Scripts | {timezone.now().strftime('%Y-%m-%d')}"
                    executor = DataBackupExecutor.BackupCustomScript(organization=organization,
                                                                     responsible_user=organization.users.first())
                    executor.backup_custom_scripts(backup_name=backup_name, password=sample_number)
                else:
                    print("[automated_backups_tasks.initiate_automated_backups]: Error occurred while initiating "
                          "automated backups. Backup type not found.")
            except Exception as e:
                print(f"[automated_backups_tasks.initiate_automated_backups]: Error occurred while initiating "
                      f"automated backups. {e}")
                continue

    print(
        f"[automated_backups_tasks.initiate_automated_backups]: Automated backups initiated successfully for {len(user_organizations)} organizations.")
    return True
