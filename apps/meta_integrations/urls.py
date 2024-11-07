#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-11-06 17:46:20
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-06 17:46:21
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
from apps.meta_integrations.views import MetaIntegrationView_MetaIntegrationCategoryList, \
    MetaIntegrationView_MetaIntegrationCategoryStore, MetaIntegrationView_IntegrateMetaIntegrationTeam

app_name = "meta_integrations"

urlpatterns = [
    path('categories/', MetaIntegrationView_MetaIntegrationCategoryList.as_view(
        template_name="meta_integrations/meta_integration_categories_list.html"), name="list"),
    path('categories/<slug:category_slug>/',
         MetaIntegrationView_MetaIntegrationCategoryStore.as_view(
             template_name="meta_integrations/store_meta_integration_category.html"), name="store"),

    path('integrate/', MetaIntegrationView_IntegrateMetaIntegrationTeam.as_view(), name="integrate"),
]
