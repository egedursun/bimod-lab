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
