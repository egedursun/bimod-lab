from django.urls import path
from .views import DashboardMainView, RefreshStatisticsView, ChangeStatisticsDatetimeIntervalView

app_name = "dashboard"


urlpatterns = [
    path("", DashboardMainView.as_view(template_name="dashboard/dashboard_main.html"), name="main-dashboard"),
    path("refresh/<str:days>/", RefreshStatisticsView.as_view(
        template_name="dashboard/dashboard_main.html"
    ), name="refresh"),
    path("adjust_interval/<int:days>/", ChangeStatisticsDatetimeIntervalView.as_view(
        template_name="dashboard/dashboard_main.html"
    ), name="adjust-interval"),
]
