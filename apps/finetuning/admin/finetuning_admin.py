#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: finetuning_admin.py
#  Last Modified: 2024-10-05 01:39:48
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

from apps.finetuning.models import (
    FineTunedModelConnection
)

from apps.finetuning.utils import (
    FINETUNING_ADMIN_LIST,
    FINETUNING_ADMIN_SEARCH
)


@admin.register(FineTunedModelConnection)
class FineTunedModelConnectionAdmin(admin.ModelAdmin):
    list_display = FINETUNING_ADMIN_LIST
    search_fields = FINETUNING_ADMIN_SEARCH
