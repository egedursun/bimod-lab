#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#
#

from django.urls import path

from .views import (MLModelView_ManagerCreate, MLModelView_ManagerUpdate,
                    MLModelView_ManagerList, MLModelView_ManagerDelete,
                    MLModelView_ItemCreate, MLModelView_ItemList)

app_name = 'datasource_ml_models'

urlpatterns = [
    path('create/', MLModelView_ManagerCreate.as_view(
        template_name='datasource_ml_models/base/create_datasource_ml_model.html'), name='create'),
    path('update/<int:pk>/', MLModelView_ManagerUpdate.as_view(
        template_name='datasource_ml_models/base/update_datasource_ml_model.html'), name='update'),
    path('list/', MLModelView_ManagerList.as_view(
        template_name='datasource_ml_models/base/list_datasource_ml_models.html'), name='list'),
    path('delete/<int:pk>/', MLModelView_ManagerDelete.as_view(
        template_name='datasource_ml_models/base/confirm_delete_datasource_ml_model.html'), name='delete'),
    path('item/create/', MLModelView_ItemCreate.as_view(
        template_name='datasource_ml_models/models/create_datasource_ml_model_item.html'), name='item_create'),
    path('item/list/', MLModelView_ItemList.as_view(
        template_name='datasource_ml_models/models/list_datasource_ml_model_items.html'), name='item_list'),
    path('item/delete/', MLModelView_ItemList.as_view(
        template_name='datasource_ml_models/models/list_datasource_ml_model_items.html'), name='item_delete'),
]
