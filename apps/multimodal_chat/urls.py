from django.urls import path

from .views import ChatView, ChatDeleteView, ChatArchiveView, ChatArchiveListView, ChatUnarchiveView

app_name = "multimodal_chat"


urlpatterns = [
    path('chat/', ChatView.as_view(
        template_name="multimodal_chat/chat.html"
    ), name='chat'),
    path('chat/<int:pk>/', ChatDeleteView.as_view(
        template_name="multimodal_chat/confirm_delete_chat.html"
    ), name='delete'),
    path('archive/<int:pk>/', ChatArchiveView.as_view(
        template_name="multimodal_chat/archived_chats.html"
    ), name='archive'),
    path('unarchive/<int:pk>/', ChatUnarchiveView.as_view(
        template_name="multimodal_chat/archived_chats.html"
    ), name='unarchive'),
    path('chat/archive/', ChatArchiveListView.as_view(
        template_name="multimodal_chat/archived_chats.html"
    ), name='archive_list'),
]
