#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_hadron_node_views.py
#  Last Modified: 2024-10-17 22:51:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:51:32
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.hadron_prime.models import HadronNode
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class HadronPrimeView_DeleteHadronNode(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        node = get_object_or_404(HadronNode, id=kwargs['pk'])
        context['node'] = node
        return context

    def post(self, request, *args, **kwargs):
        node = get_object_or_404(HadronNode, id=kwargs['pk'])
        system_id = node.system.id
        node.delete()
        logger.info(f'Hadron Node "{node.node_name}" deleted by user "{request.user}".')
        messages.success(request, f'The Hadron Node "{node.node_name}" was successfully deleted.')
        return redirect('hadron_prime:detail_hadron_system', pk=system_id)
