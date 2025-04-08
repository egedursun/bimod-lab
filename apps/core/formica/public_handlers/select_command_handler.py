#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: select_command_handler.py
#  Last Modified: 2024-10-31 05:36:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 13:13:17
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

from apps.core.generative_ai.utils import (
    GPT_DEFAULT_ENCODING_ENGINE,
    ChatRoles,
    find_tool_call_from_json,
    Office_Models,
    Office_ChatRoles,
)

from apps.llm_transaction.models import LLMTransaction

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames,
    LLMTokenTypesNames
)

logger = logging.getLogger(__name__)


def handle_select_command_public(
    xc,
    command: str,
    selected_text: str,
    content: str
) -> str:
    from apps.core.formica.formica_executor_public import (
        FormicaExecutionManager_Public
    )

    from apps.core.formica.prompt_builders import (
        build_select_command_system_prompt_public
    )

    xc: FormicaExecutionManager_Public

    try:
        tx = LLMTransaction.objects.create(
            organization=xc.copilot.organization,
            model=xc.copilot_llm,
            responsible_user=xc.document_connection.owner_user,
            responsible_assistant=xc.copilot,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=command,
            transaction_type=ChatRoles.USER,
            transaction_source=LLMTransactionSourcesTypesNames.FORMICA,
            llm_token_type=LLMTokenTypesNames.INPUT,
        )

        logger.info(f"[handle_ai_command] Created LLMTransaction for user command: {command}")

    except Exception as e:
        logger.error(f"[handle_ai_command] Error creating LLMTransaction for user command: {command}. Error: {e}")
        pass

    output, error = None, None

    system_prompt = build_select_command_system_prompt_public(
        xc=xc,
        user_query=command,
        selected_text=selected_text,
        content=content
    )

    client = xc.naked_c

    try:
        tx = LLMTransaction.objects.create(
            organization=xc.copilot.organization,
            model=xc.copilot_llm,
            responsible_user=xc.document_connection.owner_user,
            responsible_assistant=xc.copilot,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=system_prompt,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.FORMICA,
            llm_token_type=LLMTokenTypesNames.INPUT,
        )

        logger.info(f"[handle_ai_command] Created LLMTransaction for system prompt.")

    except Exception as e:
        logger.error(f"[handle_ai_command] Error creating LLMTransaction for system prompt. Error: {e}")
        pass

    try:
        structured_system_prompt = {
            "content": system_prompt,
            "role": Office_ChatRoles.SYSTEM,
        }

        llm_response = client.chat.completions.create(
            model=Office_Models.GPT4O,
            # model=xc.copilot_llm.model_name,
            messages=[
                structured_system_prompt
            ],
            # temperature=float(xc.copilot_llm.temperature),
            # frequency_penalty=float(xc.copilot_llm.frequency_penalty),
            # presence_penalty=float(xc.copilot_llm.presence_penalty),
            # max_tokens=int(xc.copilot_llm.maximum_tokens),
            # top_p=float(xc.copilot_llm.top_p)
        )

        choices = llm_response.choices
        first_choice = choices[0]

        choice_message = first_choice.message
        choice_message_content = choice_message.content

        logger.info(f"[handle_ai_command] Generated AI response.")

    except Exception as e:
        error = f"[handle_ai_command] Error executing SELECT command: {command}. Error: {e}"
        logger.error(error)

        return output, error

    try:
        tx = LLMTransaction.objects.create(
            organization=xc.copilot.organization,
            model=xc.copilot_llm,
            responsible_user=xc.document_connection.owner_user,
            responsible_assistant=xc.copilot,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=choice_message_content,
            transaction_type=ChatRoles.ASSISTANT,
            transaction_source=LLMTransactionSourcesTypesNames.FORMICA,
            llm_token_type=LLMTokenTypesNames.OUTPUT,
        )

        logger.info(f"[handle_ai_command] Created LLMTransaction for AI response.")

    except Exception as e:
        logger.error(f"[handle_ai_command] Error creating LLMTransaction for AI response. Error: {e}")
        pass

    try:
        tx = LLMTransaction(
            organization=xc.copilot.organization,
            model=xc.copilot_llm,
            responsible_user=xc.document_connection.owner_user,
            responsible_assistant=xc.copilot,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.FORMICA,
            is_tool_cost=True,
            llm_token_type=LLMTokenTypesNames.OUTPUT,
        )

        tx.save()

        logger.info(f"[handle_ai_command] SELECT command cost.")

    except Exception as e:
        logger.error(f"[handle_ai_command] Error creating LLMTransaction for SELECT command cost. Error: {e}")
        pass

    try:
        choice_message_content = choice_message_content.replace("```json", "").replace("```", "").replace("`", "")
        choice_message_content = find_tool_call_from_json(choice_message_content)[0]

    except Exception as e:
        print(f"[handle_ai_command] Error parsing AI response. Error: {e}")
        logger.error(f"[handle_ai_command] Error parsing AI response. Error: {e}")

    output = choice_message_content

    return output, error
