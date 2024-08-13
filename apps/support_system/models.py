"""
Module: support_system.models

This module defines the models for the support ticket system, including the main
SupportTicket model and the SupportTicketResponse model for managing user support
interactions. It includes the necessary fields, relationships, and metadata for the
proper functioning of the ticketing system.
"""

from django.db import models


TICKET_STATUSES = [
    ('open', 'Open'),
    ('in_progress', 'In Progress'),
    ('closed', 'Closed'),
    ('resolved', 'Resolved'),
]

PRIORITY_CHOICES = [
    ('recommendation', 'Recommendation'),
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('critical', 'Critical'),
]


# Create your models here.

class SupportTicket(models.Model):
    """
    Model: SupportTicket

    The SupportTicket model represents a support ticket submitted by a user. It contains
    information about the user who submitted the ticket, the title, a detailed description
    of the issue, the status of the ticket, and the priority level. The model also includes
    fields for file attachments, creation date, and last updated date.

    Fields:
    - user: ForeignKey to the auth.User model representing the user who submitted the ticket.
    - title: CharField for the title of the support ticket.
    - issue_description: TextField for a detailed description of the issue.
    - status: CharField representing the current status of the ticket (e.g., open, in progress, closed, resolved).
    - priority: CharField indicating the priority level of the ticket (e.g., low, medium, high, critical).
    - attachment: FileField for optional file attachments related to the ticket.
    - created_at: DateTimeField automatically set to the timestamp when the ticket was created.
    - updated_at: DateTimeField automatically updated to the current timestamp whenever the ticket is modified.

    Meta Options:
    - ordering: Default ordering is by the creation date ('created_at').
    - verbose_name: Singular name of the model in the admin interface.
    - verbose_name_plural: Plural name of the model in the admin interface.
    - indexes: Database indexes to optimize querying based on status, priority, and timestamps.
    """

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    issue_description = models.TextField()
    status = models.CharField(max_length=50, choices=TICKET_STATUSES, default='open')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='low')

    attachment = models.FileField(upload_to='tickets/attachments/%Y/%m/%d/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.status} - {self.priority} - {self.created_at.strftime("%Y%m%d%H:%M")}'

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Support Ticket'
        verbose_name_plural = 'Support Tickets'

        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['status', 'updated_at']),
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['status', 'priority', 'created_at']),
            models.Index(fields=['status', 'priority', 'updated_at']),
        ]


class SupportTicketResponse(models.Model):
    """
    Model: SupportTicketResponse

    The SupportTicketResponse model represents a response to a support ticket. It contains
    a reference to the corresponding SupportTicket, the user who submitted the response, and
    the response content itself. The model also tracks the timestamp when the response was created.

    Fields:
    - ticket: ForeignKey to the SupportTicket model, representing the ticket this response is associated with.
    - user: ForeignKey to the auth.User model, representing the user who submitted the response.
    - response: TextField for the content of the response.
    - created_at: DateTimeField automatically set to the timestamp when the response was created.

    Meta Options:
    - ordering: Default ordering is by the creation date ('created_at').
    - verbose_name: Singular name of the model in the admin interface.
    - verbose_name_plural: Plural name of the model in the admin interface.
    - indexes: Database indexes to optimize querying based on the ticket, user, and creation date.
    """

    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    response = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Support Ticket Response'
        verbose_name_plural = 'Support Ticket Responses'

        indexes = [
            models.Index(fields=['ticket', 'created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['ticket', 'user', 'created_at']),
        ]

    def __str__(self):
        return f'{self.ticket.title} - {self.user.username} - {self.created_at.strftime("%Y%m%d%H:%M")}'
