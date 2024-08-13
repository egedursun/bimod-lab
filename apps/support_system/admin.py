from django.contrib import admin

from apps.support_system.models import SupportTicket, SupportTicketResponse


# Register your models here.

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority']
    search_fields = ['title', 'issue_description']
    date_hierarchy = 'created_at'


@admin.register(SupportTicketResponse)
class SupportTicketResponseAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'user', 'created_at']
    search_fields = ['ticket__title', 'response']
    date_hierarchy = 'created_at'
