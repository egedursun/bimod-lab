#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_hadron_topic_views.py
#  Last Modified: 2024-10-17 22:50:07
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:50:07
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
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.hadron_prime.models import HadronSystem, HadronTopic
from apps.hadron_prime.utils import HADRON_TOPIC_CATEGORIES
from apps.organization.models import Organization
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class HadronPrimeView_CreateHadronTopic(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        systems = HadronSystem.objects.filter(organization__in=user_orgs)

        context['organizations'] = user_orgs
        context['systems'] = systems
        context['topic_categories'] = HADRON_TOPIC_CATEGORIES
        return context

    def post(self, request, *args, **kwargs):
        system_id = request.POST.get('system')
        topic_name = request.POST.get('topic_name')
        topic_description = request.POST.get('topic_description')
        topic_purpose = request.POST.get('topic_purpose')
        topic_category = request.POST.get('topic_category')

        if not system_id or not topic_name or not topic_category:
            logger.error('The required fields are not filled out.')
            messages.error(request, 'Please fill out all required fields.')
            return redirect('hadron_prime:create_hadron_topic')

        system = HadronSystem.objects.get(id=system_id)
        HadronTopic.objects.create(
            system=system, topic_name=topic_name, topic_description=topic_description,
            topic_purpose=topic_purpose, topic_category=topic_category, created_by_user=request.user)

        logger.info(f'Hadron Topic "{topic_name}" created.')
        messages.success(request, f'Hadron Topic "{topic_name}" created successfully.')
        return redirect('hadron_prime:list_hadron_system')
