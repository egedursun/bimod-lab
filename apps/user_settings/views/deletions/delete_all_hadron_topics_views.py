#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_hadron_topics_views.py
#  Last Modified: 2024-10-18 21:54:39
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-18 21:55:39
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
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.hadron_prime.models import HadronTopic
from apps.organization.models import Organization
import logging

from apps.user_permissions.utils import PermissionNames

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllHadronTopics(View, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        user = request.user
        user_orgs = Organization.objects.filter(users__in=[user])
        hadron_topics = HadronTopic.objects.filter(system__organization__in=user_orgs)
        confirmation_field = request.POST.get('confirmation', None)
        if confirmation_field != 'CONFIRM DELETING ALL HADRON TOPICS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL HADRON TOPICS'.")
            logger.error(f"Invalid confirmation field: {confirmation_field}")
            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_HADRON_TOPICS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_HADRON_TOPICS):
            messages.error(self.request, "You do not have permission to delete hadron topics.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for hadron_topic in hadron_topics:
                hadron_topic.delete()
            logger.info(f"All hadron topics associated with User: {user.id} have been deleted.")
            messages.success(request, "All hadron topics associated with your account have been deleted.")
        except Exception as e:
            logger.error(f"Error deleting hadron topics: {e}")
            messages.error(request, f"Error deleting hadron topics: {e}")
        return redirect('user_settings:settings')
