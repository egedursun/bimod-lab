#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: meeting_recording_audio_ai_delivery_views.py
#  Last Modified: 2024-10-28 03:30:56
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 03:30:57
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

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE, ChatRoles
from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.core.transcriber.transcriber_executor import TranscriberExecutionManager
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames
from apps.metakanban.models import MetaKanbanMeetingTranscription, MetaKanbanBoard

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class MetaKanbanView_MeetingRecordingAudioAIDelivery(View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        board_id = request.POST.get('board_id')
        metakanban_board_api_key = request.POST.get('metakanban_api_key')
        meeting_recording_audio_wav = request.FILES.get('meeting_recording_audio_wav')

        if not board_id:
            return JsonResponse({"success": False, "error": "board_id is required."}, status=400)
        if not metakanban_board_api_key:
            return JsonResponse({"success": False, "error": "metakanban_api_key is required."}, status=400)
        if not meeting_recording_audio_wav:
            return JsonResponse({"success": False, "error": "meeting_recording_audio_wav is required."},
                                status=400)

        try:
            if "Bearer" in metakanban_board_api_key:
                metakanban_board_api_key = metakanban_board_api_key.replace("Bearer", "").strip()
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

        board: MetaKanbanBoard = MetaKanbanBoard.objects.filter(id=board_id).first()
        if not board:
            return JsonResponse({"success": False, "error": "Board not found."}, status=404)
        if board.connection_api_key != metakanban_board_api_key:
            return JsonResponse({"success": False, "error": "Invalid API Key."}, status=401)

        try:
            xc = TranscriberExecutionManager()
            transcription_text, error = xc.transcribe_audio(audio_data=meeting_recording_audio_wav.read())
            if error:
                return JsonResponse({"success": False, "error": error}, status=500)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

        # Save transcription_text to MetaKanbanMeetingTranscription
        MetaKanbanMeetingTranscription.objects.create(
            board_id=board_id,
            meeting_transcription_text=transcription_text,
            is_processed_with_ai=False
        )

        try:
            tx = LLMTransaction(
                organization=board.project.organization, model=board.llm_model,
                responsible_user=board.created_by_user, responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, llm_cost=InternalServiceCosts.MeetingTranscription.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.MEETING_TRANSCRIPTION, is_tool_cost=True
            )
            tx.save()
            logger.info(f"[metakanban_meeting_transcription] Created LLMTransaction for MetaKanban Meeting Transcription.")
        except Exception as e:
            logger.error(
                f"[metakanban_meeting_transcription] Error creating LLMTransaction for MetaKanban Meeting Transcription. Error: {e}")
            pass

        return JsonResponse({"success": True, "error": None}, status=200)
