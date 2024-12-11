#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: code_repository_storage_admin.py
#  Last Modified: 2024-10-05 01:39:47
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

from django.contrib import admin

from apps.core.codebase.codebase_decoder import (
    CodeBaseDecoder
)

from apps.datasource_codebase.models import (
    CodeRepositoryStorageConnection
)

from apps.datasource_codebase.utils import (
    build_weaviate_class_name_with_random,
    CODE_REPOSITORY_STORAGE_ADMIN_LIST,
    CODE_REPOSITORY_STORAGE_ADMIN_FILTER,
    CODE_REPOSITORY_STORAGE_ADMIN_SEARCH
)


@admin.register(CodeRepositoryStorageConnection)
class CodeRepositoryStorageConnectionAdmin(admin.ModelAdmin):
    list_display = CODE_REPOSITORY_STORAGE_ADMIN_LIST
    list_filter = CODE_REPOSITORY_STORAGE_ADMIN_FILTER
    search_fields = CODE_REPOSITORY_STORAGE_ADMIN_SEARCH

    readonly_fields = [
        'created_at',
        'updated_at'
    ]

    list_per_page = 20
    list_max_show_all = 100

    def save_model(
        self,
        request,
        obj,
        form,
        change
    ):

        if obj.vectorizer is None:
            obj.vectorizer = "text2vec-openai"

        if obj.class_name is None:
            obj.class_name = build_weaviate_class_name_with_random(obj)

        client = CodeBaseDecoder.get(obj)

        if client is not None:
            result = client.create_weaviate_classes()
            if not result["status"]:
                pass

        obj.schema_json = client.retrieve_schema()

        super().save_model(
            request,
            obj,
            form,
            change
        )

    def delete_model(self, request, obj):

        client = CodeBaseDecoder.get(obj)

        if client is not None:
            result = client.delete_weaviate_classes(
                class_name=obj.class_name
            )

            if not result["status"]:
                pass

        super().delete_model(request, obj)
