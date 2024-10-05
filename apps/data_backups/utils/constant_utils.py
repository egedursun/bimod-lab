#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
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
