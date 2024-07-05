from django.urls import path

from apps.landing.views import LandingPageView


app_name = "landing"


urlpatterns = [
    path("", LandingPageView.as_view(template_name="landing/index.html"), name="index"),
]
