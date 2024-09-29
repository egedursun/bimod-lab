#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: urls.py
#  Last Modified: 2024-08-30 13:22:33
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:27:41
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

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
