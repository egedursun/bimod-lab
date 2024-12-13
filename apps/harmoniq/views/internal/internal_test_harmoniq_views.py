#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: internal_test_harmoniq_views.py
#  Last Modified: 2024-10-07 01:00:36
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-07 01:00:37
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.views.generic import (
    TemplateView
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class HarmoniqView_TestInternal(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        logger.info(f"Internal Test Harmoniq View was accessed by User: {self.request.user.id}.")

        return context
