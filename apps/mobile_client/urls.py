#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-11-26 14:19:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-26 14:19:48
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

from apps.mobile_client.views import (
    MobileChatView_ChatConfiguration,
    MobileChatView_ChatList,
    MobileChatView_ChatDetail
)

app_name = 'mobile_client'

urlpatterns = [
    path(
        'chat/list/',
        MobileChatView_ChatList.as_view(
            template_name='mobile_client/mobile_chats.html'
        ),
        name='chat_list'
    ),

    path(
        'chat/main/',
        MobileChatView_ChatDetail.as_view(
            template_name='mobile_client/mobile_chat_detail.html'
        ),
        name='chat_detail'
    ),

    path(
        'chat/configuration/',
        MobileChatView_ChatConfiguration.as_view(
            template_name='mobile_client/mobile_chat_configuration.html'
        ),
        name='chat_configuration'
    ),
]
