#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: video_generator_decoder.py
#  Last Modified: 2024-10-01 17:08:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-10-01 17:08:59
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#
from apps._services.video_generation.utils import VideoGeneratorProviderTypesNames
from apps._services.video_generation.video_generation_executor import VideoGenerationExecutor
from apps.video_generations.models import VideoGeneratorConnection


class VideoGeneratorDecoder:

    @staticmethod
    def get(connection_id: int):
        try:
            connection: VideoGeneratorConnection = VideoGeneratorConnection.objects.get(id=connection_id)
        except VideoGeneratorConnection.DoesNotExist:
            return None

        if connection.provider == VideoGeneratorProviderTypesNames.LUMA_AI:
            return VideoGenerationExecutor(connection=connection)
