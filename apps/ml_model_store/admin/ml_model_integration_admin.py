#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ml_model_integration_admin.py
#  Last Modified: 2024-11-08 14:38:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-08 14:38:58
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

from apps.ml_model_store.models import MLModelIntegration
from apps.ml_model_store.utils import ML_MODEL_INTEGRATION_ADMIN_LIST, ML_MODEL_INTEGRATION_ADMIN_FILTER, \
    ML_MODEL_INTEGRATION_ADMIN_SEARCH


@admin.register(MLModelIntegration)
class MLModelIntegrationAdmin(admin.ModelAdmin):
    list_display = ML_MODEL_INTEGRATION_ADMIN_LIST
    list_filter = ML_MODEL_INTEGRATION_ADMIN_FILTER
    search_fields = ML_MODEL_INTEGRATION_ADMIN_SEARCH
    ordering = ["-created_at"]
