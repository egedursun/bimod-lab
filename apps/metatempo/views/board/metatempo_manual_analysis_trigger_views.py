#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metatempo_manual_analysis_trigger_views.py
#  Last Modified: 2024-10-28 20:31:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 20:31:16
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
from django.views import View


class MetaTempoView_TriggerManualAnalysis(LoginRequiredMixin, View):

    # TODO-EGE: Functional view, this will manually trigger the 'overall analysis' function in the 'executor' in
    #   'core' directory.

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass
