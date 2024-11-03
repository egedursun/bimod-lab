#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: repo_command_handler.py
#  Last Modified: 2024-10-21 23:57:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 21:52:09
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import json
import logging

from apps.core.slider.utils import find_tool_call_from_json, SLIDER_TOOL_CALL_MAXIMUM_ATTEMPTS
from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE, ChatRoles
from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.core.tool_calls.core_services.core_service_code_base_query import run_query_code_base
from apps.core.tool_calls.input_verifiers.verify_query_code_base import verify_code_base_query_content
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames

logger = logging.getLogger(__name__)


def handle_repo_command(xc, command: str):
    from apps.core.slider.slider_executor import SliderExecutionManager
    from apps.core.slider.prompt_builders import build_repo_command_system_prompt
    xc: SliderExecutionManager

    try:
        tx = LLMTransaction.objects.create(
            organization=xc.slider_document.organization, model=xc.copilot_llm,
            responsible_user=xc.slider_document.created_by_user, responsible_assistant=xc.copilot,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, transaction_context_content=command,
            llm_cost=0, internal_service_cost=0, tax_cost=0, total_cost=0, total_billable_cost=0,
            transaction_type=ChatRoles.USER, transaction_source=LLMTransactionSourcesTypesNames.SLIDER
        )
        logger.info(f"[handle_ai_command] Created LLMTransaction for user command: {command}")
    except Exception as e:
        logger.error(f"[handle_ai_command] Error creating LLMTransaction for user command: {command}. Error: {e}")
        pass

    output, error = None, None
    system_prompt = build_repo_command_system_prompt(xc=xc, user_query=command)
    client = xc.naked_c

    try:
        tx = LLMTransaction.objects.create(
            organization=xc.slider_document.organization, model=xc.copilot_llm,
            responsible_user=xc.slider_document.created_by_user, responsible_assistant=xc.copilot,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, transaction_context_content=system_prompt,
            llm_cost=0, internal_service_cost=0, tax_cost=0, total_cost=0, total_billable_cost=0,
            transaction_type=ChatRoles.SYSTEM, transaction_source=LLMTransactionSourcesTypesNames.SLIDER
        )
        logger.info(f"[handle_ai_command] Created LLMTransaction for system prompt.")
    except Exception as e:
        logger.error(f"[handle_ai_command] Error creating LLMTransaction for system prompt. Error: {e}")
        pass

    try:
        structured_system_prompt = {"content": system_prompt, "role": "system"}
        llm_response = client.chat.completions.create(
            model=xc.copilot_llm.model_name, messages=[structured_system_prompt],
            temperature=float(xc.copilot_llm.temperature),
            frequency_penalty=float(xc.copilot_llm.frequency_penalty),
            presence_penalty=float(xc.copilot_llm.presence_penalty), max_tokens=int(xc.copilot_llm.maximum_tokens),
            top_p=float(xc.copilot_llm.top_p))
        choices = llm_response.choices
        first_choice = choices[0]
        choice_message = first_choice.message
        choice_message_content = choice_message.content
        logger.info(f"[handle_ai_command] Generated AI response.")

        try:
            tx = LLMTransaction.objects.create(
                organization=xc.slider_document.organization, model=xc.copilot_llm,
                responsible_user=xc.slider_document.created_by_user, responsible_assistant=xc.copilot,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, transaction_context_content=choice_message_content,
                llm_cost=0, internal_service_cost=0, tax_cost=0, total_cost=0, total_billable_cost=0,
                transaction_type=ChatRoles.ASSISTANT, transaction_source=LLMTransactionSourcesTypesNames.SLIDER
            )
            logger.info(f"[handle_ai_command] Created LLMTransaction for AI response.")
        except Exception as e:
            logger.error(f"[handle_ai_command] Error creating LLMTransaction for AI response. Error: {e}")
            pass
    except Exception as e:
        error = f"[handle_ai_command] Error executing VECTOR command: {command}. Error: {e}"
        logger.error(error)
        return output, error

    # TOOL USAGE IDENTIFICATION
    tool_counter = 0
    context_messages = [structured_system_prompt]
    while (len(find_tool_call_from_json(choice_message_content)) > 0 and
           (tool_counter < SLIDER_TOOL_CALL_MAXIMUM_ATTEMPTS)):
        tool_counter += 1
        tool_requests_dicts = find_tool_call_from_json(choice_message_content)
        if len(tool_requests_dicts) > 0:
            for tool_req_dict in tool_requests_dicts:
                defined_tool_descriptor = tool_req_dict.get("tool", "")
                output_tool_call = f"""
                        Tool Response: {defined_tool_descriptor}

                        '''
                    """
                error = verify_code_base_query_content(content=tool_req_dict)
                if error:
                    logger.error(error)
                    return error, None, None, None
                output_tool_call = _handle_tool_code_base_query(tool_usage_dict=tool_req_dict,
                                                                output_tool_call=output_tool_call)
                output_tool_call += """
                        '''
                    """
                context_messages.append({"content": output_tool_call, "role": "system"})
        try:
            llm_response = client.chat.completions.create(
                model=xc.copilot_llm.model_name, messages=context_messages,
                temperature=float(xc.copilot_llm.temperature),
                frequency_penalty=float(xc.copilot_llm.frequency_penalty),
                presence_penalty=float(xc.copilot_llm.presence_penalty), max_tokens=int(xc.copilot_llm.maximum_tokens),
                top_p=float(xc.copilot_llm.top_p))
            choices = llm_response.choices
            first_choice = choices[0]
            choice_message = first_choice.message
            choice_message_content = choice_message.content
            logger.info(f"[handle_ai_command] Generated AI response.")

            try:
                tx = LLMTransaction.objects.create(
                    organization=xc.slider_document.organization, model=xc.copilot_llm,
                    responsible_user=xc.slider_document.created_by_user, responsible_assistant=xc.copilot,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, transaction_context_content=choice_message_content,
                    llm_cost=0, internal_service_cost=0, tax_cost=0, total_cost=0, total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT, transaction_source=LLMTransactionSourcesTypesNames.SLIDER
                )
            except Exception as e:
                logger.error(f"[handle_ai_command] Error creating LLMTransaction for AI response. Error: {e}")
                pass
        except Exception as e:
            logger.error(f"[handle_ai_command] Error executing VECTOR command: {command}. Error: {e}")
            error = f"[handle_ai_command] Error executing VECTOR command: {command}. Error: {e}"
            return output, error

    if tool_counter == SLIDER_TOOL_CALL_MAXIMUM_ATTEMPTS:
        error = (f"[handle_ai_command] Error executing VECTOR command: {command}. Error: Maximum tool call attempts "
                 f"reached.")
        logger.error(error)
        return output, error

    try:
        tx = LLMTransaction(
            organization=xc.copilot.organization, model=xc.copilot_llm,
            responsible_user=xc.slider_document.created_by_user, responsible_assistant=xc.copilot,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, llm_cost=InternalServiceCosts.Slider.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.SLIDER, is_tool_cost=True
        )
        tx.save()
        logger.info(f"[handle_ai_command] Created LLMTransaction for Slider.")
    except Exception as e:
        logger.error(f"[handle_ai_command] Error creating LLMTransaction for Slider. Error: {e}")
        pass

    output = choice_message_content
    return output, error


def _handle_tool_code_base_query(tool_usage_dict, output_tool_call):
    c_id = tool_usage_dict.get("parameters").get("code_base_storage_connection_id")
    query = tool_usage_dict.get("parameters").get("query")
    alpha = tool_usage_dict.get("parameters").get("alpha")
    output = run_query_code_base(c_id=c_id, query_content_str=query, semantic_alpha=alpha)
    output_str = json.dumps(output, sort_keys=True, default=str)
    output_tool_call += output_str
    logger.info(f"[handle_ai_command] Tool Response: {output_tool_call}")
    return output_tool_call
