#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: video_generator_decoder.py
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
import logging

from apps.core.video_generation.utils import VideoGeneratorProviderTypesNames
from apps.core.video_generation.video_generation_executor import VideoGenerationExecutor
from apps.video_generations.models import VideoGeneratorConnection

logger = logging.getLogger(__name__)


class VideoGeneratorDecoder:

    @staticmethod
    def get(
        connection_id: int
    ):

        try:

            connection: VideoGeneratorConnection = VideoGeneratorConnection.objects.get(
                id=connection_id
            )
            logger.info(f"Using {connection.provider} as the video generator system")

        except VideoGeneratorConnection.DoesNotExist:

            logger.error(f"Connection with id {connection_id} does not exist")
            return None

        if connection.provider == VideoGeneratorProviderTypesNames.LUMA_AI:

            logger.info("Using Luma AI as the video generator system")
            return VideoGenerationExecutor(
                connection=connection
            )
