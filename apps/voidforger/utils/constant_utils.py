#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-11-14 21:28:46
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-14 21:28:46
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

from config.settings import BASE_DIR

VOIDFORGER_RUNTIME_STATUSES = [
    ######################
    ('paused', 'Paused'),
    ######################
    ('active', 'Active'),
    ('working', 'Working'),
    ######################
]


class VoidForgerRuntimeStatusesNames:
    PAUSED = 'paused'
    ACTIVE = 'active'
    WORKING = 'working'

    @staticmethod
    def as_list():
        return [
            VoidForgerRuntimeStatusesNames.PAUSED,
            VoidForgerRuntimeStatusesNames.ACTIVE,
            VoidForgerRuntimeStatusesNames.WORKING
        ]


VOIDFORGER_TOGGLE_AUTO_EXECUTION_ACTION_TYPES = [
    ('activated', 'Activated'),
    ('paused', 'Paused'),
    ('end_of_life', 'End of Life'),
]


class VoidForgerToggleAutoExecutionActionTypesNames:
    ACTIVATED = 'activated'
    PAUSED = 'paused'
    END_OF_LIFE = 'end_of_life'

    @staticmethod
    def as_list():
        return [
            VoidForgerToggleAutoExecutionActionTypesNames.ACTIVATED,
            VoidForgerToggleAutoExecutionActionTypesNames.PAUSED,
            VoidForgerToggleAutoExecutionActionTypesNames.END_OF_LIFE
        ]


VOIDFORGER_ACTION_TYPES = [
    ('natural_language_response', 'Natural Language Response'),
    ('intermediary_agent_command', 'Intermediary Agent Command'),
    ('action_log_search_attempt', 'Action Log Search Attempt'),
    ('auto_execution_log_search_attempt', 'Auto Execution Log Search Attempt'),
    ('old_chat_messages_search_attempt', 'Old Chat Messages Search Attempt'),
    ('intermediary_agent_search_attempt', 'Intermediary Agent Search Attempt'),
]


class VoidForgerActionTypesNames:
    NATURAL_LANGUAGE_RESPONSE = 'natural_language_response'
    INTERMEDIARY_AGENT_COMMAND = 'intermediary_agent_command'
    ACTION_LOG_SEARCH_ATTEMPT = 'action_log_search_attempt'
    AUTO_EXECUTION_LOG_SEARCH_ATTEMPT = 'auto_execution_log_search_attempt'
    OLD_CHAT_MESSAGES_SEARCH_ATTEMPT = 'old_chat_messages_search_attempt'
    INTERMEDIARY_AGENT_SEARCH_ATTEMPT = 'intermediary_agent_search_attempt'

    @staticmethod
    def as_list():
        return [
            VoidForgerActionTypesNames.NATURAL_LANGUAGE_RESPONSE,
            VoidForgerActionTypesNames.INTERMEDIARY_AGENT_COMMAND,
            VoidForgerActionTypesNames.ACTION_LOG_SEARCH_ATTEMPT,
            VoidForgerActionTypesNames.AUTO_EXECUTION_LOG_SEARCH_ATTEMPT,
            VoidForgerActionTypesNames.OLD_CHAT_MESSAGES_SEARCH_ATTEMPT,
            VoidForgerActionTypesNames.INTERMEDIARY_AGENT_SEARCH_ATTEMPT
        ]


class OpenAIEmbeddingModels:
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_ADA_V2 = "text-embedding-ada-002"


OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS = 3072

VECTOR_INDEX_PATH_ACTION_MEMORIES = os.path.join(BASE_DIR, 'vectors', 'voidforger_vectors', 'action_memories')
VECTOR_INDEX_PATH_AUTO_EXECUTION_MEMORIES = os.path.join(BASE_DIR, 'vectors', 'voidforger_vectors', 'auto_execution_memories')
VECTOR_INDEX_PATH_CHAT_MESSAGES = os.path.join(BASE_DIR, 'vectors', 'voidforger_vectors', 'chat_messages')

