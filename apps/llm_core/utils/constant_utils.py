#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


LARGE_LANGUAGE_MODEL_PROVIDERS = [
    ("OA", "OpenAI-GPT"),
]


class LargeLanguageModelProvidersNames:
    OPENAI_GPT = "OpenAI-GPT"

    @staticmethod
    def as_list():
        return [
            LargeLanguageModelProvidersNames.OPENAI_GPT
        ]


GPT_MODEL_NAMES = [
    ("gpt-4o", "gpt-4o"),
    ("gpt-4-turbo", "gpt-4-turbo"),
    ("gpt-4", "gpt-4"),
]


class GPTModelNamesNames:
    GPT_4O = "gpt-4o"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4 = "gpt-4"

    @staticmethod
    def as_list():
        return [
            GPTModelNamesNames.GPT_4O,
            GPTModelNamesNames.GPT_4_TURBO,
            GPTModelNamesNames.GPT_4
        ]


LLM_CORE_ADMIN_LIST = (
    "nickname",
    "provider",
    "model_name",
    "temperature",
    "created_at",
    "updated_at"
)
LLM_CORE_ADMIN_FILTER = (
    "nickname",
    "provider",
    "model_name",
    "temperature",
    "created_at",
    "updated_at"
)
LLM_CORE_ADMIN_SEARCH = (
    "nickname",
    "provider",
    "model_name",
    "temperature",
    "created_at",
    "updated_at"
)
