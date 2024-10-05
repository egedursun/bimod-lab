#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
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
from .views import (CreateOrganizationView, OrganizationListView, OrganizationUpdateView,
                    OrganizationDeleteView, OrganizationAddCreditsView, OrganizationBalanceTransferView,
                    OrganizationUserAddGiftCreditsView)

app_name = "organization"

urlpatterns = [
    path('create/',
         CreateOrganizationView.as_view(template_name="organization/create_organization.html"),
         name="create"),
    path('list/', OrganizationListView.as_view(template_name="organization/list_organizations.html"),
         name="list"),
    path('update/<int:pk>/', OrganizationUpdateView.as_view(template_name="organization/update_organization.html"),
         name="update"),
    path('delete/<int:pk>/', OrganizationDeleteView.as_view(),
         name="delete"),
    path('add_credits/<int:pk>/', OrganizationAddCreditsView.as_view(),
         name="add_credits"),

    path('balance_transfer/', OrganizationBalanceTransferView.as_view(), name='balance_transfer'),
    path('add_gift_credits/<int:pk>/', OrganizationUserAddGiftCreditsView.as_view(), name='add_gift_credits'),
]
