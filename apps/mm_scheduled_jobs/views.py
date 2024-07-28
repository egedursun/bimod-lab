from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from apps.mm_scheduled_jobs.forms import ScheduledJobForm
from apps.mm_scheduled_jobs.models import ScheduledJob
from web_project import TemplateLayout


# Create your views here.

class CreateScheduledJobView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = ScheduledJobForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ScheduledJobForm(request.POST)

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

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class ListScheduledJobLogsView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class ConfirmDeleteScheduledJobView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context
