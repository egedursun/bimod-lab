#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_toggle_auto_execution_memory_vector_data_admin.py
#  Last Modified: 2024-11-15 17:36:49
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 17:36:49
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

from apps.voidforger.models import VoidForgerAutoExecutionMemoryVectorData
from apps.voidforger.utils import VOIDFORGER_AUTO_EXECUTION_MEMORY_VECTOR_DATA_ADMIN_LIST, \
    VOIDFORGER_AUTO_EXECUTION_MEMORY_VECTOR_DATA_ADMIN_FILTER, \
    VOIDFORGER_AUTO_EXECUTION_MEMORY_VECTOR_DATA_ADMIN_SEARCH


@admin.register(VoidForgerAutoExecutionMemoryVectorData)
class VoidForgerAutoExecutionMemoryVectorDataAdmin(admin.ModelAdmin):
    list_display = VOIDFORGER_AUTO_EXECUTION_MEMORY_VECTOR_DATA_ADMIN_LIST
    list_filter = VOIDFORGER_AUTO_EXECUTION_MEMORY_VECTOR_DATA_ADMIN_FILTER
    search_fields = VOIDFORGER_AUTO_EXECUTION_MEMORY_VECTOR_DATA_ADMIN_SEARCH
    ordering = ('-created_at', '-updated_at')
