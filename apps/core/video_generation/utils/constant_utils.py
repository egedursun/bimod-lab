#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 02:31:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

VIDEO_GENERATOR_PROVIDER_TYPES = [
    ('luma-ai', 'Luma AI'),
]


class VideoGeneratorProviderTypesNames:
    LUMA_AI = 'luma-ai'

    @staticmethod
    def as_list():
        return [
            VideoGeneratorProviderTypesNames.LUMA_AI
        ]


class VideoGeneratorFrameTypes:
    START = "start"
    END = "end"
    START_AND_END = "start_and_end"


class LumaAIGenerationStates:
    COMPLETED = "completed"
    FAILED = "failed"


VIDEO_GENERATOR_PING_INTERVAL_SECONDS = 2

UNCLASSIFIED_FILE_EXTENSION = ".bin"


class VideoGenerationActionTypes:
    TEXT_TO_VIDEO_WITH_LOOP_AND_ASPECT_RATIO = "text_to_video_with_loop_and_aspect_ratio"
    TEXT_TO_VIDEO_WITH_LOOP = "text_to_video_with_loop"
    TEXT_TO_VIDEO_WITH_ASPECT_RATIO = "text_to_video_with_aspect_ratio"
    TEXT_TO_VIDEO = "text_to_video"
    TEXT_AND_IMAGE_TO_VIDEO_WITH_LOOP_AND_WITH_START_FRAME = "text_and_image_to_video_with_loop_and_with_start_frame"
    TEXT_AND_IMAGE_TO_VIDEO_WITH_START_FRAME = "text_and_image_to_video_with_start_frame"
    TEXT_AND_IMAGE_TO_VIDEO_WITH_END_FRAME = "text_and_image_to_video_with_end_frame"
    TEXT_AND_IMAGE_TO_VIDEO_WITH_START_AND_END_FRAME = "text_and_image_to_video_with_start_and_end_frame"

    @staticmethod
    def as_list():
        return [
            VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP_AND_ASPECT_RATIO,
            VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP,
            VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_ASPECT_RATIO,
            VideoGenerationActionTypes.TEXT_TO_VIDEO,
            VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_LOOP_AND_WITH_START_FRAME,
            VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_FRAME,
            VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_END_FRAME,
            VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_AND_END_FRAME,
        ]
