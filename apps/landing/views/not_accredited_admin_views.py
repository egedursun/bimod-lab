#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: not_accredited_admin_views.py
#  Last Modified: 2024-09-27 18:25:50
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:54:29
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.views.generic import TemplateView

from web_project import TemplateLayout, TemplateHelper


class NotAccreditedAdminView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update(
            {
                "layout": "blank", "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
                "display_customizer": False,
            }
        )
        # map_context according to updated context values
        TemplateHelper.map_context(context)
        return context
