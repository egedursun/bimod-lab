#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: data_backup_executor.py
#  Last Modified: 2024-10-05 02:20:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
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

from apps.assistants.models import Assistant

from django.core import serializers

from apps.data_security.models import NERIntegration
from apps.llm_core.models import LLMCore
from apps.mm_apis.models import CustomAPI
from apps.mm_functions.models import CustomFunction
from apps.mm_scripts.models import CustomScript


logger = logging.getLogger(__name__)

class DataBackupExecutor:
    class BackupLLMModel:
        def __init__(self, organization, responsible_user):
            self.organization = organization
            self.responsible_user = responsible_user

        def backup_llm_models(self, backup_name, password):
            from apps.data_backups.models import DataBackup
            from apps.data_backups.utils import BackupTypesNames
            try:
                queryset = LLMCore.objects.filter(organization=self.organization)
                serialized_data = serializers.serialize('json', queryset)

                _ = DataBackup.objects.create(
                    organization=self.organization, responsible_user=self.responsible_user,
                    backup_name=backup_name, backup_type=BackupTypesNames.LLM_MODELS,
                    serialized_data=serialized_data, encryption_password=password)
                logger.info(f"[DataBackupExecutor.BackupLLMModel.backup_llm_models] Backed up LLM models.")
            except Exception as e:
                logger.error(f"[DataBackupExecutor.BackupLLMModel.backup_llm_models] Error backing up LLM models: {e}")
                return "An error occurred while backing up the data."
            return None

    class BackupNERInstance:
        def __init__(self, organization, responsible_user):
            self.organization = organization
            self.responsible_user = responsible_user

        def backup_ner_instances(self, backup_name, password):
            from apps.data_backups.models import DataBackup
            from apps.data_backups.utils import BackupTypesNames
            try:
                queryset = NERIntegration.objects.filter(organization=self.organization)
                serialized_data = serializers.serialize('json', queryset)
                _ = DataBackup.objects.create(
                    organization=self.organization, responsible_user=self.responsible_user,
                    backup_name=backup_name, backup_type=BackupTypesNames.NER_INSTANCES,
                    serialized_data=serialized_data, encryption_password=password)
                logger.info(f"[DataBackupExecutor.BackupNERInstance.backup_ner_instances] Backed up NER instances.")
            except Exception as e:
                logger.error(f"[DataBackupExecutor.BackupNERInstance.backup_ner_instances] Error backing up NER instances: {e}")
                return "An error occurred while backing up the data."
            return None

    class BackupAssistant:
        def __init__(self, organization, responsible_user):
            self.organization = organization
            self.responsible_user = responsible_user

        def backup_assistants(self, backup_name, password):
            from apps.data_backups.models import DataBackup
            from apps.data_backups.utils import BackupTypesNames
            try:
                queryset = Assistant.objects.filter(organization=self.organization)
                for item in queryset:
                    item: Assistant
                    item.memories.set([])
                serialized_data = serializers.serialize('json', queryset)
                _ = DataBackup.objects.create(
                    organization=self.organization, responsible_user=self.responsible_user,
                    backup_name=backup_name, backup_type=BackupTypesNames.ASSISTANTS,
                    serialized_data=serialized_data, encryption_password=password)
                logger.info(f"[DataBackupExecutor.BackupAssistant.backup_assistants] Backed up assistants.")
            except Exception as e:
                logger.error(f"[DataBackupExecutor.BackupAssistant.backup_assistants] Error backing up assistants: {e}")
                return "An error occurred while backing up the data."
            return None

    class BackupCustomFunction:
        def __init__(self, organization, responsible_user):
            self.organization = organization
            self.responsible_user = responsible_user

        def backup_custom_functions(self, backup_name, password):
            from apps.data_backups.models import DataBackup
            from apps.data_backups.utils import BackupTypesNames
            try:
                queryset = CustomFunction.objects.filter(created_by_user=self.responsible_user)
                serialized_data = serializers.serialize('json', queryset)
                _ = DataBackup.objects.create(
                    organization=self.organization, responsible_user=self.responsible_user,
                    backup_name=backup_name, backup_type=BackupTypesNames.CUSTOM_FUNCTIONS,
                    serialized_data=serialized_data, encryption_password=password)
                logger.info(f"[DataBackupExecutor.BackupCustomFunction.backup_custom_functions] Backed up custom functions.")
            except Exception as e:
                logger.error(f"[DataBackupExecutor.BackupCustomFunction.backup_custom_functions] Error backing up custom functions: {e}")
                return "An error occurred while backing up the data."
            return None

    class BackupCustomAPI:
        def __init__(self, organization, responsible_user):
            self.organization = organization
            self.responsible_user = responsible_user

        def backup_custom_apis(self, backup_name, password):
            from apps.data_backups.models import DataBackup
            from apps.data_backups.utils import BackupTypesNames
            try:
                queryset = CustomAPI.objects.filter(created_by_user=self.responsible_user)
                serialized_data = serializers.serialize('json', queryset)
                _ = DataBackup.objects.create(
                    organization=self.organization, responsible_user=self.responsible_user,
                    backup_name=backup_name, backup_type=BackupTypesNames.CUSTOM_APIS,
                    serialized_data=serialized_data, encryption_password=password)
                logger.info(f"[DataBackupExecutor.BackupCustomAPI.backup_custom_apis] Backed up custom APIs.")
            except Exception as e:
                logger.error(f"[DataBackupExecutor.BackupCustomAPI.backup_custom_apis] Error backing up custom APIs: {e}")
                return "An error occurred while backing up the data."
            return None

    class BackupCustomScript:
        def __init__(self, organization, responsible_user):
            self.organization = organization
            self.responsible_user = responsible_user

        def backup_custom_scripts(self, backup_name, password):
            from apps.data_backups.models import DataBackup
            from apps.data_backups.utils import BackupTypesNames
            try:
                queryset = CustomScript.objects.filter(created_by_user=self.responsible_user)
                serialized_data = serializers.serialize('json', queryset)
                _ = DataBackup.objects.create(
                    organization=self.organization, responsible_user=self.responsible_user,
                    backup_name=backup_name, backup_type=BackupTypesNames.CUSTOM_SCRIPTS,
                    serialized_data=serialized_data, encryption_password=password)
                logger.info(f"[DataBackupExecutor.BackupCustomScript.backup_custom_scripts] Backed up custom scripts.")
            except Exception as e:
                logger.error(f"[DataBackupExecutor.BackupCustomScript.backup_custom_scripts] Error backing up custom scripts: {e}")
                return "An error occurred while backing up the data."
            return None

    @staticmethod
    def restore(backup_object, password):
        try:
            if backup_object.encryption_password != password:
                return "The password is incorrect."
            deserialized_data = serializers.deserialize('json', backup_object.serialized_data)
            for obj in deserialized_data:
                obj: Assistant
                try:
                    obj.save()
                    logger.info(f"[DataBackupExecutor.restore] Restored the data.")
                except Exception as e:
                    logger.error(f"[DataBackupExecutor.restore] Error restoring the data: {e}")
                    return "An error occurred while restoring the data."

        except Exception as e:
            logger.error(f"[DataBackupExecutor.restore] Error restoring the data: {e}")
            return "An error occurred while restoring the data: " + str(e)
        return None
