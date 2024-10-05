#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-09-25 17:51:06
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

from .views import AcademyView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "app/academy/dashboard/",
        login_required(AcademyView.as_view(template_name="app_academy_dashboard.html")),
        name="app-academy-dashboard",
    ),
    path(
        "app/academy/course/",
        login_required(AcademyView.as_view(template_name="app_academy_course.html")),
        name="app-academy-course",
    ),
    path(
        "app/academy/course_details/",
        login_required(AcademyView.as_view(template_name="app_academy_course_details.html")),
        name="app-academy-course-details",
    ),
]
