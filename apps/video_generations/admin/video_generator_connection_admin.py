#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: video_generator_connection_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:45
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib import admin

from apps.video_generations.models import VideoGeneratorConnection
from apps.video_generations.utils import VIDEO_GENERATOR_ADMIN_LIST, VIDEO_GENERATOR_ADMIN_FILTER, \
    VIDEO_GENERATOR_ADMIN_SEARCH


@admin.register(VideoGeneratorConnection)
class VideoGeneratorConnectionAdmin(admin.ModelAdmin):
    list_display = VIDEO_GENERATOR_ADMIN_LIST
    search_fields = VIDEO_GENERATOR_ADMIN_SEARCH
    list_filter = VIDEO_GENERATOR_ADMIN_FILTER
