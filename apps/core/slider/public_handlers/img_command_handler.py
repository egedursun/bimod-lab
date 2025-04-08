#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: img_command_handler.py
#  Last Modified: 2024-10-31 05:36:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 20:52:04
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

from apps.core.slider.utils import (
    SLIDER_TOOL_CALL_MAXIMUM_ATTEMPTS,
)

from apps.core.generative_ai.utils import (
    GPT_DEFAULT_ENCODING_ENGINE,
    ChatRoles,
    find_tool_call_from_json,
    Office_ChatRoles,
    Office_Models,
)

from apps.core.tool_calls.core_services.core_service_generate_image import (
    run_generate_image
)

from apps.core.tool_calls.input_verifiers.verify_generate_image import (
    verify_generate_image_content
)

from apps.core.tool_calls.utils import (
    IMAGE_GENERATION_AFFIRMATION_PROMPT
)

from apps.llm_transaction.models import LLMTransaction

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames,
    LLMTokenTypesNames
)

from apps.multimodal_chat.models import MultimodalChat

from apps.multimodal_chat.utils import (
    generate_chat_name,
    SourcesForMultimodalChatsNames
)

logger = logging.getLogger(__name__)


def handle_img_command_public(
    xc,
    command: str,
    content: str
) -> str:
    from apps.core.slider.slider_executor_public import (
        SliderExecutionManager_Public
    )

    from apps.core.slider.prompt_builders import (
        build_img_command_system_prompt_public
    )

    xc: SliderExecutionManager_Public

    try:
        tx = LLMTransaction.objects.create(
            organization=xc.copilot.organization,
            model=xc.copilot_llm,
            responsible_user=xc.document_connection.owner_user,
            responsible_assistant=xc.copilot,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=command,
            transaction_type=ChatRoles.USER,
            transaction_source=LLMTransactionSourcesTypesNames.SLIDER,
            llm_token_type=LLMTokenTypesNames.INPUT,
        )

        logger.info(f"[handle_ai_command] Created LLMTransaction for user command: {command}")

    except Exception as e:
        logger.error(f"[handle_ai_command] Error creating LLMTransaction for user command: {command}. Error: {e}")
        pass

    output, error = None, None

    system_prompt = build_img_command_system_prompt_public(
        xc=xc,
        user_query=command,
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
            transaction_source=LLMTransactionSourcesTypesNames.SLIDER,
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
            messages=[structured_system_prompt],
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

        try:
            tx = LLMTransaction.objects.create(
                organization=xc.copilot.organization,
                model=xc.copilot_llm,
                responsible_user=xc.document_connection.owner_user,
                responsible_assistant=xc.copilot,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_context_content=choice_message_content,
                transaction_type=ChatRoles.ASSISTANT,
                transaction_source=LLMTransactionSourcesTypesNames.SLIDER,
                llm_token_type=LLMTokenTypesNames.OUTPUT,
            )
            logger.info(f"[handle_ai_command] Created LLMTransaction for AI response.")

        except Exception as e:
            logger.error(f"[handle_ai_command] Error creating LLMTransaction for AI response. Error: {e}")
            pass

    except Exception as e:
        logger.error(f"[handle_ai_command] Error generating AI response. Error: {e}")
        error = f"[handle_ai_command] Error executing IMG command: {command}. Error: {e}"

        return output, error

    # TOOL USAGE IDENTIFICATION

    tool_counter = 0
    context_messages = [structured_system_prompt]

    while (
        len(find_tool_call_from_json(choice_message_content)) > 0 and
        tool_counter < SLIDER_TOOL_CALL_MAXIMUM_ATTEMPTS
    ):
        tool_counter += 1

        tool_requests_dicts = find_tool_call_from_json(
            choice_message_content
        )

        if len(tool_requests_dicts) > 0:
            for tool_req_dict in tool_requests_dicts:

                error = verify_generate_image_content(
                    content=tool_req_dict
                )

                if error:
                    logger.error(f"[handle_ai_command] Error verifying tool content: {error}")
                    return error, None, None, None

                image_uri = _handle_tool_generate_image(
                    xc=xc,
                    assistant_id=xc.copilot.id,
                    tool_usage_dict=tool_req_dict
                )

                context_messages.append(
                    {
                        "content": image_uri,
                        "role": ChatRoles.SYSTEM,
                    }
                )

                if image_uri and image_uri != "":
                    output = image_uri

                    return output, error

        try:

            llm_response = client.chat.completions.create(
                model=xc.copilot_llm.model_name,
                messages=context_messages,
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

            try:
                tx = LLMTransaction.objects.create(
                    organization=xc.copilot.organization,
                    model=xc.copilot_llm,
                    responsible_user=xc.document_connection.owner_user,
                    responsible_assistant=xc.copilot,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=choice_message_content,
                    transaction_type=ChatRoles.ASSISTANT,
                    transaction_source=LLMTransactionSourcesTypesNames.SLIDER,
                    llm_token_type=LLMTokenTypesNames.OUTPUT,
                )

                logger.info(f"[handle_ai_command] Created LLMTransaction for AI response.")

            except Exception as e:
                logger.error(f"[handle_ai_command] Error creating LLMTransaction for AI response. Error: {e}")
                pass

        except Exception as e:
            logger.error(f"[handle_ai_command] Error generating AI response. Error: {e}")
            error = f"[handle_ai_command] Error executing AI command: {command}. Error: {e}"

            return output, error

    if tool_counter == SLIDER_TOOL_CALL_MAXIMUM_ATTEMPTS:
        error = (f"[handle_ai_command] Error executing IMG command: {command}. Error: Maximum tool call attempts "
                 f"reached.")

        logger.error(error)

        return output, error

    try:
        tx = LLMTransaction(
            organization=xc.copilot.organization,
            model=xc.copilot_llm,
            responsible_user=xc.document_connection.owner_user,
            responsible_assistant=xc.copilot,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.SLIDER,
            is_tool_cost=True,
            llm_token_type=LLMTokenTypesNames.OUTPUT,
        )

        tx.save()

        logger.info(f"[handle_ai_command] Created LLMTransaction for Slider.")

    except Exception as e:
        logger.error(f"[handle_ai_command] Error creating LLMTransaction for Slider. Error: {e}")
        pass

    output = choice_message_content

    return output, error


def _handle_tool_generate_image(
    xc,
    assistant_id,
    tool_usage_dict
):
    prompt = tool_usage_dict.get("parameters").get("prompt")
    size = tool_usage_dict.get("parameters").get("size")
    quality = tool_usage_dict.get("parameters").get("quality")

    temporary_chat = MultimodalChat.objects.create(
        user=xc.copilot.created_by_user,
        organization=xc.copilot.organization,
        assistant=xc.copilot,
        chat_name=generate_chat_name(),
        created_by_user=xc.copilot.created_by_user,
        chat_source=SourcesForMultimodalChatsNames.SLIDER,
    )

    image_generation_response = run_generate_image(
        agent_id=assistant_id,
        chat_id=temporary_chat.id,
        img_generation_prompt=prompt + IMAGE_GENERATION_AFFIRMATION_PROMPT,
        img_dimensions=size,
        img_resolution=quality
    )

    image_uri = image_generation_response.get("image_uri")
    logger.info(f"[handle_ai_command] Generated image: {image_uri}")

    return image_uri
