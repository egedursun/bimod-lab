from django.urls import path

from apps.message_templates.views import ListMessageTemplateView, CreateMessageTemplateView, UpdateMessageTemplateView, \
    DeleteMessageTemplateView

app_name = "message_templates"

urlpatterns = [
    path("list/", ListMessageTemplateView.as_view(
        template_name="message_templates/list_message_templates.html"
    ), name="list"),
    path("create/", CreateMessageTemplateView.as_view(
        template_name="message_templates/create_message_template.html"
    ), name="create"),
    path("<int:pk>/update/", UpdateMessageTemplateView.as_view(
        template_name="message_templates/update_message_template.html"
    ), name="update"),
    path("<int:pk>/delete/", DeleteMessageTemplateView.as_view(), name="delete"),
]
