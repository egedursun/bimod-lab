#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
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

from apps.message_templates.views import (
    MessageTemplateView_List,
    MessageTemplateView_Create,
    MessageTemplateView_Update,
    MessageTemplateView_Delete
)

app_name = "message_templates"

urlpatterns = [
    path(
        "list/",
        MessageTemplateView_List.as_view(
            template_name="message_templates/list_message_templates.html"
        ),
        name="list"
    ),

    path(
        "create/",
        MessageTemplateView_Create.as_view(
            template_name="message_templates/create_message_template.html"
        ),
        name="create"
    ),

    path(
        "<int:pk>/update/",
        MessageTemplateView_Update.as_view(
            template_name="message_templates/update_message_template.html"
        ),
        name="update"
    ),

    path(
        "<int:pk>/delete/",
        MessageTemplateView_Delete.as_view(

        ),
        name="delete"
    ),
]
