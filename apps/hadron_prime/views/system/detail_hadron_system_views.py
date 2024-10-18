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
from django.views.generic import TemplateView

from apps.organization.models import Organization
from web_project import TemplateLayout


# TODO-EGE: Implement the detail_hadron_system_views.py file.

class HadronPrimeView_DetailHadronSystem(LoginRequiredMixin, TemplateView):

    # In this page, the user will be able to see:
    #  1. The details and information of the system data model.
    #  2. The list of nodes in the system. -> When clicked, redirects to: Detail Node, Update Node, Delete Node
    #  3. The list of topics in the system. -> When clicked, redirects to: Detail Topic, Update Topic, Delete Topic

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        return context

    def post(self, request, *args, **kwargs):
        pass
