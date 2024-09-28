from django.urls import path

from .views import ChatView, ChatDeleteView, ChatArchiveView, ChatArchiveListView, ChatUnarchiveView, \
    ChatStreamView, ChatMessageNarrationView, LeanChatView, LeanChatArchiveView, \
    LeanChatUnarchiveView, LeanChatArchiveListView, LeanChatStreamView, LeanChatDeleteView

app_name = "multimodal_chat"

urlpatterns = [
    path('chat/', ChatView.as_view(
        template_name="multimodal_chat/chats/chat.html"
    ), name='chat'),
    path('chat/stream/', ChatStreamView.as_view(), name='chat_stream'),
    path('chat/<int:pk>/', ChatDeleteView.as_view(
        template_name="multimodal_chat/chats/confirm_delete_chat.html"
    ), name='delete'),
    path('archive/<int:pk>/', ChatArchiveView.as_view(
        template_name="multimodal_chat/archives/archived_chats.html"
    ), name='archive'),
    path('unarchive/<int:pk>/', ChatUnarchiveView.as_view(
        template_name="multimodal_chat/archives/archived_chats.html"
    ), name='unarchive'),
    path('chat/archive/', ChatArchiveListView.as_view(
        template_name="multimodal_chat/archives/archived_chats.html"
    ), name='archive_list'),

    path('tts/chat/message/<int:pk>/', ChatMessageNarrationView.as_view(), name='tts_chat_message'),

    #####

    path('lean_chat/', LeanChatView.as_view(
        template_name="multimodal_chat/chats/lean_chat.html"
    ), name='lean_chat'),
    path('lean_chat/stream/', LeanChatStreamView.as_view(), name='chat_stream_lean'),
    path('lean_chat/<int:pk>/', LeanChatDeleteView.as_view(
        template_name="multimodal_chat/chats/confirm_delete_lean_chat.html"
    ), name='delete_lean'),
    path('archive_lean/<int:pk>/', LeanChatArchiveView.as_view(
        template_name="multimodal_chat/archives/archived_lean_chats.html"
    ), name='archive_lean'),
    path('unarchive_lean/<int:pk>/', LeanChatUnarchiveView.as_view(
        template_name="multimodal_chat/archives/archived_lean_chats.html"
    ), name='unarchive_lean'),
    path('lean_chat/archive_lean/', LeanChatArchiveListView.as_view(
        template_name="multimodal_chat/archives/archived_lean_chats.html"
    ), name='archive_list_lean'),
]
