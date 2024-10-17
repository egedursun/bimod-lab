#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: code_repository_storage_forms.py
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
#
#
#

from django import forms

from apps.datasource_codebase.models import CodeRepositoryStorageConnection


class CodeRepositoryStorageForm(forms.ModelForm):
    class Meta:
        model = CodeRepositoryStorageConnection
        fields = [
            'provider', 'host_url', 'provider_api_key', 'assistant', 'name', 'description', 'vectorizer',
            'vectorizer_api_key', 'embedding_chunk_size', 'embedding_chunk_overlap', 'search_instance_retrieval_limit'
        ]
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}
