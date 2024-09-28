"""
This module provides views for managing and executing triggered jobs within the Bimod.io platform.

The views allow authenticated users to create, list, delete, and manage triggered jobs and their logs. Additionally, there is a webhook listener view that processes incoming webhook payloads to trigger specific jobs.
"""

import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from apps._services.config.costs_map import ToolCostsMap
from apps._services.llms.llm_decoder import InternalLLMClient
from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import TransactionSourcesNames
from apps.mm_triggered_jobs.forms import TriggeredJobForm
from apps.mm_triggered_jobs.models import TriggeredJob, TriggeredJobInstance, TriggeredJobInstanceStatusesNames
from apps.mm_triggered_jobs.utils import generate_triggered_job_chat_name
from apps.multimodal_chat.models import MultimodalChat, ChatSourcesNames, MultimodalChatMessage
from apps.user_permissions.models import UserPermission
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


@method_decorator(csrf_exempt, name='dispatch')
class TriggeredJobWebhookListenerView(View):
    """
    Handles incoming webhook requests for triggered jobs.

    This view listens for incoming webhook POST requests to trigger specific jobs associated with an assistant. It verifies the assistant and job, updates the job run count, processes the event, and manages the lifecycle of the job execution.

    Methods:
        get(self, request, assistant_id, triggered_job_id): Returns a 405 Method Not Allowed error for GET requests.
        post(self, request, assistant_id, triggered_job_id): Processes the incoming webhook payload and triggers the job.
        handle_triggered_job(job, instance): Static method to handle the execution of the triggered job.
    """

    def get(self, request, assistant_id, triggered_job_id):
        _, _ = assistant_id, triggered_job_id
        return JsonResponse({'status': 'error', 'message': 'Method GET is not allowed'}, status=405)

    def post(self, request, assistant_id, triggered_job_id):
        try:
            payload = json.loads(request.body)
            # Fetch the relevant assistant and triggered job
            try:
                job = TriggeredJob.objects.get(id=triggered_job_id)
                assistant = job.trigger_assistant
                check_assistant = Assistant.objects.get(id=assistant_id)
                if assistant != check_assistant:
                    return JsonResponse({'status': 'error', 'message': 'Assistant verification failed'}, status=400)
            except TriggeredJob.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Triggered Job could not been found'}, status=404)
            except Assistant.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Assistant could not been found'}, status=404)

            # [-1] Check if the execution count is more than the maximum runs, if so delete
            # the TriggeredJob, and return
            if job.current_run_count > job.maximum_runs:
                job.delete()
                print(f"[Triggered Job Executor.delete]: Deleted the Triggered Job {job.name} as it has reached the maximum "
                      f"runs.")
                return JsonResponse({'status': 'error', 'message': 'Maximum runs reached for the triggered job'}, status=400)

            # [0] Create a new TriggeredJobInstance for tracking
            new_instance = TriggeredJobInstance.objects.create(
                triggered_job=job, status=TriggeredJobInstanceStatusesNames.PENDING, webhook_payload=payload
            )
            # add it to the job
            job.triggered_job_instances.add(new_instance)
            job.save()
            # [1] Update the job run count
            job.current_run_count += 1
            job.save()
            new_instance.execution_index = job.current_run_count
            new_instance.save()
            print(f"[Triggered Job Executor]: Received a new webhook payload for the Triggered Job {job.name} ")
            # Process the event
            self.handle_triggered_job(job=job, instance=new_instance)
            return JsonResponse({
                'status': 'success', 'message': 'Webhook payload received successfully',
                'data': { 'assistant_id': assistant_id, 'triggered_job_id': triggered_job_id, 'payload': payload }
            }, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON object'}, status=400)

    @staticmethod
    def handle_triggered_job(job, instance):
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
        try:
            # [2] Create a chat
            chat = MultimodalChat.objects.create(
                user=job.created_by_user,
                organization=job.trigger_assistant.organization,
                assistant=job.trigger_assistant,
                chat_name=generate_triggered_job_chat_name(job.name),
                created_by_user=job.created_by_user,
                chat_source=ChatSourcesNames.TRIGGERED,
            )
            # [3] Set the status as building
            instance.status = TriggeredJobInstanceStatusesNames.BUILDING
            instance.save()
            # [4] Create the instruction prompt
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
            # [5] Send the instruction feed message
            instruction_feed_message = MultimodalChatMessage.objects.create(
                multimodal_chat=chat,
                sender_type='USER',
                message_text_content=instruction_feed
            )
            # [6] Set the status as initializing assistant
            instance.status = TriggeredJobInstanceStatusesNames.INITIALIZING_ASSISTANT
            instance.save()
            # [7] Initialize the assistant client
            llm_client = InternalLLMClient.get(assistant=chat.assistant, multimodal_chat=chat)
            # [8] Set the status as generating
            instance.status = TriggeredJobInstanceStatusesNames.GENERATING
            instance.save()
            # [9] Get the response
            response_text = llm_client.respond(latest_message=instruction_feed_message)
            # [10] Set the status as saving logs
            instance.status = TriggeredJobInstanceStatusesNames.SAVING_LOGS
            instance.save()
            # [11] Save the logs
            instance.logs = response_text
            instance.save()
            # [12] Set the status as cleaning up
            instance.status = TriggeredJobInstanceStatusesNames.CLEANING_UP
            instance.save()
            # [13] Delete the chat
            chat.delete()
            # [14] Set the status as completed
            instance.status = TriggeredJobInstanceStatusesNames.COMPLETED
            instance.ended_at = timezone.now()
            instance.save()
            # [15] Add the transaction
            transaction = LLMTransaction(
                organization=job.assistant.organization, model=job.assistant.llm_model, responsible_user=None,
                responsible_assistant=job.assistant, encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=ToolCostsMap.TriggeredJobExecutor.COST, transaction_type=ChatRoles.SYSTEM,
                transaction_source=TransactionSourcesNames.TRIGGER_JOB_EXECUTION, is_tool_cost=True
            )
            transaction.save()
        except Exception as e:
            instance.status = TriggeredJobInstanceStatusesNames.FAILED
            instance.save()
            print(f"[Triggered Job Executor]: Failed to execute the triggered job {job.name} due to an error: {e}")


class CreateTriggeredJobView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of new triggered jobs.

    This view allows users to create triggered jobs that are associated with an assistant and can be executed based on specific events. The view checks user permissions before allowing the creation of a new triggered job.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the form for creating a triggered job.
        post(self, request, *args, **kwargs): Processes the form submission to create a new triggered job.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = TriggeredJobForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TriggeredJobForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD_TRIGGERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_TRIGGERS):
            messages.error(self.request, "You do not have permission to add triggered jobs.")
            return redirect('mm_triggered_jobs:list')
        ##############################

        if form.is_valid():
            triggered_job = form.save(commit=False)
            triggered_job.created_by_user = request.user
            # Handle dynamic fields
            step_guide = request.POST.getlist('step_guide[]')
            triggered_job.step_guide = step_guide
            triggered_job.save()
            messages.success(request, "Triggered Job created successfully!")
            print('[CreateTriggeredJobView.post] Triggered Job created successfully.')
            return redirect('mm_triggered_jobs:list')
        else:
            messages.error(request, "There was an error creating the triggered job.")
            return self.render_to_response({'form': form})


