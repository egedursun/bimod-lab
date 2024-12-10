#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: s8_determine_action_with_ai_handlers.py
#  Last Modified: 2024-10-17 22:37:12
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:40:11
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

from apps.core.generative_ai.utils import (
    GPT_DEFAULT_ENCODING_ENGINE,
    ChatRoles
)
from apps.core.hadron_prime.parsers import (
    make_request_from_curl
)

from apps.core.hadron_prime.prompt_builders import (
    build_hadron_prime_system_prompt
)

from apps.core.hadron_prime.prompts import (
    verify_hadron_prime_expert_network_query_content
)

from apps.core.hadron_prime.utils import (
    find_tool_call_from_json,
    HADRON_PRIME_TOOL_CALL_MAXIMUM_ATTEMPTS
)

from apps.core.internal_cost_manager.costs_map import (
    InternalServiceCosts
)

from apps.core.tool_calls.leanmod.core_services.core_service_query_expert_network import (
    execute_expert_network_query
)

from apps.hadron_prime.models import HadronNode
from apps.llm_transaction.models import LLMTransaction

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames
)

logger = logging.getLogger(__name__)


def consult_ai(
    node: HadronNode,
    current_state: str,
    goal_state: str,
    error_calculation: str,
    measurements: str,
    topic_messages: str,
    sease_logs: str,
    publish_history_logs: str,
    analytical_data: str,
    action_set_data: str
):
    from apps.core.generative_ai.gpt_openai_manager import (
        OpenAIGPTClientManager
    )

    ai_consultancy_output, command, error = "N/A", "N/A", None

    c = OpenAIGPTClientManager.get_naked_client(
        llm_model=node.llm_model
    )

    system_prompt = build_hadron_prime_system_prompt(
        node=node,
        current_state=current_state,
        goal_state=goal_state,
        error_calculation=error_calculation,
        measurements=measurements,
        topic_messages=topic_messages,
        sease_logs=sease_logs,
        publish_history_logs=publish_history_logs,
        analytical_data=analytical_data,
        action_set_data=action_set_data
    )

    structured_system_prompt = {
        "role": "system",
        "content": str(system_prompt)
    }

    try:
        tx = LLMTransaction.objects.create(
            organization=node.system.organization,
            model=node.llm_model,
            responsible_user=node.created_by_user,
            responsible_assistant=None,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=system_prompt,
            llm_cost=0,
            internal_service_cost=0,
            tax_cost=0,
            total_cost=0,
            total_billable_cost=0,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.HADRON_PRIME
        )

        logger.info(f"[consult_ai] Created LLMTransaction for system prompt: {system_prompt}")

        llm_response = c.chat.completions.create(
            model=node.llm_model.model_name,
            messages=[structured_system_prompt],
            temperature=float(node.llm_model.temperature),
            frequency_penalty=float(
                node.llm_model.frequency_penalty
            ),
            presence_penalty=float(
                node.llm_model.presence_penalty
            ),
            max_tokens=int(
                node.llm_model.maximum_tokens
            ),
            top_p=float(
                node.llm_model.top_p
            )
        )

        choices = llm_response.choices
        first_choice = choices[0]

        choice_message = first_choice.message
        choice_message_content = choice_message.content

        tx = LLMTransaction.objects.create(
            organization=node.system.organization,
            model=node.llm_model,
            responsible_user=node.created_by_user,
            responsible_assistant=None,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=choice_message_content,
            llm_cost=0,
            internal_service_cost=0,
            tax_cost=0,
            total_cost=0,
            total_billable_cost=0,
            transaction_type=ChatRoles.ASSISTANT,
            transaction_source=LLMTransactionSourcesTypesNames.HADRON_PRIME
        )

        logger.info(f"[consult_ai] Created LLMTransaction for AI response.")

    except Exception as e:
        logger.error(f"Error occurred while consulting AI: {str(e)}")
        error = str(e)

        return ai_consultancy_output, command, error

    # TOOL USAGE IDENTIFICATION

    tool_counter = 0
    context_messages = [structured_system_prompt]

    while (
        len(find_tool_call_from_json(choice_message_content)) > 0 and
        tool_counter < HADRON_PRIME_TOOL_CALL_MAXIMUM_ATTEMPTS
    ):
        tool_counter += 1
        tool_requests_dicts = find_tool_call_from_json(choice_message_content)

        if len(tool_requests_dicts) > 0:

            for tool_req_dict in tool_requests_dicts:
                defined_tool_descriptor = tool_req_dict.get("tool", "")
                output_tool_call = f"""
                    Tool Response: {defined_tool_descriptor}

                    '''
                """

                error = verify_hadron_prime_expert_network_query_content(
                    content=tool_req_dict
                )

                if error:
                    logger.error(error)
                    return ai_consultancy_output, command, error

                assistant_id = tool_req_dict.get("parameters").get("assistant_id")
                query = tool_req_dict.get("parameters").get("query")

                image_urls = tool_req_dict.get("parameters").get("image_urls")
                file_urls = tool_req_dict.get("parameters").get("file_urls")

                expert_network_response = execute_expert_network_query(
                    agent_id=assistant_id,
                    xn_query=query,
                    img_uris=image_urls,
                    f_uris=file_urls
                )

                expert_network_response_raw_str = json.dumps(
                    expert_network_response,
                    sort_keys=True,
                    default=str
                )

                output_tool_call += expert_network_response_raw_str

                context_messages.append(
                    {
                        "content": str(output_tool_call),
                        "role": "system"
                    }
                )

        try:
            llm_response = c.chat.completions.create(
                model=node.llm_model.model_name,
                messages=context_messages,
                temperature=float(node.llm_model.temperature),
                frequency_penalty=float(node.llm_model.frequency_penalty),
                presence_penalty=float(node.llm_model.presence_penalty),
                max_tokens=int(node.llm_model.maximum_tokens),
                top_p=float(node.llm_model.top_p)
            )

            choices = llm_response.choices
            first_choice = choices[0]

            choice_message = first_choice.message
            choice_message_content = choice_message.content

            logger.info(f"[consult_ai] Generated AI response again after tool usage.")

            try:

                tx = LLMTransaction.objects.create(
                    organization=node.system.organization,
                    model=node.llm_model,
                    responsible_user=node.created_by_user,
                    responsible_assistant=None,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=choice_message_content,
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.ASSISTANT,
                    transaction_source=LLMTransactionSourcesTypesNames.HADRON_PRIME
                )

                logger.info(f"[consult_ai] Created LLMTransaction for AI response.")

            except Exception as e:
                logger.error(f"[consult_ai] Error creating LLMTransaction for AI response. Error: {e}")
                pass

        except Exception as e:
            logger.error(f"[consult_ai] Error generating AI response. Error: {e}")
            error = f"[consult_ai] Error generating AI response. Error: {e}"

            return ai_consultancy_output, command, error

    if tool_counter == HADRON_PRIME_TOOL_CALL_MAXIMUM_ATTEMPTS:
        logger.error(
            f"[consult_ai] Error generating AI response. Error: Maximum tool call attempts reached."
            f"reached.")

        error = f"[consult_ai] Error generating AI response. Error: Maximum tool call attempts reached."

        return ai_consultancy_output, command, error

    context_messages.append(
        {
            "content": f"""
                ------------------------------

                **YOUR ACTION DECISION WAS THIS:**
                '''
                {str(choice_message_content)}
                '''

                ------------------------------

                **PLEASE PROVIDE A SHORT SUMMARY OF YOUR JUSTIFICATION/RATIONALE FOR THE ACTION CHOICE IN NATURAL LANGUAGE**

                    - DO NOT PASS "A FEW SENTENCES AT MOST".
            """,
            "role": "assistant"
        }
    )

    try:
        command_response = c.chat.completions.create(
            model=node.llm_model.model_name,
            messages=context_messages,
            temperature=float(node.llm_model.temperature),
            frequency_penalty=float(node.llm_model.frequency_penalty),
            presence_penalty=float(node.llm_model.presence_penalty),
            max_tokens=int(node.llm_model.maximum_tokens),
            top_p=float(node.llm_model.top_p)
        )

        choices = command_response.choices
        first_choice = choices[0]

        choice_message = first_choice.message
        command = choice_message.content

        logger.info(f"[consult_ai] Generated AI response for command.")

    except Exception as e:
        logger.error(f"[consult_ai] Error generating AI response for command. Error: {e}")
        error = f"[consult_ai] Error generating AI response for command. Error: {e}"

        return ai_consultancy_output, command, error

    try:
        tx = LLMTransaction(
            organization=node.system.organization,
            model=node.llm_model,
            responsible_user=node.created_by_user,
            responsible_assistant=None,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.HadronPrime.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.HADRON_PRIME,
            is_tool_cost=True
        )

        tx.save()

        logger.info(f"[handle_ai_command] Created LLMTransaction for Hadron Prime.")

    except Exception as e:
        logger.error(f"[handle_ai_command] Error creating LLMTransaction for Hadron Prime. Error: {e}")
        pass

    logger.info("Consulted to AI successfully.")
    ai_consultancy_output = choice_message_content

    return ai_consultancy_output, command, error


