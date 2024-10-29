#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: agent_communication_views.py
#  Last Modified: 2024-10-28 20:46:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 20:46:18
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

from web_project import TemplateLayout


class MetaTempoView_AgentCommunication(LoginRequiredMixin, TemplateView):

    # TODO-EGE: Functional View: This is the view where the user will interact and ask one-shot questions to the
    #       AI agent to gather more insight about the status of the tempo within the project and the team.

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        pass
