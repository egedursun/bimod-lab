#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metatempo_execution_handler.py
#  Last Modified: 2024-10-28 19:38:44
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 19:38:45
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import base64
import json
import logging
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.utils import timezone

from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE, ChatRoles
from apps.core.internal_cost_manager.costs_map import InternalServiceCosts

from apps.core.metatempo.builders import (
    build_log_snapshot_interpretation_prompt,
    build_daily_logs_interpretation_prompt,
    build_overall_interpretation_prompt,
    build_user_loq_question_interpretation_prompt
)

from apps.core.metatempo.utils import (
    MAXIMUM_OVERALL_LOG_RETRIEVAL_INTERVAL_DAYS,
    find_tool_call_from_json_single
)

from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames

from apps.metatempo.models import (
    MetaTempoConnection,
    MetaTempoMemberLog,
    MetaTempoMemberLogDaily,
    MetaTempoProjectOverallLog
)

from apps.metatempo.utils import MetaTempoOverallLogIntervalsNames

logger = logging.getLogger(__name__)


class MetaTempoExecutionActionTypesNames:
    INTERPRET_AND_SAVE_LOG_SNAPSHOT = "interpret_and_save_log_snapshot"
    INTERPRET_AND_SAVE_DAILY_LOGS = "interpret_and_save_daily_logs"
    INTERPRET_OVERALL_LOGS = "interpret_overall_logs"
    ASK_LOGS_QUESTION = "ask_logs_question"

    @staticmethod
    def as_list():
        return [
            MetaTempoExecutionActionTypesNames.INTERPRET_AND_SAVE_LOG_SNAPSHOT,
            MetaTempoExecutionActionTypesNames.INTERPRET_AND_SAVE_DAILY_LOGS,
            MetaTempoExecutionActionTypesNames.INTERPRET_OVERALL_LOGS,
            MetaTempoExecutionActionTypesNames.ASK_LOGS_QUESTION
        ]


