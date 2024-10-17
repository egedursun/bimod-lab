#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:32
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
from .views import FormLayoutsView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "form/layouts_vertical/",
        login_required(FormLayoutsView.as_view(template_name="form_layouts_vertical.html")),
        name="form-layouts-vertical",
    ),
    path(
        "form/layouts_horizontal/",
        login_required(FormLayoutsView.as_view(template_name="form_layouts_horizontal.html")),
        name="form-layouts-horizontal",
    ),
    path(
        "form/layouts_sticky/",
        login_required(FormLayoutsView.as_view(template_name="form_layouts_sticky.html")),
        name="form-layouts-sticky",
    ),
]
