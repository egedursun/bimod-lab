#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:32
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
from .views import LogisticsView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "app/logistics/dashboard/",
        login_required(LogisticsView.as_view(template_name="app_logistics_dashboard.html")),
        name="app-logistics-dashboard",
    ),
    path(
        "app/logistics/fleet/",
        login_required(LogisticsView.as_view(template_name="app_logistics_fleet.html")),
        name="app-logistics-fleet",
    ),
]
