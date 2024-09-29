#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: urls.py
#  Last Modified: 2024-09-06 16:10:49
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:30:07
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from apps.data_security.views import (CreateNERIntegrationView, UpdateNERIntegrationView, DeleteNERIntegrationView,
                                      ListNERIntegrationsView)

app_name = "data_security"

urlpatterns = [
    path("ner/create/", CreateNERIntegrationView.as_view(
        template_name="data_security/ner/create_ner_integration.html"
    ), name="create_ner_integration"),
    path("ner/list/", ListNERIntegrationsView.as_view(
        template_name="data_security/ner/list_ner_integrations.html"
    ), name="list_ner_integrations"),
    path("ner/update/<int:pk>/", UpdateNERIntegrationView.as_view(
        template_name="data_security/ner/update_ner_integration.html"
    ), name="update_ner_integration"),
    path("ner/delete/<int:pk>/", DeleteNERIntegrationView.as_view(
        template_name="data_security/ner/confirm_delete_ner_integration.html"
    ), name="delete_ner_integration"),
]
