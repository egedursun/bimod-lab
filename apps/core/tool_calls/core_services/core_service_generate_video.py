#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_generate_video.py
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

import logging

from apps.core.video_generation.utils import (
    VideoGeneratorFrameTypes,
    VideoGenerationActionTypes
)

from apps.core.video_generation.video_generation_executor import VideoGenerationExecutor
from apps.core.video_generation.video_generator_decoder import VideoGeneratorDecoder

logger = logging.getLogger(__name__)


def run_generate_video(
    connection_id: int,
    video_generator_action_type: str,
    video_generator_query: str,
    aspect_ratio=None,
    start_frame_url=None,
    end_frame_url=None
):
    xc: VideoGenerationExecutor = VideoGeneratorDecoder.get(
        connection_id=connection_id
    )

    try:
        if video_generator_action_type == VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP_AND_ASPECT_RATIO:

            response = xc.text_to_video(
                query=video_generator_query,
                loop=True,
                with_aspect_ratio=True,
                aspect_ratio=aspect_ratio
            )

        elif video_generator_action_type == VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP:

            response = xc.text_to_video(
                query=video_generator_query,
                loop=True,
                with_aspect_ratio=False
            )

        elif video_generator_action_type == VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_ASPECT_RATIO:

            response = xc.text_to_video(
                query=video_generator_query,
                loop=False,
                with_aspect_ratio=True,
                aspect_ratio=aspect_ratio
            )

        elif video_generator_action_type == VideoGenerationActionTypes.TEXT_TO_VIDEO:

            response = xc.text_to_video(
                query=video_generator_query,
                loop=False,
                with_aspect_ratio=False
            )

        elif video_generator_action_type == VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_LOOP_AND_WITH_START_FRAME:

            response = xc.text_and_image_to_video(
                query=video_generator_query,
                loop=True,
                frame_type=VideoGeneratorFrameTypes.START,
                start_frame_url=start_frame_url
            )

        elif video_generator_action_type == VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_FRAME:

            response = xc.text_and_image_to_video(
                query=video_generator_query,
                loop=False,
                frame_type=VideoGeneratorFrameTypes.START,
                start_frame_url=start_frame_url
            )

        elif video_generator_action_type == VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_END_FRAME:

            response = xc.text_and_image_to_video(
                query=video_generator_query,
                loop=False,
                frame_type=VideoGeneratorFrameTypes.END,
                end_frame_url=end_frame_url
            )

        elif video_generator_action_type == VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_AND_END_FRAME:
            response = xc.text_and_image_to_video(
                query=video_generator_query,
                loop=False,
                frame_type=VideoGeneratorFrameTypes.START_AND_END,
                start_frame_url=start_frame_url,
                end_frame_url=end_frame_url
            )

        else:

            logger.error(f"Invalid action type: {video_generator_action_type}.")
            return {
                "video_url": None,
                "error": "The action type is not recognized. Please check the action type and try again."
            }

    except Exception as e:
        logger.error(f"Error occurred while generating the video: {e}")
        error = f"Error occurred while generating the image: {str(e)}"

        return {
            "video_url": None,
            "error": error
        }

    logger.info(f"Video generation output: {response}")
    return response
