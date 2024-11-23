#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

ORCHESTRATION_QUERY_LOG_TYPES = [
    ("user", "User"),
    ("info", "Info"),
    ("error", "Error"),
    ("worker_request", "Worker Request"),
    ("worker_response", "Worker Response"),
    ("maestro_answer", "Maestro Answer"),
]


class OrchestrationQueryLogTypesNames:
    USER = "user"
    INFO = "info"
    ERROR = "error"
    WORKER_REQUEST = "worker_request"
    WORKER_RESPONSE = "worker_response"
    MAESTRO_ANSWER = "maestro_answer"

    @staticmethod
    def as_list():
        return [
            OrchestrationQueryLogTypesNames.INFO,
            OrchestrationQueryLogTypesNames.ERROR,
            OrchestrationQueryLogTypesNames.WORKER_REQUEST,
            OrchestrationQueryLogTypesNames.WORKER_RESPONSE,
            OrchestrationQueryLogTypesNames.MAESTRO_ANSWER
        ]


ORCHESTRATION_RESPONSE_LANGUAGES = [
    ("auto", "Auto (Detect)"),
    ("en", "English"),
    ("es", "Spanish"),
    ("fr", "French"),
    ("de", "German"),
    ("it", "Italian"),
    ("pt", "Portuguese"),
    ("nl", "Dutch"),
    ("ru", "Russian"),
    ("ja", "Japanese"),
    ("ko", "Korean"),
    ("zh", "Chinese"),
    ("ar", "Arabic"),
    ("tr", "Turkish"),
    ("pl", "Polish"),
    ("sv", "Swedish"),
    ("da", "Danish"),
    ("fi", "Finnish"),
    ("no", "Norwegian"),
    ("he", "Hebrew"),
    ("id", "Indonesian"),
    ("ms", "Malay"),
    ("th", "Thai"),
    ("hi", "Hindi"),
    ("hu", "Hungarian"),
    ("cs", "Czech"),
    ("sk", "Slovak"),
    ("uk", "Ukrainian"),
    ("ro", "Romanian"),
    ("bg", "Bulgarian"),
    ("el", "Greek"),
    ("fi", "Finnish"),
    ("et", "Estonian"),
    ("lv", "Latvian"),
    ("lt", "Lithuanian"),
    ("hr", "Croatian"),
    ("sr", "Serbian"),
    ("sl", "Slovenian"),
    ("mk", "Macedonian"),
    ("sq", "Albanian"),
    ("bs", "Bosnian"),
    ("is", "Icelandic"),
    ("cy", "Welsh"),
    ("ga", "Irish"),
]

ORCHESTRATION_RESPONSE_LANGUAGES = [
                                       ORCHESTRATION_RESPONSE_LANGUAGES[0]
                                   ] + sorted(
    ORCHESTRATION_RESPONSE_LANGUAGES[1:],
    key=lambda x: x[1]
)

MAESTRO_ADMIN_LIST = [
    "name",
    "organization",
    "llm_model",
    "created_by_user",
    "last_updated_by_user",
    "created_at",
    "updated_at",
]
MAESTRO_ADMIN_SEARCH = [
    "name",
    "organization",
    "llm_model",
    "created_by_user",
    "last_updated_by_user",
]
MAESTRO_ADMIN_FILTER = [
    "organization",
    "llm_model",
    "created_by_user",
    "last_updated_by_user",
    "created_at",
    "updated_at",
]

MAESTRO_QUERY_ADMIN_LIST = [
    'maestro',
    'query_text',
    'created_by_user',
    'last_updated_by_user',
    'created_at',
    'updated_at'
]

MAESTRO_QUERY_ADMIN_SEARCH = [
    'maestro',
    'query_text',
    'created_by_user',
    'last_updated_by_user'
]
MAESTRO_QUERY_ADMIN_FILTER = [
    'maestro',
    'created_by_user',
    'last_updated_by_user',
    'created_at',
    'updated_at'
]

MAESTRO_QUERY_LOG_ADMIN_LIST = [
    'orchestration_query',
    'log_text_content',
    'created_at'
]
MAESTRO_QUERY_LOG_ADMIN_SEARCH = [
    'orchestration_query',
    'log_text_content'
]
MAESTRO_QUERY_LOG_ADMIN_FILTER = [
    'orchestration_query',
    'created_at'
]

ORCHESTRATION_REACTANT_ASSISTANT_ADMIN_LIST = [
    "orchestration_maestro",
    "assistant",
    "created_by_user",
    "created_at",
    "updated_at"
]
ORCHESTRATION_REACTANT_ASSISTANT_ADMIN_FILTER = [
    "orchestration_maestro",
    "assistant",
    "created_by_user",
    "created_at",
    "updated_at"
]
ORCHESTRATION_REACTANT_ASSISTANT_ADMIN_SEARCH = [
    "orchestration_maestro",
    "assistant",
    "created_by_user",
    "created_at",
    "updated_at"
]
