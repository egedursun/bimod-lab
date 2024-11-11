#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-11-06 23:24:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-06 23:24:38
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

from apps.ml_model_store.views import MLModelStoreView_IntegrateMLModel, MLModelStoreView_StoreMLModelsList

app_name = 'ml_model_store'

urlpatterns = [
    path('list/', MLModelStoreView_StoreMLModelsList.as_view(
        template_name='ml_model_store/store_ml_models_list.html'), name='list'),

    path("integrate/", MLModelStoreView_IntegrateMLModel.as_view(), name="integrate"),
]
