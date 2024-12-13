#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meeting_transcriptions_ai_implement_views.py
#  Last Modified: 2024-10-28 04:13:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 04:13:00
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import (
    get_object_or_404,
    redirect
)

from django.views import View

from apps.core.metakanban.metakanban_execution_handler import (
    MetaKanbanExecutionManager
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.metakanban.models import (
    MetaKanbanMeetingTranscription
)

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class MetaKanbanView_MeetingTranscriptionAIImplement(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        transcription_id = kwargs.get('transcription_id')

        transcription = get_object_or_404(
            MetaKanbanMeetingTranscription,
            pk=transcription_id
        )

        board_id = transcription.board_id

        ##############################
        # PERMISSION CHECK FOR - IMPLEMENT_MEETING_TRANSCRIPTION_WITH_AI
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.IMPLEMENT_MEETING_TRANSCRIPTION_WITH_AI
        ):
            messages.error(self.request, "You do not have permission to implement meeting transcription with AI.")

            return redirect(
                'metakanban:meeting_transcription_list',
                board_id=board_id
            )
        ##############################

        try:
            xc = MetaKanbanExecutionManager(
                board_id=board_id
            )

            success, llm_output = xc.consult_ai(
                user_query=f"""
                --------------------------------
                **MEETING RAW TRANSCRIPT:**
                - Meeting Transcription Timestamp: {transcription.created_at}
                --------------------------------

                '''
                {transcription.meeting_transcription_text}
                '''

                --------------------------------

                **IMPORTANT NOTE:**

                - After you run the commands for updating the Kanban board, share the key takeaways in the meeting
                by checking the transcription text. **DO NOT SHARE** anything other than comma separated takeaways
                in your final response.

                    ________________________________________________________________

                    **Example Final Response with Comma Separated Values:**

                    '''
                    The task must be finalized by EOW, team needs budget, project is currently on track
                    '''

                    ________________________________________________________________

                --------------------------------
            """)

            if not success:
                logger.error("Error executing (meeting transcription) MetaKanban query.")
                messages.error(request, "Error executing (meeting transcription) MetaKanban query.")

                return redirect(
                    'metakanban:meeting_transcription_list',
                    board_id=board_id
                )

            try:
                transcription.ai_implemented = True

                transcription.save()

            except Exception as e:
                logger.error(f"Error saving AI implementation status: {str(e)}")
                messages.error(request, "Error saving AI implementation status.")

                return redirect(
                    'metaKanban:meeting_transcription_list',
                    board_id=board_id
                )

            try:
                key_takeaways_list = llm_output.split(',')

                key_takeaways_list = [
                    key_takeaway.replace("`", "")
                    .replace("'", "")
                    .replace('"', "").strip() for key_takeaway in key_takeaways_list
                ]

                if not key_takeaways_list:
                    raise Exception("No key takeaways found.")

                transcription.meeting_transcription_key_takeaways = key_takeaways_list
                transcription.save()

            except Exception as e:
                logger.error(f"Error saving key takeaways: {str(e)}")
                messages.error(request, "Error saving key takeaways.")

                pass

            messages.success(request, "MetaKanban query executed successfully.")
            logger.info(f"MetaKanban AI implemented for meeting transcription: {transcription_id}")

            return redirect(
                'metakanban:meeting_transcription_list',
                board_id=board_id
            )

        except Exception as e:
            logger.error(f"Error executing (meeting transcription) MetaKanban query: {str(e)}")
            messages.error(request, "Error executing (meeting transcription) MetaKanban query: " + str(e))

            return redirect(
                'metakanban:meeting_transcription_list',
                board_id=board_id
            )
