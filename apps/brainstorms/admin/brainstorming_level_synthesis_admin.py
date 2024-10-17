#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: brainstorming_level_synthesis_admin.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
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

from apps.brainstorms.models import BrainstormingLevelSynthesis
from apps.brainstorms.utils import BRAINSTORMING_LEVEL_SYNTHESIS_ADMIN_LIST, \
    BRAINSTORMING_LEVEL_SYNTHESIS_ADMIN_FILTER, BRAINSTORMING_LEVEL_SYNTHESIS_ADMIN_SEARCH


@admin.register(BrainstormingLevelSynthesis)
class BrainstormingLevelSynthesisAdmin(admin.ModelAdmin):
    list_display = BRAINSTORMING_LEVEL_SYNTHESIS_ADMIN_LIST
    list_filter = BRAINSTORMING_LEVEL_SYNTHESIS_ADMIN_FILTER
    search_fields = BRAINSTORMING_LEVEL_SYNTHESIS_ADMIN_SEARCH
    ordering = ('-created_at',)
