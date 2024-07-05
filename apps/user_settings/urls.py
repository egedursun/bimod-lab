from django.urls import path

from apps.user_settings.views import UserSettingsView

app_name = "user_settings"


urlpatterns = [
    path('settings/', UserSettingsView.as_view(
        template_name="user_settings/settings.html"
    ), name='settings'),
]
