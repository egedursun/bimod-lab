#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: execute_scheduled_job_tasks.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:45
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

from celery import shared_task
from django.utils import timezone

from apps.core.generative_ai.utils import (
    GPT_DEFAULT_ENCODING_ENGINE,
    ChatRoles
)

from apps.core.internal_cost_manager.costs_map import InternalServiceCosts

from apps.core.generative_ai.generative_ai_decode_manager import (
    GenerativeAIDecodeController
)

from apps.core.orchestration.orchestration_executor import (
    OrchestrationExecutor
)

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames
)

from apps.llm_transaction.models import LLMTransaction

from apps.multimodal_chat.models import (
    MultimodalChat,
    MultimodalChatMessage, MultimodalLeanChat, MultimodalLeanChatMessage
)

from apps.multimodal_chat.utils import (
    SourcesForMultimodalChatsNames
)

from apps.orchestrations.models import (
    OrchestrationQuery,
    OrchestrationQueryLog
)

from apps.orchestrations.utils import (
    OrchestrationQueryLogTypesNames
)

logger = logging.getLogger(__name__)


@shared_task
def execute_scheduled_job(scheduled_job_id):
    from apps.mm_scheduled_jobs.tasks import (
        generate_scheduled_job_chat_name
    )

    from apps.mm_scheduled_jobs.models import (
        ScheduledJob,
        ScheduledJobInstance
    )

    from apps.mm_scheduled_jobs.utils import (
        ScheduledJobInstanceStatusesNames
    )

    from apps.core.generative_ai.utils import (
        GPT_DEFAULT_ENCODING_ENGINE
    )

    from apps.core.generative_ai.utils import ChatRoles

    job = ScheduledJob.objects.get(id=scheduled_job_id)
    if job.current_run_count > job.maximum_runs:
        job.delete()
        return

    new_instance = ScheduledJobInstance.objects.create(
        scheduled_job=job,
        status=ScheduledJobInstanceStatusesNames.PENDING
    )

    job.scheduled_job_instances.add(new_instance)
    job.save()
    logger.info(f"Executing Scheduled Job: {job.id}")

    try:
        job.current_run_count += 1
        job.save()

        new_instance.execution_index = job.current_run_count
        new_instance.save()

        chat = MultimodalChat.objects.create(
            user=job.created_by_user,
            organization=job.assistant.organization,
            assistant=job.assistant,
            chat_name=generate_scheduled_job_chat_name(job.name),
            created_by_user=job.created_by_user,
            chat_source=SourcesForMultimodalChatsNames.SCHEDULED,
        )

        new_instance.status = ScheduledJobInstanceStatusesNames.BUILDING
        new_instance.save()

        instruction_feed = f"""
            **WARNING: This is an AUTO-GENERATED user message.**
            - If you see this message, it means that this message is sent to you by the system, within the context
            of a scheduled automatic job execution. Please do not expect an answer to this message and treat this
            as a STRICT ORDER given to you by the user, for you to perform. DO YOUR BEST to accomplish the described
            task based on your available tools and capabilities.

            ---

            **TASK INFORMATION:**
            [Scheduled Job Name]: {job.name}  (The user-defined name of the scheduled job)
            [Scheduled Job Description]: {job.task_description} (The user-defined instructions to explain TO YOU
                what the job is about and what you need to accomplish within the context of this job. Make sure
                you read and understand the descriptions here to help the user THE BEST you can.)
            [Scheduled Job Step Guide]: (The user-defined step-by-step guide to help you understand the process of
                the job and what you need to do to accomplish the job. Make sure you read and understand the step
                guide to help the user THE BEST you can.)
            '''
            {job.step_guide}
            '''
            [How often this task is triggered (Celery Config)]:
            '''
            *Celery / Periodic Task Object*
            [Minute]: {job.minute}
            [Hour]: {job.hour}
            [Day of Week]: {job.day_of_week}
            [Day of Month]: {job.day_of_month}
            [Month of Year]: {job.month_of_year}
            '''

            [What is the life expectancy of this task]:
            '''
            [Current Run Index]: {job.current_run_count}
            [Maximum Runs]: {job.maximum_runs}
            '''
            - If the current run index exceeds the maximum runs, the scheduled job will be deleted automatically by
            the system. However, if you see this message, it means that the task still exists, and you must try to
            execute whatever ordered to you by the user within the context of this job.

            **IMPORTANT NOTES**
            - DO NOT ASK questions, since the user will not be able to answer you, as this is an automatic task.
            - If you are NOT 100% clear on what you need to accomplish, still try to do something if you think it
            wouldn't be a very harmful operation. However, if a potentially harmful operation (such as a database
            deletion operation) is ordered clearly by the user, DO NOT ASK FOR CONFIRMATION and perform the task.
            - IN FACT, NEVER ASK FOR CONFIRMATION, nor any other details since there is no way for the user to answer
            you since this message is completely automated and triggered by a Celery Cron Job.

            ---

            NOW; PLEASE GO AHEAD and EXECUTE the task according to the instructions provided to you

            ---.
        """

        instruction_feed_message = MultimodalChatMessage.objects.create(
            multimodal_chat=chat,
            sender_type='USER',
            message_text_content=instruction_feed
        )

        new_instance.status = ScheduledJobInstanceStatusesNames.INITIALIZING_ASSISTANT
        new_instance.save()

        llm_client = GenerativeAIDecodeController.get(
            assistant=chat.assistant,
            multimodal_chat=chat
        )

        new_instance.status = ScheduledJobInstanceStatusesNames.GENERATING
        new_instance.save()

        response_text = llm_client.respond(
            latest_message=instruction_feed_message
        )

        new_instance.status = ScheduledJobInstanceStatusesNames.SAVING_LOGS
        new_instance.save()

        new_instance.logs = response_text
        new_instance.save()

        new_instance.status = ScheduledJobInstanceStatusesNames.CLEANING_UP
        new_instance.save()

        chat.delete()

        new_instance.status = ScheduledJobInstanceStatusesNames.COMPLETED
        new_instance.ended_at = timezone.now()

        new_instance.save()

        transaction = LLMTransaction(
            organization=job.assistant.organization,
            model=job.assistant.llm_model,
            responsible_user=None,
            responsible_assistant=job.assistant,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.ScheduledJobExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.SCHEDULED_JOB_EXECUTION,
            is_tool_cost=True
        )

        transaction.save()
        logger.info(f"Scheduled Job: {job.id} was executed successfully.")

    except Exception as e:
        logger.error(f"Error while executing the scheduled job: {e}")

        new_instance.status = ScheduledJobInstanceStatusesNames.FAILED
        new_instance.save()


