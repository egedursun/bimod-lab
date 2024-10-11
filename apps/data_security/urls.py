#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.urls import path

from apps.data_security.views import (NERView_IntegrationCreate, NERView_IntegrationUpdate, NERView_IntegrationDelete,
                                      NERView_IntegrationList)

app_name = "data_security"

urlpatterns = [
    path("ner/create/", NERView_IntegrationCreate.as_view(
        template_name="data_security/ner/create_ner_integration.html"
    ), name="create_ner_integration"),
    path("ner/list/", NERView_IntegrationList.as_view(
        template_name="data_security/ner/list_ner_integrations.html"
    ), name="list_ner_integrations"),
    path("ner/update/<int:pk>/", NERView_IntegrationUpdate.as_view(
        template_name="data_security/ner/update_ner_integration.html"
    ), name="update_ner_integration"),
    path("ner/delete/<int:pk>/", NERView_IntegrationDelete.as_view(
        template_name="data_security/ner/confirm_delete_ner_integration.html"
    ), name="delete_ner_integration"),
]
