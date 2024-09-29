#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: code_repository_chunk_admin.py
#  Last Modified: 2024-09-26 20:30:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:36:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import admin

from apps.datasource_codebase.models import CodeBaseRepositoryChunk


@admin.register(CodeBaseRepositoryChunk)
class CodeBaseRepositoryChunkAdmin(admin.ModelAdmin):
    list_display = ['knowledge_base', 'repository', 'chunk_repository_uri', 'knowledge_base_uuid',
                    'repository_uuid', 'created_at']
    list_filter = ['repository', 'knowledge_base_uuid', 'repository_uuid', 'created_at']
    search_fields = ['repository', 'chunk_content', 'chunk_metadata', 'chunk_repository_uri',
                     'knowledge_base_uuid', 'created_at']
    readonly_fields = ['created_at']

    list_per_page = 20
    list_max_show_all = 100
