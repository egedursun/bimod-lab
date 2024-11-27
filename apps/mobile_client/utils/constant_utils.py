#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-11-26 14:21:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-26 14:21:17
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


CONNECTION_TYPES = [
    ('assistant', 'Assistant'),
    ('leanmod', 'LeanMod'),
    ('orchestration', 'Orchestration'),
    ('voidforger', 'VoidForger'),
]


class ConnectionTypesNames:
    ASSISTANT = 'assistant'
    LEANMOD = 'leanmod'
    ORCHESTRATION = 'orchestration'
    VOIDFORGER = 'voidforger'

    @staticmethod
    def as_list():
        return [
            ConnectionTypesNames.ASSISTANT,
            ConnectionTypesNames.LEANMOD,
            ConnectionTypesNames.ORCHESTRATION,
            ConnectionTypesNames.VOIDFORGER
        ]
