#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: hadron_node_speech_log_admin.py
#  Last Modified: 2024-10-22 14:00:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 14:00:54
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

from apps.hadron_prime.models.hadron_node_speech_log_models import HadronNodeSpeechLog
from apps.hadron_prime.utils import HADRON_NODE_SPEECH_LOG_ADMIN_LIST, HADRON_NODE_SPEECH_LOG_ADMIN_SEARCH, \
    HADRON_NODE_SPEECH_LOG_ADMIN_FILTER


@admin.register(HadronNodeSpeechLog)
class HadronNodeSpeechLogAdmin(admin.ModelAdmin):
    list_display = HADRON_NODE_SPEECH_LOG_ADMIN_LIST
    search_fields = HADRON_NODE_SPEECH_LOG_ADMIN_SEARCH
    list_filter = HADRON_NODE_SPEECH_LOG_ADMIN_FILTER
    ordering = ('-created_at',)
