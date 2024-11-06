#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: store_integration_category_views.py
#  Last Modified: 2024-11-05 19:46:44
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-05 19:46:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.integrations.models import AssistantIntegration
from web_project import TemplateLayout


class IntegrationView_IntegrationCategoryStore(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        integrations = AssistantIntegration.objects.filter(integration_category__category_slug=self.kwargs['category_slug']).order_by("integration_name")
        context['assistants'] = integrations
        return context
