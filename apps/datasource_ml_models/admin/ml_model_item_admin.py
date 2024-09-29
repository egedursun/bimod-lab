#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: ml_model_item_admin.py
#  Last Modified: 2024-09-27 23:54:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:47:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import admin

from apps.datasource_ml_models.models import DataSourceMLModelItem


@admin.register(DataSourceMLModelItem)
class DataSourceMLModelItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'ml_model_base', 'ml_model_name', 'description', 'ml_model_size', 'full_file_path',
                    'created_at', 'updated_at')
    list_filter = ('ml_model_base',)
    search_fields = ('ml_model_name', 'full_file_path')
    ordering = ('-created_at',)
