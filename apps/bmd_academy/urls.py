#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-11-03 17:19:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-03 17:19:13
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

from apps.bmd_academy.views import AcademyView_CourseList, AcademyView_CourseDetail

app_name = 'bmd_academy'

urlpatterns = [
    path('courses/', AcademyView_CourseList.as_view(template_name='bmd_academy/academy_courses.html'),
         name='course_list'),
    path('courses/<slug:slug>/',
         AcademyView_CourseDetail.as_view(template_name='bmd_academy/academy_course_detail.html'),
         name='course_detail'),
]
