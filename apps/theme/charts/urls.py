#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-06-28 19:08:37
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:28
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#

from django.urls import path
from .views import ChartsView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "charts/apex/",
        login_required(ChartsView.as_view(template_name="charts_apex.html")),
        name="charts-apex",
    ),
    path(
        "charts/chartjs/",
        login_required(ChartsView.as_view(template_name="charts_chartjs.html")),
        name="charts-chartjs",
    ),
]
