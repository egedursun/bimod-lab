#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django.urls import path
from .views import DashboardMainView, RefreshStatisticsView, ChangeStatisticsDatetimeIntervalView

app_name = "dashboard"

urlpatterns = [
    path("", DashboardMainView.as_view(template_name="dashboard/dashboard_main.html"), name="main-dashboard"),
    path("refresh/<str:days>/", RefreshStatisticsView.as_view(
        template_name="dashboard/dashboard_main.html"
    ), name="refresh"),
    path("adjust_interval/<int:days>/", ChangeStatisticsDatetimeIntervalView.as_view(
        template_name="dashboard/dashboard_main.html"
    ), name="adjust-interval"),
]
