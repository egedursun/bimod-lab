#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-11-03 17:19:44
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-03 17:19:53
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

ACADEMY_COURSE_ADMIN_LIST = [
    'course_title',
    'course_language',
    'course_instructor',
    'created_at',
    'updated_at'
]
ACADEMY_COURSE_ADMIN_SEARCH = [
    'course_title',
    'course_language',
    'course_instructor__full_name'
]
ACADEMY_COURSE_ADMIN_FILTER = [
    'course_language',
    'created_at',
    'updated_at'
]

ACADEMY_COURSE_INSTRUCTOR_ADMIN_LIST = (
    'full_name',
    'user',
    'created_at',
    'updated_at'
)
ACADEMY_COURSE_INSTRUCTOR_ADMIN_SEARCH = (
    'full_name',
    'user__email'
)
ACADEMY_COURSE_INSTRUCTOR_ADMIN_FILTER = (
    'created_at',
    'updated_at'
)

ACADEMY_COURSE_SECTION_ADMIN_LIST = [
    'section_name',
    'course',
    'created_at',
    'updated_at'
]
ACADEMY_COURSE_SECTION_ADMIN_SEARCH = [
    'section_name',
    'course__course_title'
]
ACADEMY_COURSE_SECTION_ADMIN_FILTER = [
    'created_at',
    'updated_at'
]

ACADEMY_COURSE_VIDEO_LIST = [
    'video_title',
    'course_section',
    'created_at',
    'updated_at'
]
ACADEMY_COURSE_VIDEO_SEARCH = [
    'video_title',
    'course_section__section_name',
    'course_section__course__course_title'
]
ACADEMY_COURSE_VIDEO_FILTER = [
    'course_section',
    'created_at',
    'updated_at'
]
