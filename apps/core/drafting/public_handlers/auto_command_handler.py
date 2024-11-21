#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auto_command_handler.py
#  Last Modified: 2024-10-15 23:32:42
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-15 23:35:41
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

from apps.core.generative_ai.utils import ChatRoles, GPT_DEFAULT_ENCODING_ENGINE
from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames


logger = logging.getLogger(__name__)


def handle_auto_command_public(xc, content: str) -> str:

    from apps.core.drafting.drafting_executor_public import DraftingExecutionManager_Public
    from apps.core.drafting.prompt_builders import build_auto_command_system_prompt_public
    xc: DraftingExecutionManager_Public

    output, error = None, None
    system_prompt = build_auto_command_system_prompt_public(xc=xc, content=content)
    client = xc.naked_c

    try:
        tx = LLMTransaction.objects.create(
            organization=xc.copilot.organization,
            model=xc.copilot_llm,
            responsible_user=xc.document_connection.owner_user,
            responsible_assistant=xc.copilot,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=system_prompt,
            llm_cost=0,
            internal_service_cost=0,
            tax_cost=0,
            total_cost=0,
            total_billable_cost=0,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.DRAFTING
        )
        logger.info(f"[handle_auto_command] Created LLMTransaction for system prompt.")

    except Exception as e:
        logger.error(f"[handle_auto_command] Error creating LLMTransaction for system prompt. Error: {e}")
        pass

    try:
        structured_system_prompt = {
            "content": system_prompt,
            "role": "system"
        }

        llm_response = client.chat.completions.create(
            model=xc.copilot_llm.model_name,
            messages=[
                structured_system_prompt
            ],
            temperature=float(xc.copilot_llm.temperature),
            frequency_penalty=float(xc.copilot_llm.frequency_penalty),
            presence_penalty=float(xc.copilot_llm.presence_penalty),
            max_tokens=int(xc.copilot_llm.maximum_tokens),
            top_p=float(xc.copilot_llm.top_p)
        )

        choices = llm_response.choices
        first_choice = choices[0]
        choice_message = first_choice.message
        choice_message_content = choice_message.content
        logger.info(f"[handle_auto_command] AUTO command response.")

    except Exception as e:
        logger.error(f"[handle_auto_command] Error executing AUTO command. Error: {e}")
        error = f"[handle_ai_command] Error executing AUTO command. Error: {e}"
        return output, error

    try:
        tx = LLMTransaction.objects.create(
            organization=xc.copilot.organization,
            model=xc.copilot_llm,
            responsible_user=xc.document_connection.owner_user,
            responsible_assistant=xc.copilot,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=choice_message_content,
            llm_cost=0,
            internal_service_cost=0,
            tax_cost=0,
            total_cost=0,
            total_billable_cost=0,
            transaction_type=ChatRoles.ASSISTANT,
            transaction_source=LLMTransactionSourcesTypesNames.DRAFTING
        )
        logger.info(f"[handle_auto_command] Created LLMTransaction for AUTO command response.")

    except Exception as e:
        logger.error(f"[handle_auto_command] Error creating LLMTransaction for AUTO command response. Error: {e}")
        pass

    try:
        tx = LLMTransaction(
            organization=xc.copilot.organization,
            model=xc.copilot_llm,
            responsible_user=xc.document_connection.owner_user,
            responsible_assistant=xc.copilot,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.Drafting.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.DRAFTING,
            is_tool_cost=True
        )
        logger.info(f"[handle_auto_command] AUTO command cost.")
        tx.save()

    except Exception as e:
        logger.error(f"[handle_auto_command] Error calculating AUTO command cost. Error: {e}")
        pass

    output = choice_message_content
    return output, error
