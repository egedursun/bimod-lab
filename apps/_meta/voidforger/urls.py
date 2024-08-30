from django.urls import path

from apps._meta.voidforger.views import VoidForgerDashboardView

app_name = 'voidforger'


urlpatterns = [
    path('internal/bimodalis/', VoidForgerDashboardView.as_view(
        template_name='voidforger/voidforger_dashboard.html'
    ), name='dashboard'),
]
