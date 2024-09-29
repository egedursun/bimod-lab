#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: user_settings_views.py
#  Last Modified: 2024-09-26 22:33:54
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:11:57
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from web_project import TemplateLayout


class UserSettingsView(TemplateView, LoginRequiredMixin):
    """
    Displays and manages user settings.

    GET:
    - Renders the user settings page.
    - Provides necessary context data initialized by TemplateLayout.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context
