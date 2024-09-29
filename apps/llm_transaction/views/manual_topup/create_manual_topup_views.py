#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: create_manual_topup_views.py
#  Last Modified: 2024-09-28 19:42:43
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:57:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

#
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.organization.models import Organization
from web_project import TemplateLayout


class CreateManualTopUpPlan(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        selected_organization = Organization.objects.filter(users__in=[self.request.user]).first()
        context['selected_organization'] = selected_organization
        organizations = Organization.objects.filter(users__in=[self.request.user]).all()
        context['organizations'] = organizations
        return context
