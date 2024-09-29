#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: constant_utils.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:07:29
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

class ChatRoles:
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    ###
    # Hidden Types (Internal)
    # [i] - TOOL
    ###


ACTIVE_RETRY_COUNT = 0
ACTIVE_TOOL_RETRY_COUNT = 0
ACTIVE_CHAIN_SIZE = 0
DEFAULT_ERROR_MESSAGE = "Failed to respond at the current moment. Please try again later."
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
DEFAULT_STATISTICS_ASSISTANT_NAME_PLACEHOLDER = "Bimod Platform Usage Statistics Assistant"
DEFAULT_STATISTICS_ASSISTANT_AUDIENCE = "Standard / Bimod Application Users"
DEFAULT_STATISTICS_ASSISTANT_TONE = "Formal & Descriptive"
DEFAULT_STATISTICS_ASSISTANT_CHAT_NAME = "Statistics Analysis & Evaluation"
BIMOD_STREAMING_END_TAG = "<[bimod_streaming_end]>"
BIMOD_PROCESS_END = "<[bimod_process_end]>"


class DefaultImageResolutionChoices:
    class Min1024Max1792:
        SQUARE = "1024x1024"
        PORTRAIT = "1024x1792"
        LANDSCAPE = "1792x1024"


class DefaultImageQualityChoices:
    STANDARD = "standard"
    HIGH_DEFINITION = "hd"


class RetryCallersNames:
    RESPOND = "respond"
    RESPOND_STREAM = "respond_stream"


class OpenAITTSVoiceNames:
    ALLOY = "alloy"  # Male Speaker: Baritone
    ECHO = "echo"  # Male Speaker: Baritone-Bass
    FABLE = "fable"  # Male Speaker: Tenor
    ONYX = "onyx"  # Male Speaker: Bass
    NOVA = "nova"  # Female Speaker: Older and Wiser
    SHIMMER = "shimmer"  # Female Speaker: Younger and Energetic
