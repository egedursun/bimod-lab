from django.urls import path

from .views import ChatView, ChatDeleteView

app_name = "multimodal_chat"


urlpatterns = [
    path('chat/', ChatView.as_view(
        template_name="multimodal_chat/chat.html"
    ), name='chat'),
    path('chat/<int:pk>/', ChatDeleteView.as_view(
        template_name="multimodal_chat/confirm_delete_chat.html"
    ), name='delete'),
]
