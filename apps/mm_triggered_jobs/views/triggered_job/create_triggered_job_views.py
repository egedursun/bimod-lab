#  Copyright Policy & Ownership
#
#  Bimod.io is a product of BMD Holdings. All materials, including but not limited to software, code, documentation,
#  graphics, design elements, and user interfaces provided by Bimod.io are protected by copyright law and international
#  treaties.
#  All content within Bimod.io is the exclusive property of BMD Holdings, unless otherwise stated.
#  Unauthorized use, distribution, or reproduction of any material contained in this software without the express
#  written consent of BMD Holdings is strictly prohibited.
#  Users may not copy, modify, distribute, display, perform, or create derivative works of Bimod.io without prior
#  written permission from BMD Holdings.


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.mm_triggered_jobs.forms import TriggeredJobForm
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


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
