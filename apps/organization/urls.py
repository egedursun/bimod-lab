#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.urls import path

from .views import (
    OrganizationView_OrganizationCreate,
    OrganizationView_OrganizationList,
    OrganizationView_OrganizationUpdate,
    OrganizationView_OrganizationDelete,
    OrganizationView_AddBalanceCredits,
    OrganizationView_TransferBalance,
    OrganizationView_AddGiftCredits
)

app_name = "organization"

urlpatterns = [
    path(
        'create/',
        OrganizationView_OrganizationCreate.as_view(
            template_name="organization/create_organization.html"
        ),
        name="create"
    ),

    path(
        'list/',
        OrganizationView_OrganizationList.as_view(
            template_name="organization/list_organizations.html"
        ),
        name="list"
    ),

    path(
        'update/<int:pk>/',
        OrganizationView_OrganizationUpdate.as_view(
            template_name="organization/update_organization.html"
        ),
        name="update"
    ),

    path(
        'delete/<int:pk>/',
        OrganizationView_OrganizationDelete.as_view(

        ),
        name="delete"
    ),

    #####

    path(
        'add_credits/',
        OrganizationView_AddBalanceCredits.as_view(

        ),
        name="add_credits"
    ),

    path(
        'balance_transfer/',
        OrganizationView_TransferBalance.as_view(

        ),
        name='balance_transfer'
    ),

    path(
        'add_gift_credits/',
        OrganizationView_AddGiftCredits.as_view(

        ),
        name='add_gift_credits'
    ),
]
