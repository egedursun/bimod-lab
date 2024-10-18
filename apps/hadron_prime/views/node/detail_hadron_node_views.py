#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: detail_hadron_node_views.py
#  Last Modified: 2024-10-18 00:24:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-18 00:24:17
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


# TODO-EGE: Implement the detail view for the HadronNode model.

class HadronPrimeView_DetailHadronNode(LoginRequiredMixin, TemplateView):

    # In this page, the user will be able to see the execution and internal logs for the hadron nodes:
    #  1. Configuration information for the node will shown at the top.
    #  2. Execution LOGS for the node will be shown.
    #  3. Publishing LOGS for the node "per topic" will be shown.
    #  4. State-Error-Action-State-Error LOGS for the node will be shown.

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_orgs = Organization.objects.filter(users__in=[self.request.user])
        return context