def determine_action_with_ai(
    node: HadronNode,
    current_state: str,
    goal_state: str,
    error_calculation: str,
    measurements: str,
    topic_messages: str,
    sease_logs: str,
    publish_history_logs: str,
    analytical_data: str
):
    determined_action, command, error = "N/A", "N/A", None
    action_set_curl = node.action_set_curl

    logger.info("Evaluating action set data.")

    try:
        response_text = make_request_from_curl(
            curl_command=action_set_curl
        )

    except Exception as e:
        logger.error(f"Error occurred while evaluating action set data: {str(e)}")
        error = str(e)

        return determined_action, command, error

    if not response_text:
        logger.error("Analytical data could not have been received.")
        error = "Analytical data could not have been received."

        return determined_action, command, error

    action_set_data = response_text
    logger.info("Action set data has been evaluated.")

    determined_action, command, error = consult_ai(
        node=node,
        current_state=current_state,
        goal_state=goal_state,
        error_calculation=error_calculation,
        measurements=measurements,
        topic_messages=topic_messages,
        sease_logs=sease_logs,
        publish_history_logs=publish_history_logs,
        analytical_data=analytical_data,
        action_set_data=action_set_data
    )

    if error:
        logger.error(f"Error occurred while determining action with AI: {error}")

        return determined_action, command, error

    logger.info("Action determination has been evaluated.")

    return determined_action, command, error
