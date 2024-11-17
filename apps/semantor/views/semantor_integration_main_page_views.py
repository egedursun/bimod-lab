#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: semantor_integration_main_page_views.py
#  Last Modified: 2024-11-10 00:31:28
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-10 00:31:28
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.semantor.models import SemantorConfiguration
from web_project import TemplateLayout


class SemantorView_Configure(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        config, created = SemantorConfiguration.objects.get_or_create(user=self.request.user)
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['config'] = config
        return context

    def post(self, request, *args, **kwargs):
        try:
            config = SemantorConfiguration.objects.filter(user=request.user).first()
            if config:
                config.is_local_network_active = request.POST.get('is_local_network_active') == 'on'
                config.is_global_network_active = request.POST.get('is_global_network_active') == 'on'
                config.maximum_assistant_search_items = int(
                    request.POST.get('maximum_assistant_search_items', config.maximum_assistant_search_items))
                config.maximum_integration_search_items = int(
                    request.POST.get('maximum_integration_search_items', config.maximum_integration_search_items))
                config.save()
                messages.success(request, "Configuration updated successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred while updating the configuration: {str(e)}")
            return redirect("semantor:configuration")

        return redirect("semantor:configuration")

####################################################################################################
