#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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

import wonderwords


def build_random_word_string():
    chat_name_1 = wonderwords.RandomWord().word(
        word_min_length=4,
        word_max_length=32,
        include_categories=["noun"],
        regex=r"^[a-zA-Z]+$"
    )

    chat_name_2 = wonderwords.RandomWord().word(
        word_min_length=4,
        word_max_length=32,
        include_categories=["noun"],
        regex=r"^[a-zA-Z]+$"
    )

    chat_name_3 = wonderwords.RandomWord().word(
        word_min_length=4,
        word_max_length=32,
        include_categories=["noun"],
        regex=r"^[a-zA-Z]+$"
    )

    chat_name_1 = chat_name_1.capitalize()
    chat_name_2 = chat_name_2.capitalize()
    chat_name_3 = chat_name_3.capitalize()

    random_digit_string = str(
        random.randint(
            1_000_000,
            9_999_999
        )
    )

    return "".join([
        chat_name_1,
        chat_name_2,
        chat_name_3,
        random_digit_string
    ])


def convert_given_name_to_class_name(given_name: str):
    o = ""

    for char in given_name:

        if char.isalnum() and char not in [
            " ",
            "_",
            "-",
            ".",
            ":",
            ";",
            ",",
            "'",
            '"',
            "!",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "(",
            ")",
            "+",
            "=",
            "{",
            "}",
            "[",
            "]",
            "<",
            ">",
            "?",
            "/",
            "\\",
            "|",
            "`",
            "~",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "0"
        ]:
            o += char

    given_name_alnum_list = o.lower().capitalize()

    return given_name_alnum_list


def generate_repository_uri(
    base_dir,
    document_name,
    file_type
):
    return f"{base_dir}{document_name.split('.')[0]}_{str(random.randint(1_000_000, 9_999_999))}.{file_type}"
