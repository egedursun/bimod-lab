#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: brainstorming_idea_admin.py
#  Last Modified: 2024-10-01 14:26:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: brainstorming_idea_admin.py
#  Last Modified: 2024-10-01 00:23:28
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-10-01 00:24:06
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

from apps.brainstorms.models import BrainstormingIdea


@admin.register(BrainstormingIdea)
class BrainstormingIdeaAdmin(admin.ModelAdmin):
    list_display = (
        'idea_title', 'brainstorming_session', 'created_by_user', 'depth_level', 'is_bookmarked', 'created_at')
    list_filter = ('brainstorming_session', 'created_by_user', 'depth_level', 'is_bookmarked', 'created_at')
    search_fields = ('idea_title', 'idea_description')
    ordering = ('-created_at', 'idea_title', 'brainstorming_session')
