from django.urls import path
from .views import CreateSupportTicketView, SupportTicketListView, SupportTicketDetailView

app_name = 'support_system'

urlpatterns = [
    path('create/', CreateSupportTicketView.as_view(
        template_name='support_system/create_support_ticket.html'
    ), name='create'),
    path('list', SupportTicketListView.as_view(
        template_name='support_system/list_support_tickets.html'
    ), name='list'),
    path('list/<int:pk>/', SupportTicketDetailView.as_view(
        template_name='support_system/support_ticket_detail.html'
    ), name='detail'),
]
