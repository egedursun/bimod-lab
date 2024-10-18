#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_hadron_topics_views.py
#  Last Modified: 2024-10-17 22:50:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:50:34
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

from apps.hadron_prime.models import HadronTopic
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class HadronPrimeView_DeleteHadronTopic(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        topic_id = kwargs.get('pk')
        hadron_topic = get_object_or_404(HadronTopic, id=topic_id)
        context['hadron_topic'] = hadron_topic
        return context

    def post(self, request, *args, **kwargs):
        topic_id = kwargs.get('pk')
        hadron_topic = get_object_or_404(HadronTopic, id=topic_id)
        hadron_topic.delete()
        logger.info(f'Hadron Topic "{hadron_topic.topic_name}" has been deleted successfully.')
        messages.success(request, f'Hadron Topic "{hadron_topic.topic_name}" has been deleted successfully.')
        return redirect('hadron_prime:list_hadron_system')
