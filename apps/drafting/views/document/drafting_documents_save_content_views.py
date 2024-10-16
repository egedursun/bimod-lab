#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: drafting_documents_save_content_views.py
#  Last Modified: 2024-10-15 21:18:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-15 21:18:31
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.drafting.models import DraftingDocument


class DraftingView_SaveContent(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        folder_id = self.kwargs['folder_id']
        document_id = self.kwargs['document_id']
        document = get_object_or_404(DraftingDocument, id=document_id)
        document_content = request.POST.get('draft_text')
        if document_content:
            document.document_content_json_quill = document_content
            document.save()
        return redirect('drafting:documents_detail', folder_id=folder_id, document_id=document_id)
