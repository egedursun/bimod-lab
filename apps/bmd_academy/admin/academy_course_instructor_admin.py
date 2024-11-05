#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: academy_course_instructor_admin.py
#  Last Modified: 2024-11-03 18:39:36
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-03 18:39:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


from django.contrib import admin

from apps.bmd_academy.models import AcademyCourseInstructor
from apps.bmd_academy.utils import ACADEMY_COURSE_INSTRUCTOR_ADMIN_LIST, ACADEMY_COURSE_INSTRUCTOR_ADMIN_SEARCH, \
    ACADEMY_COURSE_INSTRUCTOR_ADMIN_FILTER


@admin.register(AcademyCourseInstructor)
class AcademyCourseInstructorAdmin(admin.ModelAdmin):
    list_display = ACADEMY_COURSE_INSTRUCTOR_ADMIN_LIST
    search_fields = ACADEMY_COURSE_INSTRUCTOR_ADMIN_SEARCH
    list_filter = ACADEMY_COURSE_INSTRUCTOR_ADMIN_FILTER
    ordering = ('-created_at',)
