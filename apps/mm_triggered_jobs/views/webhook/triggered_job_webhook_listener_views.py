#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: triggered_job_webhook_listener_views.py
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


import json
import logging

from django.http import JsonResponse
from django.utils import timezone

from django.utils.decorators import (
    method_decorator
)

from django.views import View

from django.views.decorators.csrf import (
    csrf_exempt
)

from apps.core.generative_ai.generative_ai_decode_manager import (
    GenerativeAIDecodeController
)

from apps.assistants.models import Assistant

from apps.llm_transaction.models import (
    LLMTransaction
)

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames,
    LLMTokenTypesNames
)

from apps.mm_triggered_jobs.models import (
    TriggeredJob,
    TriggeredJobInstance
)

from apps.mm_triggered_jobs.utils import (
    TriggeredJobInstanceStatusesNames,
    generate_triggered_job_chat_name
)

from apps.multimodal_chat.models import (
    MultimodalChat,
    MultimodalChatMessage
)

from apps.multimodal_chat.utils import (
    SourcesForMultimodalChatsNames
)

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class TriggeredJobWebhookListenerView(View):
    def get(
        self,
        request,
        assistant_id,
        triggered_job_id
    ):
        _, _ = assistant_id, triggered_job_id

        logger.error('Method GET is not allowed')

        return JsonResponse(
            {
                'status': 'error',
                'message': 'Method GET is not allowed'
            },
            status=405
        )

    def post(
        self,
        request,
        assistant_id,
        triggered_job_id
    ):
        try:
            payload = json.loads(request.body)

            try:
                job = TriggeredJob.objects.get(
                    id=triggered_job_id
                )

                assistant = job.trigger_assistant

                check_assistant = Assistant.objects.get(
                    id=assistant_id
                )

                if assistant != check_assistant:
                    logger.error(f"Assistant verification failed for Triggered Job: {job.id}")

                    return JsonResponse(
                        {
                            'status': 'error',
                            'message': 'Assistant verification failed'
                        },
                        status=400
                    )

            except TriggeredJob.DoesNotExist:
                logger.error(f"Triggered Job could not been found: {triggered_job_id}")

                return JsonResponse(
                    {
                        'status': 'error',
                        'message': 'Triggered Job could not been found'
                    },
                    status=404
                )

            except Assistant.DoesNotExist:
                logger.error(f"Assistant could not been found: {assistant_id}")

                return JsonResponse(
                    {
                        'status': 'error',
                        'message': 'Assistant could not been found'
                    },
                    status=404
                )

            if job.current_run_count > job.maximum_runs:
                job.delete()

                logger.info(f"Maximum runs reached for Triggered Job: {job.id}")

                return JsonResponse(
                    {
                        'status': 'error',
                        'message': 'Maximum runs reached for the triggered job'
                    },
                    status=400
                )

            new_instance = TriggeredJobInstance.objects.create(
                triggered_job=job,
                status=TriggeredJobInstanceStatusesNames.PENDING,
                webhook_payload=payload
            )

            job.triggered_job_instances.add(
                new_instance
            )

            job.save()

            job.current_run_count += 1

            job.save()

            new_instance.execution_index = job.current_run_count

            new_instance.save()

            self.handle_triggered_job(
                job=job,
                instance=new_instance
            )

            logger.info(f"Webhook payload received for Triggered Job: {job.id}")

            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Webhook payload received successfully',
                    'data': {
                        'assistant_id': assistant_id,
                        'triggered_job_id': triggered_job_id,
                        'payload': payload
                    }
                },
                status=200
            )

        except json.JSONDecodeError:
            logger.error('Invalid JSON object')

            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Invalid JSON object'
                },
                status=400
            )

    @staticmethod
    def handle_triggered_job(job, instance):
        from apps.core.generative_ai.utils import (
            GPT_DEFAULT_ENCODING_ENGINE
        )

        from apps.core.generative_ai.utils import ChatRoles

        job: TriggeredJob

        try:
            chat = MultimodalChat.objects.create(
                user=job.created_by_user,
                organization=job.trigger_assistant.organization,
                assistant=job.trigger_assistant,
                chat_name=generate_triggered_job_chat_name(job.name),
                created_by_user=job.created_by_user,
                chat_source=SourcesForMultimodalChatsNames.TRIGGERED
            )

            instance.status = TriggeredJobInstanceStatusesNames.BUILDING

            instance.save()

            logger.info(f"Chat created for Triggered Job: {job.id}")

            instruction_feed = f"""
                **WARNING: This is an AUTO-GENERATED user message.**
                - If you see this message, it means that this message is sent to you by the system, within the context
                of a webhook-triggered automatic job execution. Please do not expect an answer to this message and treat
                this as a STRICT ORDER given to you by the user, for you to perform. DO YOUR BEST to accomplish the
                described task based on your available tools and capabilities.

                ---

                **TASK INFORMATION:**
                [Triggered Job Name]: {job.name} (The user-defined name of the triggered job)
                [Triggered Job Description]: {job.task_description} (The user-defined instructions to explain TO YOU
                    what the job is about and what you need to accomplish within the context of the job. Make sure
                    you read and understand the descriptions here to help the user THE BEST you can.)
                [Triggered Job Step Guide]: (The user-defined step-by-step guide to help you understand the process of
                    the job and what you need to do to accomplish the job. Make sure you read and understand the step
                    guide to help the user THE BEST you can.)
                '''
                {job.step_guide}
                '''
                [When this task is triggered?]: {job.event_type}
                [Source of the Webhook Trigger]: {job.trigger_source}
                [Webhook Payload]:
                '''
                {json.dumps(instance.webhook_payload, indent=4)}
                '''

                [What is the life expectancy of this task?]:
                '''
                [Current Run Index]: {job.current_run_count}
                [Maximum Runs]: {job.maximum_runs}
                '''
                - If the current run index exceeds the maximum runs, the triggered job will be deleted automatically by
                the system. However, if you see this message, it means that the task still exists, and you must try to
                execute whatever ordered to you by the user within the context of this job.

                **IMPORTANT NOTES**
                - DO NOT ASK questions, since the user will not be able to answer you, as this is an automatic task.
                - If you are NOT 100% clear on what you need to accomplish, still try to do something if you think it
                wouldn't be a very harmful operation. However, if a potentially harmful operation (such as a database
                deletion operation) is ordered clearly by the user, DO NOT ASK FOR CONFIRMATION and perform the task.
                - IN FACT, NEVER ASK FOR CONFIRMATION, nor any other details since there is no way for the user to answer
                you since this message is completely automated and triggered by a Webhook.

                ---

                NOW; PLEASE GO AHEAD and EXECUTE the task according to the instructions provided to you.

                ---
                """
            instruction_feed_message = MultimodalChatMessage.objects.create(
                multimodal_chat=chat,
                sender_type='USER',
                message_text_content=instruction_feed
            )

            instance.status = TriggeredJobInstanceStatusesNames.INITIALIZING_ASSISTANT
            instance.save()

            llm_client = GenerativeAIDecodeController.get(
                assistant=chat.assistant,
                multimodal_chat=chat
            )

            instance.status = TriggeredJobInstanceStatusesNames.GENERATING
            instance.save()

            response_text = llm_client.respond_stream(
                latest_message=instruction_feed_message
            )

            instance.status = TriggeredJobInstanceStatusesNames.SAVING_LOGS

            instance.save()

            instance.logs = response_text

            instance.save()

            instance.status = TriggeredJobInstanceStatusesNames.CLEANING_UP

            instance.save()

            chat.delete()

            instance.status = TriggeredJobInstanceStatusesNames.COMPLETED
            instance.ended_at = timezone.now()

            instance.save()

            transaction = LLMTransaction(
                organization=job.trigger_assistant.organization,
                model=job.trigger_assistant.llm_model,
                responsible_user=None,
                responsible_assistant=job.trigger_assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.TRIGGER_JOB_EXECUTION,
                is_tool_cost=True,
                llm_token_type=LLMTokenTypesNames.OUTPUT,
            )

            transaction.save()

            logger.info(f"Triggered Job completed successfully: {job.id}")

        except Exception as e:
            instance.status = TriggeredJobInstanceStatusesNames.FAILED

            instance.save()

            logger.error(f"Triggered Job failed: {job.id} - {str(e)}")
