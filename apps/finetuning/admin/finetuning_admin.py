#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import admin

from apps.finetuning.models import FineTunedModelConnection


@admin.register(FineTunedModelConnection)
class FineTunedModelConnectionAdmin(admin.ModelAdmin):
    list_display = ('organization', 'nickname', 'model_name', "provider", 'model_type', 'created_at')
    search_fields = ('organization', 'nickname', 'model_name', "provider", 'model_type', 'model_description')
