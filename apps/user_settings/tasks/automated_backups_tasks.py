#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: automated_backups_tasks.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
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
import random

from celery import shared_task
from django.contrib.auth.models import User
from django.utils import timezone

from apps.organization.models import Organization
from apps.data_backups.utils import BackupTypesNames
from apps.core.data_backups.data_backup_executor import DataBackupExecutor


logger = logging.getLogger(__name__)


@shared_task
def initiate_automated_backups():
    users = User.objects.filter(profile__automated_data_backups=True)
    user_orgs = Organization.objects.filter(users__in=users).distinct()
    for org in user_orgs:
        backup_types = BackupTypesNames.as_list()
        for backup_type in backup_types:
            try:
                if backup_type == BackupTypesNames.LLM_MODELS:
                    sample_number = str(random.randint(10000000, 99999999))
                    backup_name = f"PW: {sample_number} | Auto-Backup | LLM Models | {timezone.now().strftime('%Y-%m-%d')}"
                    executor = DataBackupExecutor.BackupLLMModel(organization=org,
                                                                 responsible_user=org.users.first())
                    executor.backup_llm_models(backup_name=backup_name, password=sample_number)
                elif backup_type == BackupTypesNames.NER_INSTANCES:
                    sample_number = str(random.randint(10000000, 99999999))
                    backup_name = f"PW: {sample_number} | Auto-Backup | NER Instances | {timezone.now().strftime('%Y-%m-%d')}"
                    executor = DataBackupExecutor.BackupNERInstance(organization=org,
                                                                    responsible_user=org.users.first())
                    executor.backup_ner_instances(backup_name=backup_name, password=sample_number)
                elif backup_type == BackupTypesNames.ASSISTANTS:
                    sample_number = str(random.randint(10000000, 99999999))
                    backup_name = f"PW: {sample_number} | Auto-Backup | Assistants | {timezone.now().strftime('%Y-%m-%d')}"
                    executor = DataBackupExecutor.BackupAssistant(organization=org,
                                                                  responsible_user=org.users.first())
                elif backup_type == BackupTypesNames.CUSTOM_FUNCTIONS:
                    sample_number = str(random.randint(10000000, 99999999))
                    backup_name = f"PW: {sample_number} | Auto-Backup | Functions | {timezone.now().strftime('%Y-%m-%d')}"
                    executor = DataBackupExecutor.BackupCustomFunction(organization=org,
                                                                       responsible_user=org.users.first())
                    executor.backup_custom_functions(backup_name=backup_name, password=sample_number)
                elif backup_type == BackupTypesNames.CUSTOM_APIS:
                    sample_number = str(random.randint(10000000, 99999999))
                    backup_name = f"PW: {sample_number} | Auto-Backup | APIs | {timezone.now().strftime('%Y-%m-%d')}"
                    executor = DataBackupExecutor.BackupCustomAPI(organization=org,
                                                                  responsible_user=org.users.first())
                    executor.backup_custom_apis(backup_name=backup_name, password=sample_number)
                elif backup_type == BackupTypesNames.CUSTOM_SCRIPTS:
                    sample_number = str(random.randint(10000000, 99999999))
                    backup_name = f"PW: {sample_number} | Auto-Backup | Scripts | {timezone.now().strftime('%Y-%m-%d')}"
                    executor = DataBackupExecutor.BackupCustomScript(organization=org,
                                                                     responsible_user=org.users.first())
                    executor.backup_custom_scripts(backup_name=backup_name, password=sample_number)
                else:
                    logger.error(f"Unknown backup type: {backup_type}")
                    pass
            except Exception as e:
                logger.error(f"Error initiating automated backup for organization {org.id}. Error: {e}")
                continue
    logger.info("Automated backups initiated.")
    return True
