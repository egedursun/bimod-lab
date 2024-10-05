MODEL_TYPES = [
    ('gpt-4o-mini', 'GPT-4o Mini'),
    ('gpt-4o', 'GPT-4o'),
    ('gpt-4', 'GPT-4'),
]

FINE_TUNING_MODEL_PROVIDERS = [
    ('openai', 'OpenAI'),
]


#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

class FineTunedModelTypesNames:
    GPT_4O_MINI = 'gpt-4o-mini'
    GPT_4O = 'gpt-4o'
    GPT_4 = 'gpt-4'

    @staticmethod
    def as_list():
        return [
            FineTunedModelTypesNames.GPT_4O_MINI,
            FineTunedModelTypesNames.GPT_4O,
            FineTunedModelTypesNames.GPT_4,
        ]


class FineTuningModelProvidersNames:
    OPENAI = 'openai'

    @staticmethod
    def as_list():
        return [
            FineTuningModelProvidersNames.OPENAI,
        ]
