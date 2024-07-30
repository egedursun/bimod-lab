from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from apps.mm_scheduled_jobs.forms import ScheduledJobForm
from apps.mm_scheduled_jobs.models import ScheduledJob, ScheduledJobInstance
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


# Create your views here.

class CreateScheduledJobView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = ScheduledJobForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ScheduledJobForm(request.POST)

        ##############################
        # PERMISSION CHECK FOR - ADD SCHEDULED JOBS
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=request.user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_SCHEDULED_JOBS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to add scheduled jobs."}
            return self.render_to_response(context)
        ##############################

        if form.is_valid():
            scheduled_job = form.save(commit=False)
            scheduled_job.created_by_user = request.user

            # Handle dynamic fields
            step_guide = request.POST.getlist('step_guide[]')
            scheduled_job.step_guide = step_guide

            scheduled_job.save()

            messages.success(request, "Scheduled Job created successfully!")
            return redirect('mm_scheduled_jobs:list')
        else:
            messages.error(request, "There was an error creating the scheduled job.")
            return self.render_to_response({'form': form})


class ListScheduledJobsView(LoginRequiredMixin, TemplateView):
    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        search_query = self.request.GET.get('search', '')
        user_organizations = self.request.user.organizations.all()
        organization_assistants = user_organizations.values_list('assistants', flat=True)

        scheduled_jobs_list = ScheduledJob.objects.filter(
            assistant__in=organization_assistants
        )

        if search_query:
            scheduled_jobs_list = scheduled_jobs_list.filter(
                Q(name__icontains=search_query) |
                Q(task_description__icontains=search_query)
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
    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        scheduled_job_id = self.kwargs.get('pk')
        scheduled_job = get_object_or_404(ScheduledJob, id=scheduled_job_id)
        context['scheduled_job'] = scheduled_job

        search_query = self.request.GET.get('search', '')
        job_instances_list = ScheduledJobInstance.objects.filter(scheduled_job=scheduled_job)

        if search_query:
            job_instances_list = job_instances_list.filter(
                Q(status__icontains=search_query)
            )

        paginator = Paginator(job_instances_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['scheduled_job_instances'] = page_obj.object_list
        context['total_scheduled_job_instances'] = job_instances_list.count()
        context['search_query'] = search_query
        return context


class ConfirmDeleteScheduledJobView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        scheduled_job_id = self.kwargs.get('pk')
        scheduled_job = get_object_or_404(ScheduledJob, id=scheduled_job_id)
        context['scheduled_job'] = scheduled_job
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE SCHEDULED JOBS
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=request.user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_SCHEDULED_JOBS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to delete scheduled jobs."}
            return self.render_to_response(context)
        ##############################

        scheduled_job_id = self.kwargs.get('pk')
        scheduled_job = get_object_or_404(ScheduledJob, id=scheduled_job_id)
        scheduled_job.delete()
        messages.success(request, "Scheduled Job deleted successfully.")
        return redirect('mm_scheduled_jobs:list')
