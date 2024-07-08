from django.urls import path

from apps.starred_messages.views import ListStarredMessageView

app_name = "starred_messages"


urlpatterns = [
    path("list/", ListStarredMessageView.as_view(), name="list"),
]
