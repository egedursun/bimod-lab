#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

#


BIMOD_STREAMING_END_TAG = "<[bimod_streaming_end]>"
BIMOD_PROCESS_END = "<[bimod_process_end]>"
BIMOD_NO_TAG_PLACEHOLDER = "<[bimod_no_tag]>"
CHAT_SOURCES = [
    ("app", "Application"),
    ("api", "API"),
    ("scheduled", "Scheduled"),
    ("orchestration", "Orchestration"),
]


class ChatSourcesNames:
    APP = "app"
    API = "api"
    SCHEDULED = "scheduled"
    TRIGGERED = "triggered"
    ORCHESTRATION = "orchestration"


class MessageSenderTypeNames:
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"
    TOOL = "TOOL"


MESSAGE_SENDER_TYPES = [
    ("USER", "User"),
    ("ASSISTANT", "Assistant"),
    ("SYSTEM", "System"),
    ("TOOL", "Tool"),
]
