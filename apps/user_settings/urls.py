from django.urls import path

from apps.user_settings.views import UserSettingsView, UserSettingsUpdateView

app_name = "user_settings"


urlpatterns = [
    path('settings/', UserSettingsView.as_view(
        template_name="user_settings/settings.html"
    ), name='settings'),
    path('settings/update/', UserSettingsUpdateView.as_view(
        template_name="user_settings/update_settings.html"
    ), name='update'),
]
