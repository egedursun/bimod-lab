#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: video_generator_connection_admin.py
#  Last Modified: 2024-10-01 17:05:39
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-10-01 17:05:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#


from django.contrib import admin

from apps.video_generations.models import VideoGeneratorConnection


@admin.register(VideoGeneratorConnection)
class VideoGeneratorConnectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'organization', 'assistant')
    search_fields = ('name', 'provider', 'organization__name', 'assistant__name')
    list_filter = ('provider', 'organization', 'assistant')
