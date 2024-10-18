#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: hadron_topic_admin.py
#  Last Modified: 2024-10-17 22:18:33
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:18:34
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

from apps.hadron_prime.models import HadronTopic
from apps.hadron_prime.utils import HADRON_TOPIC_ADMIN_LIST, HADRON_TOPIC_ADMIN_FILTER, HADRON_TOPIC_ADMIN_SEARCH


@admin.register(HadronTopic)
class HadronTopicAdmin(admin.ModelAdmin):
    list_display = HADRON_TOPIC_ADMIN_LIST
    list_filter = HADRON_TOPIC_ADMIN_FILTER
    search_fields = HADRON_TOPIC_ADMIN_SEARCH
    ordering = ['-created_at']
