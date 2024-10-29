#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metatempo_purge_logs_views.py
#  Last Modified: 2024-10-28 20:30:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 20:30:32
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


class MetaTempoView_PurgeLogs(LoginRequiredMixin, View):

    # TODO-EGE: SIMPLE-VIEW: This will delete all individual logs, as well as the overall logs associated with the
    #       connection. This will be a 'hard-deletion' operation, and it will be irreversible.

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass
