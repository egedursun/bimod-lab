#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ml_model_storage_admin.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
#

from django.contrib import admin

from apps.datasource_ml_models.models import DataSourceMLModelConnection
from apps.datasource_ml_models.utils import ML_MODEL_MANAGER_ADMIN_LIST, ML_MODEL_MANAGER_ADMIN_FILTER, \
    ML_MODEL_MANAGER_ADMIN_SEARCH


@admin.register(DataSourceMLModelConnection)
class DataSourceMLModelConnectionAdmin(admin.ModelAdmin):
    list_display = ML_MODEL_MANAGER_ADMIN_LIST
    list_filter = ML_MODEL_MANAGER_ADMIN_FILTER
    search_fields = ML_MODEL_MANAGER_ADMIN_SEARCH
    ordering = ('-created_at',)
