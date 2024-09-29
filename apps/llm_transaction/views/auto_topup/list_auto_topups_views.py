#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: list_auto_topups_views.py
#  Last Modified: 2024-09-28 15:44:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:57:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.organization.models import Organization
from web_project import TemplateLayout


class ListAutomatedTopUpPlans(LoginRequiredMixin, TemplateView):
    """
    Displays a list of automated balance top-up plans for the user's organizations.

    This view allows users to manage their automated top-up plans, including deleting existing plans.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the organizations associated with the current user and their respective top-up plans.
        post(self, request, *args, **kwargs): Processes the form submission to delete an automated top-up plan.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        return context

    def post(self, request, *args, **kwargs):
        organization_id = request.POST.get('organization_id')
        organization = Organization.objects.get(id=organization_id)
        if 'delete' in request.POST:
            organization.auto_balance_topup.delete()
            organization.auto_balance_topup = None
            organization.save()
        return redirect('llm_transaction:auto_top_up_list')
