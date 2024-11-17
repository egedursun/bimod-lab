#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: academy_courses_list_views.py
#  Last Modified: 2024-11-03 20:04:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-03 20:04:41
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from django.views.generic import TemplateView

from apps.bmd_academy.models import AcademyCourse
from web_project import TemplateLayout, TemplateHelper

logger = logging.getLogger(__name__)


class AcademyView_CourseList(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({
            "layout": "blank", "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
        })
        context['courses'] = AcademyCourse.objects.order_by("created_at").all()

        try:
            amount_videos_by_course = {}
            for course in context['courses']:
                sections = course.sections.all()
                amount_videos = 0
                for section in sections:
                    amount_videos += section.videos.count()
                amount_videos_by_course[course.id] = amount_videos
            context['amount_videos_by_course'] = amount_videos_by_course
        except Exception as e:
            logger.error(f"[AcademyView_CourseList] Error fetching the Academy Courses: {e}")
            return context

        return context
