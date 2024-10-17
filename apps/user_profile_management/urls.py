#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:47
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

from apps.user_profile_management.views import UserProfileView_List, UserProfileView_CreditCardRemove, \
    UserProfileView_ResetPassword

app_name = "user_profile_management"

urlpatterns = [
    path("profile/", UserProfileView_List.as_view(
        template_name="user_profile_management/profiles/user_profile_list.html"), name="list"),
    path("reset_password/<int:pk>", UserProfileView_ResetPassword.as_view(
        template_name="user_profile_management/profiles/user_profile_list.html"), name="reset_password"),
    path('billing/update/', UserProfileView_List.as_view(
        template_name="user_profile_management/billings/billing.html"), name='billing'),
    path('remove_card/<int:card_id>/', UserProfileView_CreditCardRemove.as_view(), name='remove_card'),
]
