"""
This module provides views for managing scheduled jobs within the Bimod.io platform.

The views allow authenticated users to create, list, view logs, and delete scheduled jobs. Permissions are checked to ensure that users have the appropriate rights to perform these actions.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.mm_scheduled_jobs.forms import ScheduledJobForm
from apps.mm_scheduled_jobs.models import ScheduledJob, ScheduledJobInstance
from apps.user_permissions.models import UserPermission
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CreateScheduledJobView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of new scheduled jobs.

    This view allows users to create scheduled jobs that can be executed by their assistants. The view checks user permissions before allowing the creation of a new scheduled job.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the form for creating a scheduled job.
        post(self, request, *args, **kwargs): Processes the form submission to create a new scheduled job and associates it with the user.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = ScheduledJobForm()
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_SCHEDULED_JOBS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_SCHEDULED_JOBS):
            messages.error(self.request, "You do not have permission to add scheduled jobs.")
            return redirect('mm_scheduled_jobs:list')
        ##############################

        form = ScheduledJobForm(request.POST)
        if form.is_valid():
            scheduled_job = form.save(commit=False)
            scheduled_job.created_by_user = request.user
            # Handle dynamic fields
            step_guide = request.POST.getlist('step_guide[]')
            scheduled_job.step_guide = step_guide
            scheduled_job.save()
            print('[CreateScheduledJobView.post] Scheduled Job created successfully.')
            messages.success(request, "Scheduled Job created successfully!")
            return redirect('mm_scheduled_jobs:list')
        else:
            messages.error(request, "There was an error creating the scheduled job.")
            return self.render_to_response({'form': form})


class ListScheduledJobsView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of scheduled jobs associated with the user's organization.

    This view retrieves and displays all scheduled jobs that are available to the current user, with support for searching and pagination.

    Methods:
        get_context_data(self, **kwargs): Retrieves the user's accessible scheduled jobs and adds them to the context.
    """

    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_SCHEDULED_JOBS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_SCHEDULED_JOBS):
            messages.error(self.request, "You do not have permission to list scheduled jobs.")
            return context
        ##############################

        search_query = self.request.GET.get('search', '')
        user_organizations = self.request.user.organizations.all()
        organization_assistants = user_organizations.values_list('assistants', flat=True)
        scheduled_jobs_list = ScheduledJob.objects.filter(assistant__in=organization_assistants)
        if search_query:
            scheduled_jobs_list = scheduled_jobs_list.filter(
                Q(name__icontains=search_query) | Q(task_description__icontains=search_query)
            )
        paginator = Paginator(scheduled_jobs_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['scheduled_jobs'] = page_obj.object_list
        context['total_scheduled_jobs'] = ScheduledJob.objects.count()
        context['search_query'] = search_query
        return context


class ListScheduledJobLogsView(LoginRequiredMixin, TemplateView):
    """
    Displays logs of scheduled job instances.

    This view retrieves and displays all instances of a specific scheduled job, with support for searching and pagination.

    Methods:
        get_context_data(self, **kwargs): Retrieves the logs of the scheduled job instances and adds them to the context.
    """

    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_SCHEDULED_JOBS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_SCHEDULED_JOBS):
            messages.error(self.request, "You do not have permission to list scheduled jobs.")
            return context
        ##############################

        scheduled_job_id = self.kwargs.get('pk')
        scheduled_job = get_object_or_404(ScheduledJob, id=scheduled_job_id)
        context['scheduled_job'] = scheduled_job
        search_query = self.request.GET.get('search', '')
        job_instances_list = ScheduledJobInstance.objects.filter(scheduled_job=scheduled_job)
        if search_query:
            job_instances_list = job_instances_list.filter(Q(status__icontains=search_query))
        paginator = Paginator(job_instances_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['scheduled_job_instances'] = page_obj.object_list
        context['total_scheduled_job_instances'] = job_instances_list.count()
        context['search_query'] = search_query
        return context


class ConfirmDeleteScheduledJobView(LoginRequiredMixin, TemplateView):
    """
    Handles the deletion of scheduled jobs.

    This view allows users to delete specific scheduled jobs, provided they have the necessary permissions.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for the deletion confirmation page.
        post(self, request, *args, **kwargs): Processes the deletion of the specified scheduled job.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        scheduled_job_id = self.kwargs.get('pk')
        scheduled_job = get_object_or_404(ScheduledJob, id=scheduled_job_id)
        context['scheduled_job'] = scheduled_job
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_SCHEDULED_JOBS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_SCHEDULED_JOBS):
            messages.error(self.request, "You do not have permission to delete scheduled jobs.")
            return redirect('mm_scheduled_jobs:list')
        ##############################

        scheduled_job_id = self.kwargs.get('pk')
        scheduled_job = get_object_or_404(ScheduledJob, id=scheduled_job_id)
        scheduled_job.delete()
        print('[ConfirmDeleteScheduledJobView.post] Scheduled Job deleted successfully.')
        messages.success(request, "Scheduled Job deleted successfully.")
        return redirect('mm_scheduled_jobs:list')
