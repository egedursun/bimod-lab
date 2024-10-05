#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
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
        return [OrchestrationQueryLogTypesNames.INFO, OrchestrationQueryLogTypesNames.ERROR,
                OrchestrationQueryLogTypesNames.WORKER_REQUEST, OrchestrationQueryLogTypesNames.WORKER_RESPONSE,
                OrchestrationQueryLogTypesNames.MAESTRO_ANSWER]


ORCHESTRATION_RESPONSE_LANGUAGES = [
    # User's question language
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
ORCHESTRATION_RESPONSE_LANGUAGES = [ORCHESTRATION_RESPONSE_LANGUAGES[0]] + sorted(ORCHESTRATION_RESPONSE_LANGUAGES[1:],
                                                                                  key=lambda x: x[1])
