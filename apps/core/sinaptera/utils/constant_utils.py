#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-12-14 15:36:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-14 15:36:19
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

class SinapteraEvaluationImprovementNitroBoostModels:
    STANDARD = "gpt-4o-mini"
    NITRO = "gpt-4o"

    @staticmethod
    def as_list():
        return [
            SinapteraEvaluationImprovementNitroBoostModels.STANDARD,
            SinapteraEvaluationImprovementNitroBoostModels.NITRO
        ]


class SinapteraCallerTypes:
    ASSISTANT = "Assistant"
    LEANMOD = "LeanMod"
    ORCHESTRATOR = "Orchestrator"
    VOIDFORGER = "VoidForger"

    @staticmethod
    def as_list():
        return [
            SinapteraCallerTypes.ASSISTANT,
            SinapteraCallerTypes.LEANMOD,
            SinapteraCallerTypes.ORCHESTRATOR,
            SinapteraCallerTypes.VOIDFORGER
        ]
