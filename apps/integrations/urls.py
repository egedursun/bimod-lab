#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-11-05 19:19:46
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-05 19:19:47
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

from apps.integrations.views import (
    IntegrationView_IntegrationCategoryStore,
    IntegrationView_IntegrationCategoriesList,
    IntegrationView_IntegrateAssistantToOrganization
)

app_name = 'integrations'

urlpatterns = [
    path(
        "categories/",
        IntegrationView_IntegrationCategoriesList.as_view(
            template_name="integrations/list_integration_categories.html"
        ),
        name="list"
    ),

    path(
        "categories/<slug:category_slug>/",
        IntegrationView_IntegrationCategoryStore.as_view(
            template_name="integrations/store_integration_category.html"
        ),
        name="store"
    ),

    path(
        "integrate/",
        IntegrationView_IntegrateAssistantToOrganization.as_view(

        ),
        name="integrate"
    ),
]