class ListTriggeredJobsView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of triggered jobs associated with the user's assistants.

    This view retrieves and displays all triggered jobs that are available to the current user, with support for searching and pagination.

    Methods:
        get_context_data(self, **kwargs): Retrieves the user's accessible triggered jobs and adds them to the context.
    """

    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_TRIGGERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_TRIGGERS):
            messages.error(self.request, "You do not have permission to list triggered jobs.")
            return context
        ##############################

        search_query = self.request.GET.get('search', '')
        user_organizations = self.request.user.organizations.all()
        organization_assistants = user_organizations.values_list('assistants', flat=True)
        triggered_jobs_list = TriggeredJob.objects.filter(trigger_assistant__in=organization_assistants)

        if search_query:
            triggered_jobs_list = triggered_jobs_list.filter(
                Q(name__icontains=search_query) | Q(task_description__icontains=search_query)
            )
        paginator = Paginator(triggered_jobs_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['triggered_jobs'] = page_obj.object_list
        context['total_triggered_jobs'] = TriggeredJob.objects.count()
        context['search_query'] = search_query
        return context


class ListTriggeredJobLogsView(LoginRequiredMixin, TemplateView):
    """
    Displays the logs of a specific triggered job.

    This view retrieves and displays all instances of a triggered job, showing the execution logs and statuses. The view supports searching and pagination.

    Methods:
        get_context_data(self, **kwargs): Retrieves the logs of the specified triggered job and adds them to the context.
    """

    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_TRIGGERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_TRIGGERS):
            messages.error(self.request, "You do not have permission to list triggered jobs.")
            return context
        ##############################

        triggered_job_id = self.kwargs.get('pk')
        triggered_job = get_object_or_404(TriggeredJob, id=triggered_job_id)
        context['triggered_job'] = triggered_job
        search_query = self.request.GET.get('search', '')
        job_instances_list = TriggeredJobInstance.objects.filter(triggered_job=triggered_job)
        if search_query:
            job_instances_list = job_instances_list.filter(Q(status__icontains=search_query))

        paginator = Paginator(job_instances_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['triggered_job_instances'] = page_obj.object_list
        context['total_triggered_job_instances'] = job_instances_list.count()
        context['search_query'] = search_query
        return context


class ConfirmDeleteTriggeredJobView(LoginRequiredMixin, TemplateView):
    """
    Handles the deletion of triggered jobs.

    This view allows users to delete specific triggered jobs, provided they have the necessary permissions. The view presents a confirmation page before the deletion is processed.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for the deletion confirmation page.
        post(self, request, *args, **kwargs): Processes the deletion of the specified triggered job.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        triggered_job_id = self.kwargs.get('pk')
        triggered_job = get_object_or_404(TriggeredJob, id=triggered_job_id)
        context['triggered_job'] = triggered_job
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_TRIGGERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_TRIGGERS):
            messages.error(self.request, "You do not have permission to delete triggered jobs.")
            return redirect('mm_triggered_jobs:list')
        ##############################

        triggered_job_id = self.kwargs.get('pk')
        triggered_job = get_object_or_404(TriggeredJob, id=triggered_job_id)
        triggered_job.delete()
        print('[ConfirmDeleteTriggeredJobView.post] Triggered Job deleted successfully.')
        messages.success(request, "Triggered Job deleted successfully.")
        return redirect('mm_triggered_jobs:list')
