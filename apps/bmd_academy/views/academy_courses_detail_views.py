#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: academy_courses_detail_views.py
#  Last Modified: 2024-11-03 20:04:52
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-03 20:04:52
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

from django.db.models import Prefetch
from django.views.generic import TemplateView

from apps.bmd_academy.models import (
    AcademyCourse,
    AcademyCourseSection,
    AcademyCourseVideo
)

from web_project import (
    TemplateLayout,
    TemplateHelper
)

logger = logging.getLogger(__name__)


class AcademyView_CourseDetail(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context.update(
            {
                "layout": "blank",
                "layout_path": TemplateHelper.set_layout(
                    "layout_blank.html",
                    context
                ),
            }
        )

        try:
            course = AcademyCourse.objects.prefetch_related(
                Prefetch(
                    'sections',
                    queryset=AcademyCourseSection.objects.order_by('created_at').prefetch_related(
                        Prefetch(
                            'videos',
                            queryset=AcademyCourseVideo.objects.order_by('created_at'))
                    )
                )
            ).get(
                course_slug=self.kwargs['slug']
            )
            context['course'] = course

        except Exception as e:
            logger.error(f"[AcademyView_CourseDetail] Error fetching the Academy Course: {e}")

            return context

        return context
