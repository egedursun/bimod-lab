#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
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


BACKUP_TYPES = [
    ('assistants', 'Assistants'),
    ('llm_models', 'LLM Models'),
    ('ner_instances', 'NER Instances'),
    ('custom_functions', 'Custom Functions'),
    ('custom_apis', 'Custom APIs'),
    ('custom_scripts', 'Custom Scripts'),
]


class BackupTypesNames:
    ASSISTANTS = 'assistants'
    LLM_MODELS = 'llm_models'
    NER_INSTANCES = 'ner_instances'
    CUSTOM_FUNCTIONS = 'custom_functions'
    CUSTOM_APIS = 'custom_apis'
    CUSTOM_SCRIPTS = 'custom_scripts'

    @staticmethod
    def as_list():
        return [
            BackupTypesNames.ASSISTANTS,
            BackupTypesNames.LLM_MODELS,
            BackupTypesNames.NER_INSTANCES,
            BackupTypesNames.CUSTOM_FUNCTIONS,
            BackupTypesNames.CUSTOM_APIS,
            BackupTypesNames.CUSTOM_SCRIPTS
        ]


DATA_BACKUP_ADMIN_LIST = [
    'organization',
    'responsible_user',
    'backup_name',
    'backup_type',
    'created_at'
]
DATA_BACKUP_ADMIN_SEARCH = [
    'organization',
    'responsible_user__username',
    'backup_name',
    'backup_type'
]
DATA_BACKUP_ADMIN_FILTER = [
    'organization',
    'responsible_user',
    'backup_name',
    'backup_type',
    'created_at'
]
