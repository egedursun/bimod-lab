from django.urls import path
from .views import DashboardMainView


app_name = "dashboard"


urlpatterns = [
    path("", DashboardMainView.as_view(template_name="dashboard/dashboard_main.html"), name="main-dashboard"),
]