@shared_task
def execute_orchestration_scheduled_job(scheduled_job_id):
    from apps.mm_scheduled_jobs.models import (
        OrchestrationScheduledJob,
        OrchestrationScheduledJobInstance
    )

    from apps.mm_scheduled_jobs.utils import (
        ScheduledJobInstanceStatusesNames
    )

    job: OrchestrationScheduledJob = OrchestrationScheduledJob.objects.get(
        id=scheduled_job_id
    )

    if job.current_run_count > job.maximum_runs:
        job.delete()
        return

    new_instance: OrchestrationScheduledJobInstance = OrchestrationScheduledJobInstance.objects.create(
        scheduled_job=job,
        status=ScheduledJobInstanceStatusesNames.PENDING
    )

    job.scheduled_job_instances.add(new_instance)
    job.save()

    logger.info(f"Executing Orchestration Scheduled Job: {job.id}")

    try:
        job.current_run_count += 1
        job.save()

        new_instance.execution_index = job.current_run_count
        new_instance.save()

        new_instance.status = ScheduledJobInstanceStatusesNames.BUILDING
        new_instance.save()

        instruction_feed = f"""
            **WARNING: This is an AUTO-GENERATED user message.**
            - If you see this message, it means that this message is sent to you by the system, within the context
            of a scheduled automatic job execution. Please do not expect an answer to this message and treat this
            as a STRICT ORDER given to you by the user, for you to perform. DO YOUR BEST to accomplish the described
            task based on your available tools and capabilities.

            ---

            **TASK INFORMATION:**
            [Scheduled Job Name]: {job.name}  (The user-defined name of the scheduled job)
            [Scheduled Job Description]: {job.task_description} (The user-defined instructions to explain TO YOU
                what the job is about and what you need to accomplish within the context of this job. Make sure
                you read and understand the descriptions here to help the user THE BEST you can.)
            [Scheduled Job Step Guide]: (The user-defined step-by-step guide to help you understand the process of
                the job and what you need to do to accomplish the job. Make sure you read and understand the step
                guide to help the user THE BEST you can.)
            '''
            {job.step_guide}
            '''
            [How often this task is triggered (Celery Config)]:
            '''
            *Celery / Periodic Task Object*
            [Minute]: {job.minute}
            [Hour]: {job.hour}
            [Day of Week]: {job.day_of_week}
            [Day of Month]: {job.day_of_month}
            [Month of Year]: {job.month_of_year}
            '''

            [What is the life expectancy of this task]:
            '''
            [Current Run Index]: {job.current_run_count}
            [Maximum Runs]: {job.maximum_runs}
            '''
            - If the current run index exceeds the maximum runs, the scheduled job will be deleted automatically by
            the system. However, if you see this message, it means that the task still exists, and you must try to
            execute whatever ordered to you by the user within the context of this job.

            **IMPORTANT NOTES**
            - DO NOT ASK questions, since the user will not be able to answer you, as this is an automatic task.
            - If you are NOT 100% clear on what you need to accomplish, still try to do something if you think it
            wouldn't be a very harmful operation. However, if a potentially harmful operation (such as a database
            deletion operation) is ordered clearly by the user, DO NOT ASK FOR CONFIRMATION and perform the task.
            - IN FACT, NEVER ASK FOR CONFIRMATION, nor any other details since there is no way for the user to answer
            you since this message is completely automated and triggered by a Celery Cron Job.

            ---

            NOW; PLEASE GO AHEAD and EXECUTE the task according to the instructions provided to you.

            ---
        """

        attached_images = []
        attached_files = []

        query: OrchestrationQuery = OrchestrationQuery.objects.create(
            maestro=new_instance.scheduled_job.maestro,
            query_text=instruction_feed,
            created_by_user=new_instance.scheduled_job.created_by_user,
            last_updated_by_user=new_instance.scheduled_job.created_by_user
        )

        query_text = query.query_text
        query_log = OrchestrationQueryLog.objects.create(
            orchestration_query=query,
            log_type=OrchestrationQueryLogTypesNames.USER,
            log_text_content=query_text + f"""
                                        -----
                                        **IMAGE URLS:**
                                        '''
                                        {attached_images}
                                        '''
                                        -----
                                        **FILE URLS:**
                                        '''
                                        {attached_files}
                                        '''
                                        -----
                                    """,
            log_file_contents=attached_files,
            log_image_contents=attached_images
        )

        query.logs.add(query_log)
        query.save()

        xc: OrchestrationExecutor = OrchestrationExecutor(
            maestro=new_instance.scheduled_job.maestro,
            query_chat=query
        )

        output = xc.execute_for_query()

        transaction = LLMTransaction(
            organization=job.maestro.organization,
            model=job.maestro.llm_model,
            responsible_user=None,
            responsible_assistant=job.maestro,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.ScheduledJobExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.SCHEDULED_JOB_EXECUTION,
            is_tool_cost=True
        )
        transaction.save()

        logger.info("Orchestration Scheduled Job Output: \n" + output)
        logger.info(f"Orchestration Scheduled Job: {job.id} was executed successfully.")

    except Exception as e:
        logger.error(f"Error while executing the orchestration scheduled job: {e}")
        new_instance.status = ScheduledJobInstanceStatusesNames.FAILED

        new_instance.save()


