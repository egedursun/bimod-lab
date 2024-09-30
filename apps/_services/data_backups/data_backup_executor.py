#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: data_backup_executor.py
#  Last Modified: 2024-09-30 11:21:25
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-30 11:21:26
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#


from apps.assistants.models import Assistant

from django.core import serializers

from apps.data_security.models import NERIntegration
from apps.llm_core.models import LLMCore
from apps.mm_apis.models import CustomAPI
from apps.mm_functions.models import CustomFunction
from apps.mm_scripts.models import CustomScript

class DataBackupExecutor:
    class BackupLLMModel:
        def __init__(self, organization, responsible_user):
            self.organization = organization
            self.responsible_user = responsible_user

        def backup_llm_models(self, backup_name, password):
            from apps.data_backups.models import DataBackup
            from apps.data_backups.utils import BackupTypesNames

            try:
                queryset = LLMCore.objects.filter(
                    organization=self.organization
                )
                serialized_data = serializers.serialize('json', queryset)

                _ = DataBackup.objects.create(organization=self.organization,
                                              responsible_user=self.responsible_user,
                                              backup_name=backup_name,
                                              backup_type=BackupTypesNames.LLM_MODELS,
                                              serialized_data=serialized_data,
                                              encryption_password=password)

                print("[DataBackupExecutor.backup_llm_models]: Data has been backed up successfully.")
            except Exception as e:
                print("[DataBackupExecutor.backup_llm_models]: ", e)
                return "An error occurred while backing up the data."

            print("[DataBackupExecutor.backup_llm_models]: Data has been backed up successfully.")
            return None

    class BackupNERInstance:
        def __init__(self, organization, responsible_user):
            self.organization = organization
            self.responsible_user = responsible_user

        def backup_ner_instances(self, backup_name, password):
            from apps.data_backups.models import DataBackup
            from apps.data_backups.utils import BackupTypesNames

            try:
                queryset = NERIntegration.objects.filter(
                    organization=self.organization
                )
                serialized_data = serializers.serialize('json', queryset)

                _ = DataBackup.objects.create(organization=self.organization,
                                              responsible_user=self.responsible_user,
                                              backup_name=backup_name,
                                              backup_type=BackupTypesNames.NER_INSTANCES,
                                              serialized_data=serialized_data,
                                              encryption_password=password)

                print("[DataBackupExecutor.backup_ner_instances]: Data has been backed up successfully.")
            except Exception as e:
                print("[DataBackupExecutor.backup_ner_instances]: ", e)
                return "An error occurred while backing up the data."

            print("[DataBackupExecutor.backup_ner_instances]: Data has been backed up successfully.")
            return None

    class BackupAssistant:
        def __init__(self, organization, responsible_user):
            self.organization = organization
            self.responsible_user = responsible_user

        def backup_assistants(self, backup_name, password):
            from apps.data_backups.models import DataBackup
            from apps.data_backups.utils import BackupTypesNames

            try:
                queryset = Assistant.objects.filter(
                    organization=self.organization
                )
                for item in queryset:
                    item: Assistant
                    item.memories.set([])
                serialized_data = serializers.serialize('json', queryset)

                _ = DataBackup.objects.create(organization=self.organization,
                                              responsible_user=self.responsible_user,
                                              backup_name=backup_name,
                                              backup_type=BackupTypesNames.ASSISTANTS,
                                              serialized_data=serialized_data,
                                              encryption_password=password)

                print("[DataBackupExecutor.backup_assistants]: Data has been backed up successfully.")
            except Exception as e:
                print("[DataBackupExecutor.backup_assistants]: ", e)
                return "An error occurred while backing up the data."

            print("[DataBackupExecutor.backup_assistants]: Data has been backed up successfully.")
            return None

    class BackupCustomFunction:
        def __init__(self, organization, responsible_user):
            self.organization = organization
            self.responsible_user = responsible_user

        def backup_custom_functions(self, backup_name, password):
            from apps.data_backups.models import DataBackup
            from apps.data_backups.utils import BackupTypesNames

            try:
                queryset = CustomFunction.objects.filter(
                    created_by_user=self.responsible_user
                )
                serialized_data = serializers.serialize('json', queryset)

                _ = DataBackup.objects.create(organization=self.organization,
                                              responsible_user=self.responsible_user,
                                              backup_name=backup_name,
                                              backup_type=BackupTypesNames.CUSTOM_FUNCTIONS,
                                              serialized_data=serialized_data,
                                              encryption_password=password)

                print("[DataBackupExecutor.backup_custom_functions]: Data has been backed up successfully.")
            except Exception as e:
                print("[DataBackupExecutor.backup_custom_functions]: ", e)
                return "An error occurred while backing up the data."

            print("[DataBackupExecutor.backup_custom_functions]: Data has been backed up successfully.")
            return None

    class BackupCustomAPI:
        def __init__(self, organization, responsible_user):
            self.organization = organization
            self.responsible_user = responsible_user

        def backup_custom_apis(self, backup_name, password):
            from apps.data_backups.models import DataBackup
            from apps.data_backups.utils import BackupTypesNames

            try:
                queryset = CustomAPI.objects.filter(
                    created_by_user=self.responsible_user
                )
                serialized_data = serializers.serialize('json', queryset)

                _ = DataBackup.objects.create(organization=self.organization,
                                              responsible_user=self.responsible_user,
                                              backup_name=backup_name,
                                              backup_type=BackupTypesNames.CUSTOM_APIS,
                                              serialized_data=serialized_data,
                                              encryption_password=password)

                print("[DataBackupExecutor.backup_custom_apis]: Data has been backed up successfully.")
            except Exception as e:
                print("[DataBackupExecutor.backup_custom_apis]: ", e)
                return "An error occurred while backing up the data."

            print("[DataBackupExecutor.backup_custom_apis]: Data has been backed up successfully.")
            return None

    class BackupCustomScript:
        def __init__(self, organization, responsible_user):
            self.organization = organization
            self.responsible_user = responsible_user

        def backup_custom_scripts(self, backup_name, password):
            from apps.data_backups.models import DataBackup
            from apps.data_backups.utils import BackupTypesNames

            try:
                queryset = CustomScript.objects.filter(
                    created_by_user=self.responsible_user
                )
                serialized_data = serializers.serialize('json', queryset)

                _ = DataBackup.objects.create(organization=self.organization,
                                              responsible_user=self.responsible_user,
                                              backup_name=backup_name,
                                              backup_type=BackupTypesNames.CUSTOM_SCRIPTS,
                                              serialized_data=serialized_data,
                                              encryption_password=password)

                print("[DataBackupExecutor.backup_custom_scripts]: Data has been backed up successfully.")
            except Exception as e:
                print("[DataBackupExecutor.backup_custom_scripts]: ", e)
                return "An error occurred while backing up the data."

            print("[DataBackupExecutor.backup_custom_scripts]: Data has been backed up successfully.")
            return None

    @staticmethod
    def restore(backup_object, password):
        try:
            if backup_object.encryption_password != password:
                return "The password is incorrect."

            deserialized_data = serializers.deserialize('json', backup_object.serialized_data)
            print("[DataBackupExecutor.restore_assistants]: Deserialized_data has been generated successfully.")

            for obj in deserialized_data:
                obj: Assistant
                try:
                    obj.save()
                except Exception as e:
                    print(
                        "[DataBackupExecutor.restore_assistants]: There has been an error while saving the object: ",
                        e)
                    return "An error occurred while restoring the data."

        except Exception as e:
            print("[DataBackupExecutor.restore_assistants]: ", e)
            return "An error occurred while restoring the data: " + str(e)

        print("[DataBackupExecutor.restore_assistants]: Data has been restored successfully.")
        return None
