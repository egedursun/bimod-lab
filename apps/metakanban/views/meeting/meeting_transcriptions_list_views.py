#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meeting_transcriptions_list_views.py
#  Last Modified: 2024-10-28 04:11:54
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 04:11:55
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import (
    get_object_or_404
)

from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.metakanban.models import (
    MetaKanbanMeetingTranscription,
    MetaKanbanBoard
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout


class MetaKanbanView_MeetingTranscriptionList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        board_id = self.kwargs['board_id']

        board = get_object_or_404(
            MetaKanbanBoard,
            pk=board_id
        )

        ##############################
        # PERMISSION CHECK - USE_METAKANBAN_MEETING_TRANSCRIPTION
        if UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.USE_METAKANBAN_MEETING_TRANSCRIPTION
        ):
            context["board_api_key"] = board.connection_api_key
        ##############################

        transcriptions = MetaKanbanMeetingTranscription.objects.filter(
            board_id=board_id
        ).order_by('-created_at')

        paginator = Paginator(transcriptions, 10)

        page_number = self.request.GET.get('page', 1)

        try:
            page_obj = paginator.get_page(page_number)

        except:
            raise Http404("Page not found.")

        context['page_obj'] = page_obj
        context['board'] = board

        return context
