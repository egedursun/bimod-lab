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


AGENT_STANDARD_MEMORY_TYPES = [
    ("user-specific", "User-Specific"),
    ("assistant-specific", "Assistant-Specific"),
    ("organization-specific", "Organization-Specific"),
]


class AgentStandardMemoryTypesNames:
    USER_SPECIFIC = "user-specific"
    ASSISTANT_SPECIFIC = "assistant-specific"
    ORGANIZATION_SPECIFIC = "organization-specific"

    @staticmethod
    def as_list():
        return [
            AgentStandardMemoryTypesNames.USER_SPECIFIC,
            AgentStandardMemoryTypesNames.ASSISTANT_SPECIFIC,
            AgentStandardMemoryTypesNames.ORGANIZATION_SPECIFIC,
        ]


MEMORIES_ADMIN_LIST = [
    "user",
    "assistant",
    "memory_type",
    "created_at",
    "memory_text_content",
    "created_at",
]

MEMORIES_ADMIN_FILTER = [
    "memory_type"
]
MEMORIES_ADMIN_SEARCH = [
    "user__username",
    "assistant__name"
]
