#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#


ASSISTANT_RESPONSE_LANGUAGES = [
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
ASSISTANT_RESPONSE_LANGUAGES = [ASSISTANT_RESPONSE_LANGUAGES[0]] + sorted(ASSISTANT_RESPONSE_LANGUAGES[1:],
                                                                          key=lambda x: x[1])

CONTEXT_OVERFLOW_STRATEGY = [
    ("stop", "Stop Conversation"),
    ("forget", "Forget Oldest Messages"),
    ("vectorize", "Vectorize Oldest Messages"),
]


class ContextOverflowStrategyNames:
    STOP = "stop"
    FORGET = "forget"
    VECTORIZE = "vectorize"

    @staticmethod
    def as_dict():
        return {"stop": "Stop Conversation", "forget": "Forget Oldest Messages",
                "vectorize": "Vectorize Oldest Messages"}


VECTORIZERS = [
    ("text2vec-openai", "Text2Vec (OpenAI)"),
]


class VectorizerNames:
    TEXT2VEC_OPENAI = "text2vec-openai"

    @staticmethod
    def as_dict():
        return {"text2vec-openai": "Text2Vec (OpenAI)"}


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
