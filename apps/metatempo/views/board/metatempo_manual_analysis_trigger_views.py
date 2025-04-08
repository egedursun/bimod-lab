#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metatempo_manual_analysis_trigger_views.py
#  Last Modified: 2024-10-28 20:31:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 20:31:16
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

from django.shortcuts import redirect
from django.views import View

from apps.core.generative_ai.utils import (
    ChatRoles,
    GPT_DEFAULT_ENCODING_ENGINE
)

from apps.core.metatempo.metatempo_execution_handler import (
    MetaTempoExecutionManager
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.llm_transaction.models import (
    LLMTransaction
)

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames,
    LLMTokenTypesNames
)

from apps.metatempo.models import (
    MetaTempoConnection
)

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class MetaTempoView_TriggerManualAnalysis(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        connection_id = kwargs.get('connection_id')

        ##############################
        # PERMISSION CHECK FOR - USE_META_TEMPO_AI
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.USE_META_TEMPO_AI
        ):
            messages.error(self.request, "You do not have permission to trigger manual analysis for a "
                                         "MetaTempo Connection.")

            return redirect(
                'metatempo:main_board',
                connection_id=connection_id
            )
        ##############################

        try:
            connection = MetaTempoConnection.objects.get(
                id=connection_id
            )

            xc = MetaTempoExecutionManager(
                metatempo_connection_id=connection_id
            )

            result, error = xc.interpret_overall_logs()

            if error:
                logger.error(f"[interpret_overall_logs] Error processing overall analysis: {error}")

                return redirect(
                    'metatempo:main_board',
                    connection_id=connection_id
                )

        except Exception as e:
            logger.error(f"[interpret_overall_logs] Exception occurred while creating the analysis: {str(e)}")

            return redirect(
                'metatempo:main_board',
                connection_id=connection_id
            )

        try:
            tx = LLMTransaction(
                organization=connection.board.project.organization,
                model=connection.board.llm_model,
                responsible_user=connection.board.created_by_user,
                responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.METATEMPO,
                is_tool_cost=True,
                llm_token_type=LLMTokenTypesNames.OUTPUT,
            )

            tx.save()

            logger.info(
                f"[interpret_overall_logs] Created LLMTransaction for MetaTempo [MANUAL] Overall Analysis Log."
            )

        except Exception as e:
            logger.error(
                f"[interpret_overall_logs] Error creating LLMTransaction for MetaTempo [MANUAL] Overall Analysis Log. Error: {e}")
            pass

        messages.success(
            request,
            f"Manual analysis has been successfully completed for the selected "
            f"MetaTempo connection."
        )

        return redirect(
            'metatempo:main_board',
            connection_id=connection_id
        )
