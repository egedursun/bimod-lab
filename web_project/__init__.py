#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: __init__.py
#  Last Modified: 2024-06-20 04:48:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:17:53
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

# from web_project.bootstrap import TemplateBootstrap
from web_project.template_helpers.theme import TemplateHelper
from django.conf import settings


class TemplateLayout:
    # Initialize the bootstrap files and page layout
    def init(self, context):
        # Init the Template Context using TEMPLATE_CONFIG
        context = TemplateHelper.init_context(context)
        # Set a default layout globally using settings.py. Can be set in the page level view file as well.
        layout = context["layout"]

        # Set the selected layout
        context.update(
            {
                "layout_path": TemplateHelper.set_layout(
                    "layout_" + layout + ".html", context
                ),
                # Set default rtl True if the language Arabic else use rtl_mode value from TEMPLATE_CONFIG
                "rtl_mode": True
                if self.request.COOKIES.get('django_text_direction') == "rtl"
                else settings.TEMPLATE_CONFIG.get("rtl_mode"),
            }
        )

        # Map context variables
        TemplateHelper.map_context(context)

        return context
