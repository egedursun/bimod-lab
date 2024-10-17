#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:31
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.urls import path
from .views import CardView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "cards/basic/",
        login_required(CardView.as_view(template_name="cards_basic.html")),
        name="cards-basic",
    ),
    path(
        "cards/advance/",
        login_required(CardView.as_view(template_name="cards_advance.html")),
        name="cards-advance",
    ),
    path(
        "cards/statistics/",
        login_required(CardView.as_view(template_name="cards_statistics.html")),
        name="cards-statistics",
    ),
    path(
        "cards/analytics/",
        login_required(CardView.as_view(template_name="cards_analytics.html")),
        name="cards-analytics",
    ),
    path(
        "cards/actions/",
        login_required(CardView.as_view(template_name="cards_actions.html")),
        name="cards-actions",
    ),
]
