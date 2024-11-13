#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:43
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

from .views import ChatView_Chat, ChatView_ChatDelete, ChatView_ChatArchive, ChatView_ListArchivedChats, \
    ChatView_ChatUnarchive, \
    ChatView_ChatStream, LeanChat_MessageNarration, ChatView_LeanChat, ChatView_LeanChatArchive, \
    ChatView_LeanChatUnarchive, ChatView_LeanChatListArchivedChats, ChatView_LeanChatStream, ChatView_LeanChatDelete, \
    ChatView_MainWorkspace

app_name = "multimodal_chat"

urlpatterns = [
    path('chat/', ChatView_Chat.as_view(template_name="multimodal_chat/chats/chat.html"), name='chat'),
    path('chat/stream/', ChatView_ChatStream.as_view(), name='chat_stream'),
    path('chat/<int:pk>/', ChatView_ChatDelete.as_view(
        template_name="multimodal_chat/chats/confirm_delete_chat.html"), name='delete'),
    path('archive/<int:pk>/', ChatView_ChatArchive.as_view(
        template_name="multimodal_chat/archives/archived_chats.html"), name='archive'),
    path('unarchive/<int:pk>/', ChatView_ChatUnarchive.as_view(
        template_name="multimodal_chat/archives/archived_chats.html"), name='unarchive'),
    path('chat/archive/', ChatView_ListArchivedChats.as_view(
        template_name="multimodal_chat/archives/archived_chats.html"), name='archive_list'),
    path('tts/chat/message/<int:pk>/', LeanChat_MessageNarration.as_view(), name='tts_chat_message'),
    path('lean_chat/', ChatView_LeanChat.as_view(template_name="multimodal_chat/chats/lean_chat.html"),
         name='lean_chat'),
    path('lean_chat/stream/', ChatView_LeanChatStream.as_view(), name='chat_stream_lean'),
    path('lean_chat/<int:pk>/', ChatView_LeanChatDelete.as_view(
        template_name="multimodal_chat/chats/confirm_delete_lean_chat.html"), name='delete_lean'),
    path('archive_lean/<int:pk>/', ChatView_LeanChatArchive.as_view(
        template_name="multimodal_chat/archives/archived_lean_chats.html"), name='archive_lean'),
    path('unarchive_lean/<int:pk>/', ChatView_LeanChatUnarchive.as_view(
        template_name="multimodal_chat/archives/archived_lean_chats.html"), name='unarchive_lean'),
    path('lean_chat/archive_lean/', ChatView_LeanChatListArchivedChats.as_view(
        template_name="multimodal_chat/archives/archived_lean_chats.html"), name='archive_list_lean'),

    path('workspace/', ChatView_MainWorkspace.as_view(template_name="multimodal_chat/workspace/main_workspace.html"
                                                      ), name='main_workspace')
]
