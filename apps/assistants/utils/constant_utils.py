#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 12:51:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
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


class EmbeddingManagersNames:
    TEXT2VEC_OPENAI = "text2vec-openai"

    @staticmethod
    def as_list():
        return [EmbeddingManagersNames.TEXT2VEC_OPENAI]


AGENT_SPEECH_LANGUAGES = [
    ("auto", "Auto (Detect)"),
    ("en", "English"), ("es", "Spanish"), ("fr", "French"), ("de", "German"), ("it", "Italian"),
    ("pt", "Portuguese"), ("nl", "Dutch"), ("ru", "Russian"), ("ja", "Japanese"), ("ko", "Korean"),
    ("zh", "Chinese"), ("ar", "Arabic"), ("tr", "Turkish"), ("pl", "Polish"), ("sv", "Swedish"),
    ("da", "Danish"), ("fi", "Finnish"), ("no", "Norwegian"), ("he", "Hebrew"), ("id", "Indonesian"),
    ("ms", "Malay"), ("th", "Thai"), ("hi", "Hindi"), ("hu", "Hungarian"), ("cs", "Czech"),
    ("sk", "Slovak"), ("uk", "Ukrainian"), ("ro", "Romanian"), ("bg", "Bulgarian"), ("el", "Greek"),
    ("fi", "Finnish"), ("et", "Estonian"), ("lv", "Latvian"), ("lt", "Lithuanian"), ("hr", "Croatian"),
    ("sr", "Serbian"), ("sl", "Slovenian"), ("mk", "Macedonian"), ("sq", "Albanian"), ("bs", "Bosnian"),
    ("is", "Icelandic"), ("cy", "Welsh"), ("ga", "Irish"),
]

AGENT_SPEECH_LANGUAGES = [AGENT_SPEECH_LANGUAGES[0]] + sorted(AGENT_SPEECH_LANGUAGES[1:],
                                                              key=lambda x: x[1])

CONTEXT_MANAGEMENT_STRATEGY = [
    ("stop", "Stop Conversation"),
    ("forget", "Forget Oldest Messages"),
    ("vectorize", "Vectorize Oldest Messages"),
]


class ContextManagementStrategyNames:
    STOP = "stop"
    FORGET = "forget"
    VECTORIZE = "vectorize"

    @staticmethod
    def as_dict():
        return {
            "stop": "Stop Conversation",
            "forget": "Forget Oldest Messages",
            "vectorize": "Vectorize Oldest Messages",
        }


MULTI_STEP_REASONING_CAPABILITY_CHOICE = [
    ('none', 'None'),
    ('cost-effective', 'Cost Effective'),
    ('high-performance', 'High Performance'),
]


class MultiStepReasoningCapabilityChoicesNames:
    NONE = "none"
    COST_EFFECTIVE = "cost-effective"
    HIGH_PERFORMANCE = "high-performance"

    @staticmethod
    def as_dict():
        return {"none": "None", "cost-effective": "Cost Effective", "high-performance": "High Performance"}


class MultiStepReasoningCapabilityModelNames:
    O1_PREVIEW = "o1-preview"
    O1_MINI = "o1-mini"


AGENT_ADMIN_DISPLAY_FIELDS = (
    "organization",
    "response_language",
    "llm_model", "name",
    "instructions",
    "audience",
    "tone",
    "time_awareness",
    "place_awareness",
    "tool_max_attempts_per_instance",
    "tool_max_chains",
    "document_base_directory",
    "max_retry_count",
    "created_by_user",
    "last_updated_by_user",
    "created_at",
    "updated_at"
)

AGENT_ADMIN_FILTER_FIELDS = (
    "organization",
    "response_language",
    "llm_model",
    "name",
    "instructions",
    "audience",
    "tone",
    "document_base_directory",
    "time_awareness",
    "place_awareness",
    "tool_max_attempts_per_instance",
    "tool_max_chains",
    "max_retry_count",
    "created_by_user",
    "last_updated_by_user",
    "created_at",
    "updated_at"
)

AGENT_ADMIN_SEARCH_FIELDS = (
    "organization",
    "response_language",
    "llm_model",
    "name",
    "instructions",
    "audience",
    "tone",
    "document_base_directory",
    "time_awareness",
    "place_awareness",
    "tool_max_attempts_per_instance",
    "tool_max_chains",
    "max_retry_count",
    "created_by_user",
    "last_updated_by_user",
    "created_at",
    "updated_at"
)

RANDOM_SUFFIX_MINIMUM_VALUE = 1_000_000_000
RANDOM_SUFFIX_MAXIMUM_VALUE = 9_999_999_999

VECTOR_INDEX_PATH_ASSISTANT_CHAT_MESSAGES = os.path.join(BASE_DIR, 'assistant_vectors', 'context_memories')

ASSISTANT_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_LIST = ['id', 'assistant_chat_message', 'created_at', 'updated_at']
ASSISTANT_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_FILTER = ['assistant_chat_message', 'created_at', 'updated_at']
ASSISTANT_OLD_CHAT_MESSAGES_VECTOR_DATA_ADMIN_SEARCH = ['assistant_chat_message__id']
