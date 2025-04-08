#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: agent_communication_views.py
#  Last Modified: 2024-10-28 20:46:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 20:46:18
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
from django.views.generic import TemplateView

from apps.core.generative_ai.utils import (
    GPT_DEFAULT_ENCODING_ENGINE,
    ChatRoles
)

from apps.core.internal_cost_manager.costs_map import (
    InternalServiceCosts
)

from apps.core.metatempo.metatempo_execution_handler import (
    MetaTempoExecutionManager
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.llm_transaction.models import LLMTransaction

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames,
    LLMTokenTypesNames
)

from apps.metakanban.models import MetaKanbanBoard

from apps.metatempo.models import (
    MetaTempoConnection
)

from apps.organization.models import Organization
from apps.projects.models import ProjectItem

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class MetaTempoView_AgentCommunication(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        organization_projects = ProjectItem.objects.filter(
            organization__in=user_orgs
        )

        organization_boards = MetaKanbanBoard.objects.filter(
            project__in=organization_projects
        )

        metatempo_connections = MetaTempoConnection.objects.filter(
            board__in=organization_boards
        )

        context['metatempo_connections'] = metatempo_connections

        return context

    def post(self, request, *args, **kwargs):
        connection_id = request.POST.get('connection_id')

        ##############################
        # PERMISSION CHECK FOR - USE_META_TEMPO_AI
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.USE_META_TEMPO_AI
        ):
            messages.error(self.request, "You do not have permission to use the AI agent for MetaTempo.")

            return redirect('metatempo:agent_communication')
        ##############################

        user_query = request.POST.get('user_query')

        xc = MetaTempoExecutionManager(
            metatempo_connection_id=connection_id
        )

        response_text, error = xc.answer_logs_question(
            user_query=user_query
        )

        if error:
            messages.error(request, "Error executing MetaTempo query.")

            return redirect('metakanban:agent_communication')

        try:
            connection = MetaTempoConnection.objects.get(
                id=connection_id
            )

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

            logger.info(f"[metatempo_agent_communication] Created LLMTransaction for MetaTempo Agent AI Analysis Log.")

        except Exception as e:
            logger.error(
                f"[metatempo_agent_communication] Error creating LLMTransaction for MetaTempo Agent AI Analysis Log. Error: {e}")
            pass

        context = self.get_context_data()

        context.update(
            {
                "llm_output": response_text
            }
        )

        messages.success(request, f"AI agent has been successfully triggered for the selected MetaTempo connection.")

        return self.render_to_response(context)
