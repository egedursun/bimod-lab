#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-11-18 20:20:29
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 20:20:29
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import random


def generate_random_object_id_string():
    import random
    random_letter_0 = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random_letter_1 = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random_letter_2 = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    random_number_string = str(
        random.randint(
            100_000,
            999_999
        )
    )

    random_data_object_id_string = f"{random_letter_0}{random_letter_1}{random_letter_2}{random_number_string}"

    return random_data_object_id_string


def extract_username_from_email(email):
    name_prefix = email.split("@")[0]

    numeric_suffix = str(
        random.randint(
            100,
            999
        )
    )

    username = f"{name_prefix}{numeric_suffix}"

    return username


def create_temporary_password():
    uppercase_letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    lowercase_letters = random.choices("abcdefghijklmnopqrstuvwxyz", k=8)

    digits = random.choices("0123456789", k=2)
    special_characters = random.choices("!@#$%&*+=.?", k=2)

    password_characters = [uppercase_letter] + lowercase_letters + digits + special_characters

    random.shuffle(
        password_characters
    )

    temporary_password = "".join(
        password_characters
    )

    return temporary_password
