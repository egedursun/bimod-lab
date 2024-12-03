#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import os

EXPERT_NETWORK_ADMIN_LIST = (
    "organization", "name", "meta_description", "created_by_user", "last_updated_by_user", "created_at", "updated_at"
)
EXPERT_NETWORK_ADMIN_FILTER = (
    "organization", "name", "meta_description", "created_by_user", "last_updated_by_user", "created_at", "updated_at"
)
EXPERT_NETWORK_ADMIN_SEARCH = (
    "organization", "name", "meta_description", "created_by_user", "last_updated_by_user", "created_at", "updated_at"
)
EXPERT_NETWORK_REFERENCE_ADMIN_LIST = (
    "network", "assistant", "context_instructions", "created_by_user", "last_updated_by_user", "created_at",
    "updated_at")
EXPERT_NETWORK_REFERENCE_ADMIN_FILTER = (
    "network", "assistant", "context_instructions", "created_by_user", "last_updated_by_user", "created_at",
    "updated_at")
EXPERT_NETWORK_REFERENCE_ADMIN_SEARCH = (
    "network", "assistant", "context_instructions", "created_by_user", "last_updated_by_user", "created_at",
    "updated_at")
LEAN_ASSISTANT_ADMIN_LIST = (
    "organization", "llm_model", "name",
    "created_by_user", "last_updated_by_user", "created_at", "updated_at")
LEAN_ASSISTANT_ADMIN_FILTER = (
    "organization", "llm_model", "name",
    "created_by_user", "last_updated_by_user", "created_at", "updated_at")
LEAN_ASSISTANT_ADMIN_SEARCH = (
    "organization", "llm_model", "name",
    "created_by_user", "last_updated_by_user", "created_at", "updated_at")

RANDOM_NAME_SUFFIX_MIN_VALUE = 1_000_000_000
RANDOM_NAME_SUFFIX_MAX_VALUE = 9_999_999_999

VECTOR_INDEX_PATH_LEANMOD_CHAT_MESSAGES = os.path.join("vectors", "assistant_vectors", "leanmod_context_memories")

LEANMOD_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_LIST = ['id', 'leanmod_chat_message', 'created_at', 'updated_at']
LEANMOD_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_FILTER = ['leanmod_chat_message', 'created_at', 'updated_at']
LEANMOD_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_SEARCH = ['leanmod_chat_message__id']

