#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: video_generation_execution_handler.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#

from apps._services.video_generation.utils import VideoGeneratorFrameTypes, VideoGenerationActionTypes
from apps._services.video_generation.video_generation_executor import VideoGenerationExecutor
from apps._services.video_generation.video_generator_decoder import VideoGeneratorDecoder


def execute_video_generation(connection_id: int,
                             action_type: str,
                             query: str,
                             # String 'aspect ratio' operations
                             aspect_ratio=None,
                             # URL for 'start frame' operations
                             start_frame_url=None,
                             # URL for 'end frame' operations
                             end_frame_url=None):
    executor: VideoGenerationExecutor = VideoGeneratorDecoder.get(connection_id=connection_id)
    print(f"[video_generation_execution_handler.execute_video_generation] Retrieved the video generator executor.")

    try:
        if action_type == VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP_AND_ASPECT_RATIO:
            response = executor.text_to_video(query=query, loop=True, with_aspect_ratio=True,
                                              aspect_ratio=aspect_ratio)
        elif action_type == VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_LOOP:
            response = executor.text_to_video(query=query, loop=True, with_aspect_ratio=False)
        elif action_type == VideoGenerationActionTypes.TEXT_TO_VIDEO_WITH_ASPECT_RATIO:
            response = executor.text_to_video(query=query, loop=False, with_aspect_ratio=True,
                                              aspect_ratio=aspect_ratio)
        elif action_type == VideoGenerationActionTypes.TEXT_TO_VIDEO:
            response = executor.text_to_video(query=query, loop=False, with_aspect_ratio=False)
        elif action_type == VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_LOOP_AND_WITH_START_FRAME:
            response = executor.text_and_image_to_video(query=query, loop=True,
                                                        frame_type=VideoGeneratorFrameTypes.START,
                                                        start_frame_url=start_frame_url)
        elif action_type == VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_FRAME:
            response = executor.text_and_image_to_video(query=query, loop=False,
                                                        frame_type=VideoGeneratorFrameTypes.START,
                                                        start_frame_url=start_frame_url)
        elif action_type == VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_END_FRAME:
            response = executor.text_and_image_to_video(query=query, loop=False,
                                                        frame_type=VideoGeneratorFrameTypes.END,
                                                        end_frame_url=end_frame_url)
        elif action_type == VideoGenerationActionTypes.TEXT_AND_IMAGE_TO_VIDEO_WITH_START_AND_END_FRAME:
            response = executor.text_and_image_to_video(query=query, loop=False,
                                                        frame_type=VideoGeneratorFrameTypes.START_AND_END,
                                                        start_frame_url=start_frame_url, end_frame_url=end_frame_url)
        else:
            print("[video_generation_execution_handler.execute_video_generation] The action type is not recognized. "
                  "Please check the action type and try again.")
            return {
                "video_url": None,
                "error": "The action type is not recognized. Please check the action type and try again."
            }

    except Exception as e:
        error = (f"[video_generation_execution_handler.execute_video_generation] Error occurred while generating the "
                 f"image: {str(e)}")
        return {
            "video_url": None,
            "error": error
        }
    print(f"[video_generation_execution_handler.execute_video_generation] Video generated successfully.")
    return response
