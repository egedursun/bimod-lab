import json
from uuid import uuid4

from celery import shared_task
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from slugify import slugify

from apps._services.llms.llm_decoder import InternalLLMClient
from apps.multimodal_chat.models import MultimodalChat, ChatSourcesNames, MultimodalChatMessage


class TriggerTypeChoicesNames:
    INTERVAL = 'interval'
    CHRONOLOGICAL = 'chronological'


def generate_scheduled_job_chat_name(scheduled_job_name):
    uuid_1 = str(uuid4())
    uuid_2 = str(uuid4())
    return f"{slugify(scheduled_job_name)} - {uuid_1} - {uuid_2}"


@shared_task
def execute_scheduled_job(scheduled_job_id):
    from apps.mm_scheduled_jobs.models import ScheduledJob, ScheduledJobInstance
    from apps.mm_scheduled_jobs.models import ScheduledJobInstanceStatusesNames

    # Logic to execute the scheduled job
    job = ScheduledJob.objects.get(id=scheduled_job_id)

    # [-1] Check if the execution count is more than the maximum runs, if so delete the ScheduledJob, and return
    if job.current_run_count > job.maximum_runs:
        job.delete()
        print(f"[Scheduled Job Executor]: Deleted the Scheduled Job {job.name} as it has reached the maximum runs.")
        return

    # [0] Create the instance
    new_instance = ScheduledJobInstance.objects.create(
        scheduled_job=job,
        status=ScheduledJobInstanceStatusesNames.PENDING)
    # add it to the job
    job.scheduled_job_instances.add(new_instance)
    job.save()

    try:

        # [1] Update the job run count
        job.current_run_count += 1
        job.save()
        new_instance.execution_index = job.current_run_count
        new_instance.save()

        # [2] Create a chat
        chat = MultimodalChat.objects.create(
            user=job.created_by_user,
            organization=job.assistant.organization,
            assistant=job.assistant,
            chat_name=generate_scheduled_job_chat_name(job.name),
            created_by_user=job.created_by_user,
            chat_source=ChatSourcesNames.SCHEDULED,
        )

        # [3] Set the status as building
        new_instance.status = ScheduledJobInstanceStatusesNames.BUILDING
        new_instance.save()

        # [4] Create the instruction prompt
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

        # [5] Create the instruction feed message
        instruction_feed_message = MultimodalChatMessage.objects.create(
            multimodal_chat=chat,
            sender_type='USER',
            message_text_content=instruction_feed
        )

        # [6] Set the status as initializing assistant
        new_instance.status = ScheduledJobInstanceStatusesNames.INITIALIZING_ASSISTANT
        new_instance.save()

        # [7] Initialize the assistant client
        llm_client = InternalLLMClient.get(assistant=chat.assistant, multimodal_chat=chat)

        # [8] Set the status as generating
        new_instance.status = ScheduledJobInstanceStatusesNames.GENERATING
        new_instance.save()

        # [9] Get the response
        response_text = llm_client.respond(latest_message=instruction_feed_message)

        # [10] Set the status as saving logs
        new_instance.status = ScheduledJobInstanceStatusesNames.SAVING_LOGS
        new_instance.save()

        # [11] Save the logs
        new_instance.logs = response_text
        new_instance.save()

        # [12] Set the status as cleaning up
        new_instance.status = ScheduledJobInstanceStatusesNames.CLEANING_UP
        new_instance.save()

        # [13] Delete the chat
        chat.delete()

        # [14] Set the status as completed
        new_instance.status = ScheduledJobInstanceStatusesNames.COMPLETED
        new_instance.ended_at = timezone.now()
        new_instance.save()

    except Exception as e:
        new_instance.status = ScheduledJobInstanceStatusesNames.FAILED
        new_instance.save()
        print("[Scheduled Job Executor Error]: ", e)


def add_periodic_task(scheduled_job):
    crontab_schedule, created = CrontabSchedule.objects.get_or_create(
        minute=scheduled_job.minute or '*',
        hour=scheduled_job.hour or '*',
        day_of_week=scheduled_job.day_of_week or '*',
        day_of_month=scheduled_job.day_of_month or '*',
        month_of_year=scheduled_job.month_of_year or '*'
    )
    PeriodicTask.objects.create(
        crontab=crontab_schedule,
        name=f'ScheduledJob-{scheduled_job.id}',
        task='apps.mm_scheduled_jobs.tasks.execute_scheduled_job',
        args=json.dumps([scheduled_job.id])
    )
