#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:43
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


BIMOD_STREAMING_END_TAG = "<[bimod_streaming_end]>"
BIMOD_PROCESS_END = "<[bimod_process_end]>"
BIMOD_NO_TAG_PLACEHOLDER = "<[bimod_no_tag]>"

SOURCES_FOR_MULTIMODAL_CHATS = [
    ("app", "Application"),
    ("api", "API"),
    ("scheduled", "Scheduled"),
    ("orchestration", "Orchestration"),
    ("drafting", "Drafting"),
    ("formica", "Formica"),
    ("slider", "Slider"),
]


class SourcesForMultimodalChatsNames:
    APP = "app"
    API = "api"
    SCHEDULED = "scheduled"
    TRIGGERED = "triggered"
    ORCHESTRATION = "orchestration"
    DRAFTING = "drafting"
    FORMICA = "formica"
    SLIDER = "slider"


class ChatMessageRoleSenderTypes:
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"
    TOOL = "TOOL"


CHAT_MESSAGE_ROLE_SENDER_TYPES = [
    ("USER", "User"),
    ("ASSISTANT", "Assistant"),
    ("SYSTEM", "System"),
    ("TOOL", "Tool"),
]

MULTIMODAL_CHAT_ADMIN_LIST = [
    'organization',
    'assistant',
    'user',
    'chat_name',
    'created_by_user',
    'created_at',
    'updated_at'
]
MULTIMODAL_CHAT_ADMIN_FILTER = [
    'organization',
    'assistant',
    'user',
    'created_by_user',
    'created_at',
    'updated_at'
]
MULTIMODAL_CHAT_ADMIN_SEARCH = [
    'organization',
    'assistant',
    'user',
    'chat_name',
    'created_by_user',
    'created_at',
    'updated_at'
]

MULTIMODAL_MESSAGE_ADMIN_LIST = [
    'multimodal_chat',
    'sender_type',
    'sent_at'
]
MULTIMODAL_MESSAGE_ADMIN_FILTER = [
    'multimodal_chat',
    'sender_type',
    'sent_at'
]
MULTIMODAL_MESSAGE_ADMIN_SEARCH = [
    'multimodal_chat',
    'sender_type',
    'sent_at'
]

CHAT_CREATION_LOG_ADMIN_LIST = [
    "organization",
    'created_at'
]
CHAT_CREATION_LOG_ADMIN_FILTER = [
    'created_at'
]
CHAT_CREATION_LOG_ADMIN_SEARCH = [
    'created_at'
]

CHAT_MESSAGE_CREATION_LOG_ADMIN_LIST = [
    "organization",
    'created_at'
]
CHAT_MESSAGE_CREATION_LOG_ADMIN_FILTER = [
    'created_at'
]
CHAT_MESSAGE_CREATION_LOG_ADMIN_SEARCH = [
    'created_at'
]

LEAN_CHAT_ADMIN_LIST = [
    'organization',
    'lean_assistant',
    'user',
    'chat_name',
    'created_by_user',
    'created_at',
    'updated_at'
]
LEAN_CHAT_ADMIN_FILTER = [
    'organization',
    'lean_assistant',
    'user',
    'created_by_user',
    'created_at',
    'updated_at'
]
LEAN_CHAT_ADMIN_SEARCH = [
    'organization',
    'lean_assistant',
    'user',
    'chat_name',
    'created_by_user',
    'created_at',
    'updated_at'
]

MULTIMODAL_LEAN_CHAT_MESSAGE_ADMIN_LIST = [
    'multimodal_lean_chat',
    'sender_type',
    'sent_at'
]
MULTIMODAL_LEAN_CHAT_MESSAGE_ADMIN_FILTER = [
    'multimodal_lean_chat',
    'sender_type',
    'sent_at'
]
MULTIMODAL_LEAN_CHAT_MESSAGE_ADMIN_SEARCH = [
    'multimodal_lean_chat',
    'sender_type',
    'sent_at'
]


class ChatPostActionSpecifiers:
    NEW_CHAT_WITH_ASSISTANT_SPECIFIER = 'assistant_id'
    CHANGE_CHAT_NAME_SPECIFIER = 'new_chat_name'
    STARRING_MESSAGE_SPECIFIER = 'starred_message'
