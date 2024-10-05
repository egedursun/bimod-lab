#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:45
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: urls.py
#  Last Modified: 2024-08-12 23:24:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:11:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from apps.user_profile_management.views import UserProfileListView, RemoveCardView, UserProfileResetPasswordView

app_name = "user_profile_management"

urlpatterns = [
    path("profile/", UserProfileListView.as_view(
        template_name="user_profile_management/profiles/user_profile_list.html"
    ), name="list"),
    path("reset_password/<int:pk>", UserProfileResetPasswordView.as_view(
        template_name="user_profile_management/profiles/user_profile_list.html"
    ), name="reset_password"),

    path('billing/update/', UserProfileListView.as_view(
        template_name="user_profile_management/billings/billing.html"
    ), name='billing'),
    path('remove_card/<int:card_id>/', RemoveCardView.as_view(), name='remove_card'),
]
