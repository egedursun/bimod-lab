#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: detail_hadron_system_views.py
#  Last Modified: 2024-10-18 00:28:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-18 00:28:09
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
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from apps.hadron_prime.models import HadronSystem, HadronNode, HadronTopic
from apps.organization.models import Organization
from web_project import TemplateLayout


# In this page, the user will be able to see:
#  1. The details and information of the system data model.
#  2. The list of nodes in the system. -> When clicked, redirects to: Detail Node, Update Node, Delete Node
#  3. The list of topics in the system. -> When clicked, redirects to: Detail Topic, Update Topic, Delete Topic


class HadronPrimeView_DetailHadronSystem(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        system_id = self.kwargs['pk']
        system = HadronSystem.objects.get(pk=system_id)
        nodes = HadronNode.objects.filter(system=system)
        topics = HadronTopic.objects.filter(system=system)
        nodes_paginator = Paginator(nodes, 10)
        topics_paginator = Paginator(topics, 10)
        nodes_page_number = self.request.GET.get('nodes_page')
        topics_page_number = self.request.GET.get('topics_page')
        nodes_page_obj = nodes_paginator.get_page(nodes_page_number)
        topics_page_obj = topics_paginator.get_page(topics_page_number)
        context['hadron_system'] = system
        context['nodes_page_obj'] = nodes_page_obj
        context['topics_page_obj'] = topics_page_obj
        return context
