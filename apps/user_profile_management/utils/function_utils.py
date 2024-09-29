#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: function_utils.py
#  Last Modified: 2024-09-26 22:43:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:11:18
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import re


def get_card_type(card_number):
    card_types = {
        'visa': r'^4[0-9]{12}(?:[0-9]{3})?$',
        'mastercard': r'^5[1-5][0-9]{14}$',
        'amex': r'^3[47][0-9]{13}$',
    }
    for card_type, pattern in card_types.items():
        if re.match(pattern, card_number):
            return card_type
    return "visa"
