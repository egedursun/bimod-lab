#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meeting_transcription_delete_views.py
#  Last Modified: 2024-10-28 04:13:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 04:13:15
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.metakanban.models import MetaKanbanMeetingTranscription
from apps.user_permissions.utils import PermissionNames


class MetaKanbanView_MeetingTranscriptionDelete(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        transcription_id = kwargs.get('transcription_id')
        transcription = get_object_or_404(MetaKanbanMeetingTranscription, pk=transcription_id)
        board_id = transcription.board_id

        ##############################
        # PERMISSION CHECK FOR - DELETE_MEETING_TRANSCRIPTION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_MEETING_TRANSCRIPTION):
            messages.error(self.request, "You do not have permission to delete meeting transcription.")
            return redirect('metakanban:meeting_transcription_list', board_id=board_id)
        ##############################

        try:
            transcription.delete()
        except Exception as e:
            messages.error(request, "Meeting transcription could not be deleted.")
            return redirect("metakanban:meeting_transcription_list", board_id=board_id)

        messages.success(request, "Meeting transcription deleted successfully.")
        return redirect("metakanban:meeting_transcription_list", board_id=board_id)
