#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metakanban_execution_handler.py
#  Last Modified: 2024-10-23 17:38:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-23 17:38:17
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

from django.utils import timezone

from apps.core.generative_ai.utils import (
    GPT_DEFAULT_ENCODING_ENGINE,
    ChatRoles,
    find_tool_call_from_json,
)

from apps.core.metakanban.builders import (
    build_metakanban_agent_prompts
)

from apps.core.metakanban.tools.metakanban_command_query_runner import (
    run_metakanban_command_query
)

from apps.core.metakanban.tools.metakanban_command_query_verifier import (
    verify_metakanban_command_query_content
)

from apps.core.metakanban.utils import (
    METAKANBAN_TOOL_COMMAND_MAXIMUM_ATTEMPTS
)

from apps.llm_transaction.models import LLMTransaction

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames,
    LLMTokenTypesNames
)

from apps.metakanban.models import MetaKanbanBoard

logger = logging.getLogger(__name__)


class MetaKanbanExecutionManager:

    def __init__(self, board_id: int):
        from apps.core.generative_ai.gpt_openai_manager import (
            OpenAIGPTClientManager
        )

        self.board: MetaKanbanBoard = MetaKanbanBoard.objects.get(
            id=board_id
        )

        self.llm_model = self.board.llm_model

        self.c = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.llm_model
        )

    def consult_ai(self, user_query: str):
        try:
            system_prompt = build_metakanban_agent_prompts(
                board=self.board
            )

            output, error = self.handle_metakanban_operation_command(
                system_prompt=system_prompt,
                query=user_query
            )

        except Exception as e:
            error = f"[handle_metakanban_operation_command] Error executing MetaKanban query: {user_query}. Error: {e}"
            logger.error(error)

            return False, ""

        logger.info(f"[handle_metakanban_operation_command] AI response: {output}")

        return True, output

    def handle_metakanban_operation_command(
        self,
        system_prompt: str,
        query: str
    ):

        output, error = None, None

        context_messages = [
            {
                "content": system_prompt,
                "role": ChatRoles.SYSTEM,
            },
            {
                "content": query,
                "role": ChatRoles.USER,
            }
        ]

        try:
            tx = LLMTransaction.objects.create(
                organization=self.board.project.organization,
                model=self.llm_model,
                responsible_user=self.board.created_by_user,
                responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_context_content=str(system_prompt),
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.METAKANBAN,
                llm_token_type=LLMTokenTypesNames.INPUT,
            )

            logger.info(f"[handle_metakanban_operation_command] Created LLMTransaction for system prompt.")

        except Exception as e:
            logger.error(
                f"[handle_metakanban_operation_command] Error creating LLMTransaction for system prompt. Error: {e}")
            pass

        try:
            tx = LLMTransaction.objects.create(
                organization=self.board.project.organization,
                model=self.llm_model,
                responsible_user=self.board.created_by_user,
                responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_context_content=str(query),
                transaction_type=ChatRoles.USER,
                transaction_source=LLMTransactionSourcesTypesNames.METAKANBAN,
                llm_token_type=LLMTokenTypesNames.OUTPUT,
            )

            logger.info(f"[handle_metakanban_operation_command] Created LLMTransaction for user prompt.")

        except Exception as e:
            logger.error(
                f"[handle_metakanban_operation_command] Error creating LLMTransaction for user prompt. Error: {e}")
            pass

        try:
            llm_response = self.c.chat.completions.create(
                model=self.llm_model.model_name,
                messages=context_messages,
                # temperature=float(self.llm_model.temperature),
                # frequency_penalty=float(self.llm_model.frequency_penalty),
                # presence_penalty=float(self.llm_model.presence_penalty),
                # max_tokens=int(self.llm_model.maximum_tokens),
                # top_p=float(self.llm_model.top_p)
            )

            choices = llm_response.choices
            first_choice = choices[0]

            choice_message = first_choice.message
            choice_message_content = choice_message.content

            logger.info(f"[handle_metakanban_operation_command] Generated AI response.")

            try:
                tx = LLMTransaction.objects.create(
                    organization=self.board.project.organization,
                    model=self.llm_model,
                    responsible_user=self.board.created_by_user,
                    responsible_assistant=None,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=str(choice_message_content),
                    transaction_type=ChatRoles.ASSISTANT,
                    transaction_source=LLMTransactionSourcesTypesNames.METAKANBAN,
                    llm_token_type=LLMTokenTypesNames.OUTPUT,
                )

                logger.info(
                    f"[handle_metakanban_operation_command] Created LLMTransaction for assistant response (primary).")

            except Exception as e:
                logger.error(
                    f"[handle_metakanban_operation_command] Error creating LLMTransaction for assistant response (primary). Error: {e}")
                pass

        except Exception as e:
            error = f"[handle_metakanban_operation_command] Error executing MetaKanban query: {query}. Error: {e}"
            logger.error(error)

            return output, error

        # BACKUP MECHANISM TO HANDLE INCORRECT REQUESTS
        if len(find_tool_call_from_json(choice_message_content)) == 0:

            context_messages.append(
                {
                    "content": f"""
                -----
                **FATAL ERROR**

                - **DO NOT MAKE NATURAL LANGUAGE RESPONSES.**

                [ERROR] You are not outputting a tool call. You must output a tool call with JSON output. You MUST NOT
                output a natural language response. You must output a tool call with JSON output. You MUST NOT output a
                natural language response. You must output a tool call with JSON output. You MUST NOT output a natural
                language response. You must output a tool call with JSON output. You MUST NOT output a natural language
                response.

                -----
            """,
                    "role": ChatRoles.SYSTEM,
                }
            )

            llm_response = self.c.chat.completions.create(
                model=self.llm_model.model_name,
                messages=context_messages,
                # temperature=float(self.llm_model.temperature),
                # frequency_penalty=float(self.llm_model.frequency_penalty),
                # presence_penalty=float(self.llm_model.presence_penalty),
                # max_tokens=int(self.llm_model.maximum_tokens),
                # top_p=float(self.llm_model.top_p)
            )

            choices = llm_response.choices
            first_choice = choices[0]

            choice_message = first_choice.message
            choice_message_content = choice_message.content

            logger.info(f"[handle_metakanban_operation_command] Generated AI response.")

            try:
                tx = LLMTransaction.objects.create(
                    organization=self.board.project.organization,
                    model=self.llm_model,
                    responsible_user=self.board.created_by_user,
                    responsible_assistant=None,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=str(choice_message_content),
                    transaction_type=ChatRoles.ASSISTANT,
                    transaction_source=LLMTransactionSourcesTypesNames.METAKANBAN,
                    llm_token_type=LLMTokenTypesNames.OUTPUT,
                )

                logger.info(
                    f"[handle_metakanban_operation_command] Created LLMTransaction for assistant response (backup).")

            except Exception as e:
                logger.error(
                    f"[handle_metakanban_operation_command] Error creating LLMTransaction for assistant response (backup). Error: {e}")
                pass

        # TOOL USAGE IDENTIFICATION
        tool_counter = 0

        context_messages.append(
            {
                "content": choice_message_content,
                "role": ChatRoles.ASSISTANT,
            }
        )

        while (len(find_tool_call_from_json(choice_message_content)) > 0 and
               (tool_counter < METAKANBAN_TOOL_COMMAND_MAXIMUM_ATTEMPTS)):

            tool_counter += 1
            tool_requests_dicts = find_tool_call_from_json(choice_message_content)

            if len(tool_requests_dicts) > 0:
                for tool_req_dict in tool_requests_dicts:

                    defined_tool_descriptor = tool_req_dict.get("tool", "")
                    output_tool_call = f"""
                            Tool Response: {defined_tool_descriptor}

                            '''
                        """

                    error = verify_metakanban_command_query_content(
                        content=tool_req_dict
                    )

                    if error:
                        logger.error(error)
                        return error, None, None, None

                    output_tool_call = self._handle_tool_metakanban_query(
                        tool_usage_dict=tool_req_dict,
                        output_tool_call=output_tool_call
                    )

                    output_tool_call += """
                            '''
                        """

                    context_messages.append(
                        {
                            "content": output_tool_call,
                            "role": ChatRoles.SYSTEM,
                        }
                    )

            try:

                llm_response = self.c.chat.completions.create(
                    model=self.llm_model.model_name,
                    messages=context_messages,
                    # temperature=float(self.llm_model.temperature),
                    # frequency_penalty=float(self.llm_model.frequency_penalty),
                    # presence_penalty=float(self.llm_model.presence_penalty),
                    # max_tokens=int(self.llm_model.maximum_tokens),
                    # top_p=float(self.llm_model.top_p)
                )

                choices = llm_response.choices
                first_choice = choices[0]

                choice_message = first_choice.message
                choice_message_content = choice_message.content

                logger.info(f"[handle_metakanban_operation_command] Generated AI response.")

                try:
                    tx = LLMTransaction.objects.create(
                        organization=self.board.project.organization,
                        model=self.llm_model,
                        responsible_user=self.board.created_by_user,
                        responsible_assistant=None,
                        encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                        transaction_context_content=str(choice_message_content),
                        transaction_type=ChatRoles.ASSISTANT,
                        transaction_source=LLMTransactionSourcesTypesNames.METAKANBAN,
                        llm_token_type=LLMTokenTypesNames.OUTPUT,
                    )

                    logger.info(
                        f"[handle_metakanban_operation_command] Created LLMTransaction for assistant response.")

                except Exception as e:
                    logger.error(
                        f"[handle_metakanban_operation_command] Error creating LLMTransaction for assistant response. Error: {e}")
                    pass

            except Exception as e:
                logger.error(
                    f"[handle_metakanban_operation_command] Error executing MetaKanban command: {query}. Error: {e}")
                error = f"[handle_metakanban_operation_command] Error executing MetaKanban command: {query}. Error: {e}"

                return output, error

        if tool_counter == METAKANBAN_TOOL_COMMAND_MAXIMUM_ATTEMPTS:
            error = (
                f"[handle_metakanban_operation_command] Error executing MetaKanban command: {query}. Error: Maximum tool call attempts "
                f"reached.")

            logger.error(error)

            return output, error

        try:

            tx = LLMTransaction(
                organization=self.board.project.organization,
                model=self.llm_model,
                responsible_user=self.board.created_by_user,
                responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.METAKANBAN,
                is_tool_cost=True,
                llm_token_type=LLMTokenTypesNames.OUTPUT,
            )

            tx.save()

            logger.info(f"[handle_ai_command] Created LLMTransaction for MetaKanban Management by AI.")

        except Exception as e:
            logger.error(
                f"[handle_ai_command] Error creating LLMTransaction for MetaKanban Management by AI. Error: {e}")
            pass

        output = choice_message_content

        return output, error

    def _handle_tool_metakanban_query(
        self,
        tool_usage_dict,
        output_tool_call
    ):

        action_type = tool_usage_dict.get("parameters").get("action_type")
        action_content = tool_usage_dict.get("parameters").get("action_content")

        output, error = run_metakanban_command_query(
            board_id=self.board.id,
            action_type=action_type,
            action_content=action_content
        )

        output_str = f"""
           - Action Request for This Tool Execution:
                '''
                {tool_usage_dict}
            '''
           - Success Status / Created Element ID: {output}
           - Error Log (if there is any): {error}
           - Tool Use Timestamp: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}
        """

        output_tool_call += output_str

        logger.info(f"[handle_metakanban_operation_command] Tool Response: {output_tool_call}")

        return output_tool_call