@shared_task
def execute_leanmod_scheduled_job(scheduled_job_id):
    from apps.mm_scheduled_jobs.tasks import (
        generate_scheduled_job_chat_name
    )

    from apps.mm_scheduled_jobs.models import (
        LeanModScheduledJob,
        LeanModScheduledJobInstance
    )

    from apps.mm_scheduled_jobs.utils import (
        ScheduledJobInstanceStatusesNames
    )

    from apps.core.generative_ai.utils import (
        GPT_DEFAULT_ENCODING_ENGINE
    )

    from apps.core.generative_ai.utils import ChatRoles

    job: LeanModScheduledJob = LeanModScheduledJob.objects.get(
        id=scheduled_job_id
    )

    if job.current_run_count > job.maximum_runs:
        job.delete()
        return

    new_instance: LeanModScheduledJobInstance = LeanModScheduledJobInstance.objects.create(
        scheduled_job=job,
        status=ScheduledJobInstanceStatusesNames.PENDING
    )

    job.scheduled_job_instances.add(new_instance)
    job.save()
    logger.info(f"Executing LeanMod Scheduled Job: {job.id}")
    try:
        job.current_run_count += 1
        job.save()

        new_instance.execution_index = job.current_run_count
        new_instance.save()

        chat = MultimodalLeanChat.objects.create(
            user=job.created_by_user,
            organization=job.leanmod.organization,
            lean_assistant=job.leanmod,
            chat_name=generate_scheduled_job_chat_name(job.name),
            created_by_user=job.created_by_user,
            chat_source=SourcesForMultimodalChatsNames.SCHEDULED,
        )

        new_instance.status = ScheduledJobInstanceStatusesNames.BUILDING

        new_instance.save()

        instruction_feed = f"""
            **WARNING: This is an AUTO-GENERATED user message.**
            - If you see this message, it means that this message is sent to you by the system, within the context
            of a scheduled automatic job execution. Please do not expect an answer to this message and treat this
            as a STRICT ORDER given to you by the user, for you to perform. DO YOUR BEST to accomplish the described
            task based on your available tools and capabilities.

            ---

            **TASK INFORMATION:**
            [Scheduled Job Name]: {job.name}  (The user-defined name of the scheduled job)
            [Scheduled Job Description]: {job.task_description} (The user-defined instructions to explain TO YOU
                what the job is about and what you need to accomplish within the context of this job. Make sure
                you read and understand the descriptions here to help the user THE BEST you can.)
            [Scheduled Job Step Guide]: (The user-defined step-by-step guide to help you understand the process of
                the job and what you need to do to accomplish the job. Make sure you read and understand the step
                guide to help the user THE BEST you can.)
            '''
            {job.step_guide}
            '''
            [How often this task is triggered (Celery Config)]:
            '''
            *Celery / Periodic Task Object*
            [Minute]: {job.minute}
            [Hour]: {job.hour}
            [Day of Week]: {job.day_of_week}
            [Day of Month]: {job.day_of_month}
            [Month of Year]: {job.month_of_year}
            '''

            [What is the life expectancy of this task]:
            '''
            [Current Run Index]: {job.current_run_count}
            [Maximum Runs]: {job.maximum_runs}
            '''
            - If the current run index exceeds the maximum runs, the scheduled job will be deleted automatically by
            the system. However, if you see this message, it means that the task still exists, and you must try to
            execute whatever ordered to you by the user within the context of this job.

            **IMPORTANT NOTES**
            - DO NOT ASK questions, since the user will not be able to answer you, as this is an automatic task.
            - If you are NOT 100% clear on what you need to accomplish, still try to do something if you think it
            wouldn't be a very harmful operation. However, if a potentially harmful operation (such as a database
            deletion operation) is ordered clearly by the user, DO NOT ASK FOR CONFIRMATION and perform the task.
            - IN FACT, NEVER ASK FOR CONFIRMATION, nor any other details since there is no way for the user to answer
            you since this message is completely automated and triggered by a Celery Cron Job.

            ---

            NOW; PLEASE GO AHEAD and EXECUTE the task according to the instructions provided to you.

            ---.
        """

        instruction_feed_message = MultimodalLeanChatMessage.objects.create(
            multimodal_lean_chat=chat,
            sender_type='USER',
            message_text_content=instruction_feed
        )

        new_instance.status = ScheduledJobInstanceStatusesNames.INITIALIZING_ASSISTANT
        new_instance.save()

        llm_client = GenerativeAIDecodeController.get_lean(
            user=job.created_by_user,
            assistant=chat.assistant,
            multimodal_chat=chat
        )

        new_instance.status = ScheduledJobInstanceStatusesNames.GENERATING
        new_instance.save()

        response_text = llm_client.respond(
            latest_message=instruction_feed_message
        )

        new_instance.status = ScheduledJobInstanceStatusesNames.SAVING_LOGS
        new_instance.save()

        new_instance.logs = response_text
        new_instance.save()

        new_instance.status = ScheduledJobInstanceStatusesNames.CLEANING_UP
        new_instance.save()

        chat.delete()

        new_instance.status = ScheduledJobInstanceStatusesNames.COMPLETED
        new_instance.ended_at = timezone.now()
        new_instance.save()

        transaction = LLMTransaction(
            organization=job.leanmod.organization,
            model=job.leanmod.llm_model,
            responsible_user=None,
            responsible_assistant=job.leanmod,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            llm_cost=InternalServiceCosts.ScheduledJobExecutor.COST,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.SCHEDULED_JOB_EXECUTION,
            is_tool_cost=True
        )
        transaction.save()

        logger.info(f"LeanMod Scheduled Job: {job.id} was executed successfully.")

    except Exception as e:
        logger.error(f"Error while executing the LeanMod scheduled job: {e}")

        new_instance.status = ScheduledJobInstanceStatusesNames.FAILED
        new_instance.save()
