#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 02:31:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

class ChatRoles:
    SYSTEM = "assistant"
    USER = "user"
    ASSISTANT = "assistant"


ACTIVE_RETRY_COUNT = 0
ACTIVE_TOOL_RETRY_COUNT = 0
ACTIVE_CHAIN_SIZE = 0

DEFAULT_ERROR_MESSAGE = """
    Failed to respond at the current moment. This issue can be related to a variety of reasons, and most of them
    are on the LLM client side. Your balance may not be sufficient from your provider, or the model you are trying to
    use may not be available at the moment. Please try again later or contact the support team for further assistance.
"""

GPT_DEFAULT_ENCODING_ENGINE = "cl100k_base"

CONCRETE_LIMIT_SINGLE_FILE_INTERPRETATION = 20

CONCRETE_LIMIT_ML_MODEL_PREDICTIONS = 10

DEFAULT_IMAGE_GENERATION_MODEL = "dall-e-3"
DEFAULT_IMAGE_MODIFICATION_MODEL = "dall-e-2"
DEFAULT_IMAGE_VARIATION_MODEL = "dall-e-2"
DEFAULT_IMAGE_GENERATION_N = 1
DEFAULT_IMAGE_MODIFICATION_N = 1
DEFAULT_IMAGE_VARIATION_N = 1

DEFAULT_STATISTICS_ANALYSIS_MAX_TOKENS = 4000
DEFAULT_STATISTICS_TEMPERATURE = 0.50
DEFAULT_STATISTICS_ASSISTANT_NAME_PLACEHOLDER = "BimodLab Platform Usage Statistics Assistant"
DEFAULT_STATISTICS_ASSISTANT_AUDIENCE = "Standard / BimodLab Application Users"
DEFAULT_STATISTICS_ASSISTANT_TONE = "Formal & Descriptive"
DEFAULT_STATISTICS_ASSISTANT_CHAT_NAME = "Statistics Analysis & Evaluation"

BIMOD_STREAMING_END_TAG = "<[bimod_streaming_end]>"
BIMOD_PROCESS_END = "<[bimod_process_end]>"


class DefaultImageResolutionChoices:
    class Min1024Max1792:
        SQUARE = "1024x1024"
        PORTRAIT = "1024x1792"
        LANDSCAPE = "1792x1024"


class DefaultImageResolutionChoicesNames:
    SQUARE = "SQUARE"
    PORTRAIT = "PORTRAIT"
    LANDSCAPE = "LANDSCAPE"


class DefaultImageQualityChoices:
    STANDARD = "standard"
    HIGH_DEFINITION = "hd"


class DefaultImageQualityChoicesNames:
    STANDARD = "STANDARD"
    HIGH_DEFINITION = "HIGH_DEFINITION"


class RetryCallersNames:
    RESPOND = "respond"
    RESPOND_STREAM = "respond_stream"


class OpenAITTSVoiceNames:
    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SHIMMER = "shimmer"


DEFAULT_MULTISTEP_REASONING_MAXIMUM_TOKENS = 4000

LLM_CORE_PROVIDERS = {
    "OPENAI": {
        "code": "OA",
        "name": "OpenAI-GPT"
    },
}

TTS_MODEL_NAME = "tts-1"
STT_MODEL_NAME = "whisper-1"

TTS_RETRY_REMOVAL = 3
STT_RETRY_REMOVAL = 3

DEFAULT_AUDIO_MIME_TYPE = "audio/mpeg"
