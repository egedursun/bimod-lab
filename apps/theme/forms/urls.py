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
from .views import FormsView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "forms/basic_inputs/",
        login_required(FormsView.as_view(template_name="forms_basic_inputs.html")),
        name="forms-basic-inputs",
    ),
    path(
        "forms/input_groups/",
        login_required(FormsView.as_view(template_name="forms_input_groups.html")),
        name="forms-input-groups",
    ),
    path(
        "forms/custom_options/",
        login_required(FormsView.as_view(template_name="forms_custom_options.html")),
        name="forms-custom-options",
    ),
    path(
        "forms/editors/",
        login_required(FormsView.as_view(template_name="forms_editors.html")),
        name="forms-editors",
    ),
    path(
        "forms/file_upload/",
        login_required(FormsView.as_view(template_name="forms_file_upload.html")),
        name="forms-file-upload",
    ),
    path(
        "forms/pickers/",
        login_required(FormsView.as_view(template_name="forms_pickers.html")),
        name="forms-pickers",
    ),
    path(
        "forms/selects/",
        login_required(FormsView.as_view(template_name="forms_selects.html")),
        name="forms-selects",
    ),
    path(
        "forms/sliders/",
        login_required(FormsView.as_view(template_name="forms_sliders.html")),
        name="forms-sliders",
    ),
    path(
        "forms/switches/",
        login_required(FormsView.as_view(template_name="forms_switches.html")),
        name="forms-switches",
    ),
    path(
        "forms/extras/",
        login_required(FormsView.as_view(template_name="forms_extras.html")),
        name="forms-extras",
    ),
]
