from django.contrib import admin

from apps.support_system.models import SupportTicketResponse


@admin.register(SupportTicketResponse)
class SupportTicketResponseAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'user', 'created_at']
    search_fields = ['ticket__title', 'response']
    date_hierarchy = 'created_at'