VOIDFORGER_CHAT_ADMIN_LIST = [
    'id',
    'voidforger',
    'user',
    'created_by_user',
    'chat_name',
    'created_at',
    'updated_at'
]
VOIDFORGER_CHAT_ADMIN_FILTER = [
    'voidforger',
    'user',
    'created_by_user',
    'created_at',
    'updated_at'
]
VOIDFORGER_CHAT_ADMIN_SEARCH = [
    'chat_name'
]

VOIDFORGER_CHAT_MESSAGE_ADMIN_LIST = [
    'multimodal_voidforger_chat',
    'sender_type',
    'sent_at'
]
VOIDFORGER_CHAT_MESSAGE_ADMIN_FILTER = [
    'sender_type',
    'sent_at'
]
VOIDFORGER_CHAT_MESSAGE_ADMIN_SEARCH = [
    'multimodal_voidforger_chat',
    'sender_type',
    'sent_at'
]

VOIDFORGER_ADMIN_LIST = (
    'user',
    'llm_model',
    'runtime_status',
    'tone',
    'response_language',
    'created_at',
    'updated_at'
)
VOIDFORGER_ADMIN_FILTER = (
    'runtime_status',
    'tone',
    'response_language'
)
VOIDFORGER_ADMIN_SEARCH = ('user__username',)

VOIDFORGER_ACTION_MEMORY_LOG_ADMIN_LIST = [
    'voidforger',
    'action_type',
    'timestamp'
]
VOIDFORGER_ACTION_MEMORY_LOG_ADMIN_FILTER = [
    'voidforger',
    'action_type',
    'timestamp'
]
VOIDFORGER_ACTION_MEMORY_LOG_ADMIN_SEARCH = [
    'voidforger',
    'action_type',
    'timestamp'
]

VOIDFORGER_TOGGLE_AUTO_EXECUTION_LOG_ADMIN_LIST = [
    'voidforger',
    'action_type',
    'responsible_user',
    'timestamp'
]
VOIDFORGER_TOGGLE_AUTO_EXECUTION_LOG_ADMIN_FILTER = [
    'voidforger',
    'action_type',
    'responsible_user'
]
VOIDFORGER_TOGGLE_AUTO_EXECUTION_LOG_ADMIN_SEARCH = [
    'voidforger__id',
    'action_type',
    'responsible_user__username'
]

VOIDFORGER_ACTION_MEMORY_VECTOR_DATA_ADMIN_LIST = (
    'voidforger_action_memory',
    'created_at',
    'updated_at'
)
VOIDFORGER_ACTION_MEMORY_VECTOR_DATA_ADMIN_FILTER = (
    'voidforger_action_memory',
    'created_at',
    'updated_at'
)
VOIDFORGER_ACTION_MEMORY_VECTOR_DATA_ADMIN_SEARCH = (
    'voidforger_action_memory',
    'created_at',
    'updated_at'
)

VOIDFORGER_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_LIST = [
    'id',
    'voidforger_chat_message',
    'created_at',
    'updated_at'
]
VOIDFORGER_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_FILTER = [
    'voidforger_chat_message',
    'created_at',
    'updated_at'
]
VOIDFORGER_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_SEARCH = [
    'voidforger_chat_message__id'
]

VOIDFORGER_AUTO_EXECUTION_MEMORY_VECTOR_DATA_ADMIN_LIST = (
    'voidforger_auto_execution_memory',
    'created_at',
    'updated_at',
)
VOIDFORGER_AUTO_EXECUTION_MEMORY_VECTOR_DATA_ADMIN_FILTER = (
    'created_at',
    'updated_at',
)
VOIDFORGER_AUTO_EXECUTION_MEMORY_VECTOR_DATA_ADMIN_SEARCH = (
    'voidforger_auto_execution_memory',
    'created_at',
    'updated_at',
)
