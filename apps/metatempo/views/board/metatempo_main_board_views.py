#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metatempo_main_board_views.py
#  Last Modified: 2024-10-28 20:30:23
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 20:30:23
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


class MetaTempoView_MainBoard(LoginRequiredMixin, TemplateView):

    # TODO-EGE: SIMPLE-VIEW: This will be the primary page for seeing and interpreting the logs produced by the AI
    #       assistant regarding 'member logs', 'member daily logs', and 'overall logs'. The user will also be able
    #       to 'purge the logs', 'click and connect to AI agent' to gather insights and more information, see the
    #       'api key' for connecting to the 'MetaKanban Tracker via Electron', and his 'own key' for associating the
    #       user with the tracked user. (This requires 'user model' update: add new field: 'metatempo_tracking_auth_key')
    #       The user can also click 'regenerate API key' to create a new key for the 'MetaKanban Tracker via Electron'.

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context