class MetaTempoExecutionManager:

    def __init__(
        self,
        metatempo_connection_id: int
    ):
        from apps.core.generative_ai.gpt_openai_manager import OpenAIGPTClientManager
        self.metatempo_connection = MetaTempoConnection.objects.get(
            id=metatempo_connection_id
        )
        self.metakanban_board = self.metatempo_connection.board
        self.llm_model = self.metakanban_board.llm_model
        self.c = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.llm_model
        )

    def _consult_ai(
        self,
        action_type: str,
        interpretation_query: str = None,
        log_screenshot_data=None,
        batched_logs: list = None
    ):

        context_messages_history = []

        if action_type == MetaTempoExecutionActionTypesNames.INTERPRET_AND_SAVE_LOG_SNAPSHOT:

            action_specific_system_prompt = build_log_snapshot_interpretation_prompt(
                connection=self.metatempo_connection
            )
            context_messages_history.append(
                {
                    "role": "system",
                    "content": action_specific_system_prompt
                }
            )

            try:
                tx = LLMTransaction.objects.create(
                    organization=self.metatempo_connection.board.project.organization,
                    model=self.llm_model,
                    responsible_user=self.metatempo_connection.board.created_by_user,
                    responsible_assistant=None,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=str(action_specific_system_prompt),
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.SYSTEM,
                    transaction_source=LLMTransactionSourcesTypesNames.METATEMPO
                )
                logger.info(f"[handle_metatempo_operation_command] Created LLMTransaction for system prompt.")

            except Exception as e:
                logger.error(
                    f"[handle_metatempo_operation_command] Error creating LLMTransaction for system prompt. Error: {e}")
                pass

            if not log_screenshot_data:
                logger.error("No log screenshot data provided for interpretation.")
                return None, "No log screenshot data provided for interpretation."

            log_screenshot_base_64 = base64.b64encode(log_screenshot_data).decode("utf-8")
            formatted_uri = f"data:image/png;base64,{log_screenshot_base_64}"

            context_messages_history.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": interpretation_query
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": formatted_uri
                            }
                        }
                    ]
                }
            )

        elif action_type == MetaTempoExecutionActionTypesNames.INTERPRET_AND_SAVE_DAILY_LOGS:

            action_specific_system_prompt = build_daily_logs_interpretation_prompt(
                connection=self.metatempo_connection,
                batched_logs=batched_logs
            )

            try:
                tx = LLMTransaction.objects.create(
                    organization=self.metatempo_connection.board.project.organization,
                    model=self.llm_model,
                    responsible_user=self.metatempo_connection.board.created_by_user,
                    responsible_assistant=None,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=str(action_specific_system_prompt),
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.SYSTEM,
                    transaction_source=LLMTransactionSourcesTypesNames.METATEMPO
                )
                logger.info(f"[handle_metatempo_operation_command] Created LLMTransaction for system prompt.")

            except Exception as e:
                logger.error(
                    f"[handle_metatempo_operation_command] Error creating LLMTransaction for system prompt. Error: {e}")
                pass

            context_messages_history.append({"role": "system", "content": action_specific_system_prompt})

        elif action_type == MetaTempoExecutionActionTypesNames.INTERPRET_OVERALL_LOGS:

            action_specific_system_prompt = build_overall_interpretation_prompt(
                connection=self.metatempo_connection,
                batched_logs=batched_logs
            )

            try:
                tx = LLMTransaction.objects.create(
                    organization=self.metatempo_connection.board.project.organization,
                    model=self.llm_model,
                    responsible_user=self.metatempo_connection.board.created_by_user,
                    responsible_assistant=None,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=str(action_specific_system_prompt),
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.SYSTEM,
                    transaction_source=LLMTransactionSourcesTypesNames.METATEMPO
                )
                logger.info(f"[handle_metatempo_operation_command] Created LLMTransaction for system prompt.")

            except Exception as e:
                logger.error(
                    f"[handle_metatempo_operation_command] Error creating LLMTransaction for system prompt. Error: {e}")
                pass

            context_messages_history.append({"role": "system", "content": action_specific_system_prompt})

        elif action_type == MetaTempoExecutionActionTypesNames.ASK_LOGS_QUESTION:

            action_specific_system_prompt = build_user_loq_question_interpretation_prompt(
                connection=self.metatempo_connection,
                batched_logs=batched_logs
            )
            context_messages_history.append({
                "role": "system",
                "content": action_specific_system_prompt
            })

            try:
                tx = LLMTransaction.objects.create(
                    organization=self.metatempo_connection.board.project.organization,
                    model=self.llm_model,
                    responsible_user=self.metatempo_connection.board.created_by_user,
                    responsible_assistant=None,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=str(action_specific_system_prompt),
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.SYSTEM,
                    transaction_source=LLMTransactionSourcesTypesNames.METATEMPO
                )
                logger.info(f"[handle_metatempo_operation_command] Created LLMTransaction for system prompt.")

            except Exception as e:
                logger.error(
                    f"[handle_metatempo_operation_command] Error creating LLMTransaction for system prompt. Error: {e}")
                pass

            if not interpretation_query:
                logger.error("No interpretation query provided for logs question.")
                return None, "No interpretation query provided for logs question."

            try:
                tx = LLMTransaction.objects.create(
                    organization=self.metatempo_connection.board.project.organization,
                    model=self.llm_model,
                    responsible_user=self.metatempo_connection.created_by_user,
                    responsible_assistant=None,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    transaction_context_content=str(interpretation_query),
                    llm_cost=0,
                    internal_service_cost=0,
                    tax_cost=0,
                    total_cost=0,
                    total_billable_cost=0,
                    transaction_type=ChatRoles.USER,
                    transaction_source=LLMTransactionSourcesTypesNames.METATEMPO
                )
                logger.info(f"[handle_metatempo_operation_command] Created LLMTransaction for user prompt.")

            except Exception as e:
                logger.error(
                    f"[handle_metatempo_operation_command] Error creating LLMTransaction for user prompt. Error: {e}")
                pass

            context_messages_history.append({"role": "user", "content": interpretation_query})

        else:
            logger.error("Invalid action type provided: " + action_type)
            return None, "Invalid action type provided: " + action_type

        try:
            llm_output = self.c.chat.completions.create(
                model=self.llm_model.model_name,
                messages=context_messages_history,
                temperature=int(self.llm_model.temperature),
                max_tokens=int(self.llm_model.maximum_tokens)
            )
            logger.info(f"Retrieved image interpretation content.")

        except Exception as e:
            logger.error(f"Failed to retrieve LLM interpretation content: " + str(e))
            return None, "Failed to retrieve LLM interpretation content: " + str(e)

        try:
            choices = llm_output.choices
            first_choice = choices[0]
            choice_message = first_choice.message
            choice_message_content = choice_message.content
            final_response = choice_message_content
            logger.info(f"Processed LLM image interpretation content.")

        except Exception as e:
            logger.error(f"Failed to process LLM interpretation content: " + str(e))
            return None, "Failed to process LLM interpretation content: " + str(e)

        try:
            tx = LLMTransaction.objects.create(
                organization=self.metatempo_connection.board.project.organization,
                model=self.llm_model,
                responsible_user=self.metatempo_connection.board.created_by_user,
                responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_context_content=str(choice_message_content),
                llm_cost=0,
                internal_service_cost=0,
                tax_cost=0,
                total_cost=0,
                total_billable_cost=0,
                transaction_type=ChatRoles.ASSISTANT,
                transaction_source=LLMTransactionSourcesTypesNames.METATEMPO
            )
            logger.info(
                f"[handle_metatempo_operation_command] Created LLMTransaction for assistant response (primary).")

        except Exception as e:
            logger.error(
                f"[handle_metatempo_operation_command] Error creating LLMTransaction for assistant response (primary). Error: {e}")
            pass

        return final_response, None

    def interpret_and_save_log_snapshot(
        self,
        context_user: User,
        snapshot_metadata: dict,
        log_screenshot_data: str
    ):

        # Trigger: Via API Call (POST)
        response_json_string, error = self._consult_ai(
            action_type=MetaTempoExecutionActionTypesNames.INTERPRET_AND_SAVE_LOG_SNAPSHOT,
            interpretation_query=f"""
                ### **SNAPSHOT METADATA:**

                '''

                {snapshot_metadata}

                '''

                -----
            """, log_screenshot_data=log_screenshot_data)

        if error:
            return None, error

        try:
            response_json = find_tool_call_from_json_single(response_json_string)

        except Exception as e:
            logger.error(f"Failed to parse response JSON of the AI response: " + str(e))
            return None, "Failed to parse response JSON of the AI response: " + str(e)

        activity_summary = response_json.get("activity_summary", None)
        activity_tags = response_json.get("activity_tags", None)
        work_intensity = response_json.get("work_intensity", None)
        application_usage_stats = response_json.get("application_usage_stats", None)

        try:
            log_entry = MetaTempoMemberLog.objects.create(
                identifier_uuid=snapshot_metadata.get("identifier_uuid"),
                metatempo_connection=self.metatempo_connection,
                user=context_user,
                activity_summary=activity_summary,
                activity_tags=activity_tags,
                work_intensity=work_intensity,
                application_usage_stats=application_usage_stats,
                timestamp=snapshot_metadata.get("timestamp")
            )
            log_entry.screenshot_image.save('screenshot.png', ContentFile(log_screenshot_data))
            log_entry.save()

        except Exception as e:
            logger.error(f"Failed to save MetaTempo member log: " + str(e))
            return json.dumps(response_json), "Failed to save MetaTempo member log: " + str(e)

        return json.dumps(response_json), error

    def interpret_and_save_daily_logs_batch(self, users: list):
        # Trigger: Via Automated Cron Job (LAST 24 HOURS)

        log_outputs, error = [], None
        try:
            for user in users:

                user: User
                timestamp_minus_24_hours = timezone.now() - timedelta(hours=24)

                log_records = MetaTempoMemberLog.objects.filter(
                    user=user,
                    timestamp__gte=timestamp_minus_24_hours
                )
                log_outputs, error = self._interpret_and_save_daily_logs(
                    context_user=user,
                    log_records=log_records
                )

                if error:
                    logger.error(f"Failed to interpret and save daily logs [ITEM] for user: {user.username}")
                    log_outputs.append("ERROR: Corrupted item.")

                try:
                    tx = LLMTransaction(
                        organization=self.metatempo_connection.board.project.organization,
                        model=self.metatempo_connection.board.llm_model,
                        responsible_user=self.metatempo_connection.board.created_by_user,
                        responsible_assistant=None,
                        encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                        llm_cost=InternalServiceCosts.MetaTempo.COST,
                        transaction_type=ChatRoles.SYSTEM,
                        transaction_source=LLMTransactionSourcesTypesNames.METATEMPO,
                        is_tool_cost=True
                    )
                    tx.save()
                    logger.info(
                        f"[interpret_and_save_daily_logs_batch] Created LLMTransaction for MetaTempo [BATCH] daily Log item.")

                except Exception as e:
                    logger.error(
                        f"[interpret_and_save_daily_logs_batch] Error creating LLMTransaction for MetaTempo Agent [BATCH] daily Log item. Error: {e}")
                    pass

        except Exception as e:
            error = "Failed to interpret and save daily logs [BATCH]: " + str(e)
            logger.error(error)
            return None, error

        return log_outputs, error

    def _interpret_and_save_daily_logs(
        self,
        context_user: User,
        log_records: list
    ):

        response_json_string, error = self._consult_ai(
            action_type=MetaTempoExecutionActionTypesNames.INTERPRET_AND_SAVE_DAILY_LOGS,
            batched_logs=log_records
        )

        if error:
            return None, error

        try:
            response_json = find_tool_call_from_json_single(response_json_string)

        except Exception as e:
            logger.error(f"Failed to parse response JSON of the AI response: " + str(e))
            return None, "Failed to parse response JSON of the AI response: " + str(e)

        daily_activity_summary = response_json.get("daily_activity_summary", None)
        key_tasks = response_json.get("key_tasks", None)
        overall_work_intensity = response_json.get("overall_work_intensity", None)
        application_usage_stats = response_json.get("application_usage_stats", None)

        try:
            log_daily_entry = MetaTempoMemberLogDaily.objects.create(
                metatempo_connection=self.metatempo_connection,
                user=context_user,
                daily_activity_summary=daily_activity_summary,
                key_tasks=key_tasks,
                overall_work_intensity=overall_work_intensity,
                application_usage_stats=application_usage_stats
            )

            log_daily_entry.logs.set(log_records)
            log_daily_entry.save()

        except Exception as e:
            logger.error(f"Failed to save MetaTempo daily log: " + str(e))
            return json.dumps(response_json), "Failed to save MetaTempo daily log: " + str(e)

        return json.dumps(response_json), error

    def interpret_overall_logs(self):
        # Trigger (1): Via Automated Cron Job
        # Trigger (2): Manual Triggering via Web Application (Detail MetaTempo Connection Page)

        delta_value_hours = 0
        recording_interval = self.metatempo_connection.overall_log_intervals
        if recording_interval == MetaTempoOverallLogIntervalsNames.DAILY:
            delta_value_hours = 24 * 1
        elif recording_interval == MetaTempoOverallLogIntervalsNames.BI_DAILY:
            delta_value_hours = 24 * 2
        elif recording_interval == MetaTempoOverallLogIntervalsNames.WEEKLY:
            delta_value_hours = 24 * 7
        elif recording_interval == MetaTempoOverallLogIntervalsNames.BI_WEEKLY:
            delta_value_hours = 24 * 14
        elif recording_interval == MetaTempoOverallLogIntervalsNames.MONTHLY:
            delta_value_hours = 24 * 30

        timestamp_minus_interval = timezone.now() - timedelta(
            hours=delta_value_hours
        )

        log_records = MetaTempoMemberLogDaily.objects.filter(
            datestamp__gte=timestamp_minus_interval
        )

        response_json_string, error = self._consult_ai(
            action_type=MetaTempoExecutionActionTypesNames.INTERPRET_OVERALL_LOGS,
            batched_logs=log_records
        )

        if error:
            return None, error

        try:
            response_json = find_tool_call_from_json_single(response_json_string)

        except Exception as e:
            logger.error(f"Failed to parse response JSON of the AI response: " + str(e))
            return None, "Failed to parse response JSON of the AI response: " + str(e)

        overall_activity_summary = response_json.get("overall_activity_summary", None)
        overall_key_insights = response_json.get("overall_key_insights", None)
        overall_work_intensity = response_json.get("overall_work_intensity", None)
        overall_application_usage_stats = response_json.get("overall_application_usage_stats", None)

        try:
            log_overall_entry = MetaTempoProjectOverallLog.objects.create(
                metatempo_connection=self.metatempo_connection,
                overall_activity_summary=overall_activity_summary,
                overall_key_insights=overall_key_insights,
                overall_work_intensity=overall_work_intensity,
                overall_application_usage_stats=overall_application_usage_stats
            )
            log_overall_entry.save()

        except Exception as e:
            logger.error(f"Failed to save MetaTempo overall log: " + str(e))
            return json.dumps(response_json), "Failed to save MetaTempo overall log: " + str(e)

        return json.dumps(response_json), error

    def answer_logs_question(self, user_query: str):
        # Trigger (1): Via Web Application (AI Agent Page) (*connected to view*)

        overall_logs_maximum_delta = MAXIMUM_OVERALL_LOG_RETRIEVAL_INTERVAL_DAYS
        daily_logs_timestamp_minus_interval = timezone.now() - timedelta(days=overall_logs_maximum_delta)

        maximum_overall_logs = MetaTempoProjectOverallLog.objects.filter(
            metatempo_connection=self.metatempo_connection,
            datestamp__gte=daily_logs_timestamp_minus_interval
        )

        response_text, error = self._consult_ai(
            action_type=MetaTempoExecutionActionTypesNames.ASK_LOGS_QUESTION,
            interpretation_query=user_query,
            batched_logs=maximum_overall_logs
        )

        return response_text, error
