#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: utils.py
#  Last Modified: 2024-08-02 12:34:42
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:14:17
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import datetime
import random
import string


def generate_random_string(length=16):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def generate_referral_code(length=16):
    alphas = string.ascii_uppercase  # 26
    numerics = string.digits  # 10
    year = datetime.datetime.now().year.__str__()
    month = datetime.datetime.now().month.__str__()
    day = datetime.datetime.now().day.__str__()
    generated_alpha = ''.join(random.choice(alphas) for _ in range(length // 2))
    generated_numeric = ''.join(random.choice(numerics) for _ in range(length // 2))
    generated_date = f"{year}-{month}{day}"
    return f"{generated_alpha[0:4]}-{generated_alpha[4:]}-{generated_numeric[0:4]}-{generated_numeric[4:]}-{generated_date}0"
