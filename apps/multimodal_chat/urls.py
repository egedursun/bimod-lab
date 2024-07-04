from django.urls import path

from .views import ChatView

app_name = "multimodal_chat"


urlpatterns = [
    path('chat/', ChatView.as_view(
        template_name="multimodal_chat/chat.html"
    ), name='chat'),
]
