#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: detail_hadron_topic_views.py
#  Last Modified: 2024-10-18 00:17:11
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-18 00:17:12
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
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.hadron_prime.models import HadronTopic, HadronTopicMessage
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class HadronPrimeView_DetailHadronTopic(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        topic_id = kwargs.get('pk')

        ##############################
        # PERMISSION CHECK FOR - LIST_HADRON_TOPICS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_HADRON_TOPICS):
            messages.error(self.request, "You do not have permission to list Hadron Topics.")
            return context
        ##############################

        hadron_topic = get_object_or_404(HadronTopic, id=topic_id)
        messages_list = HadronTopicMessage.objects.filter(topic=hadron_topic).order_by('-created_at')
        paginator = Paginator(messages_list, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['hadron_topic'] = hadron_topic
        context['page_obj'] = page_obj
        return context
