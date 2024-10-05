#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: constant_utils.py
#  Last Modified: 2024-10-02 20:03:45
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:32
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
#  File: constant_utils.py
#  Last Modified: 2024-10-02 19:49:51
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-10-02 19:49:52
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#


HARMONIQ_INPUT_MODES = [
    ('text', 'Text'),
    ('audio', 'Audio'),
]

class HarmoniqInputModesTypes:
    TEXT = 'text'
    AUDIO = 'audio'

    @staticmethod
    def as_list():
        return [HarmoniqInputModesTypes.TEXT, HarmoniqInputModesTypes.AUDIO]
