from django.core.files.base import ContentFile


#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: test_models.py
#  Last Modified: 2024-08-12 23:33:43
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:09:14
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

def test_init_support_system_test_models():
    assert True


from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.support_system.models import SupportTicket

User = get_user_model()


class SupportTicketModelTest(TestCase):

    def setUp(self):
        # Use get_or_create to ensure users are not duplicated during tests
        self.user, created = User.objects.get_or_create(username='testuser', password='password')

    def test_support_ticket_creation(self):
        # Test creating a support ticket with default fields
        ticket = SupportTicket.objects.create(
            user=self.user,
            title='Issue with the app',
            issue_description='The application is crashing on startup.'
        )

        # Ensure the ticket was created successfully and has default status/priority
        self.assertEqual(ticket.status, 'open')
        self.assertEqual(ticket.priority, 'low')
        self.assertEqual(ticket.user, self.user)
        self.assertEqual(ticket.title, 'Issue with the app')
        self.assertEqual(ticket.issue_description, 'The application is crashing on startup.')

    def test_support_ticket_with_custom_status_and_priority(self):
        # Test creating a support ticket with custom status and priority
        ticket = SupportTicket.objects.create(
            user=self.user,
            title='Critical issue',
            issue_description='The server is down.',
            status='in_progress',
            priority='critical',
            attachment=None
        )

        # Ensure the ticket was created successfully with the correct custom status/priority
        self.assertEqual(ticket.status, 'in_progress')
        self.assertEqual(ticket.priority, 'critical')
        self.assertEqual(ticket.title, 'Critical issue')
        self.assertEqual(ticket.issue_description, 'The server is down.')

    def test_support_ticket_with_attachment(self):
        # Test creating a support ticket with an attachment
        with open('test_attachment.txt', 'w') as f:
            f.write('Test file content')

        with open('test_attachment.txt', 'rb') as attachment_file:
            ticket = SupportTicket.objects.create(
                user=self.user,
                title='Attachment issue',
                issue_description='The file upload is not working properly.',
                attachment=ContentFile(attachment_file.read(), name='test_attachment.txt')
            )

        # Ensure the ticket was created and the attachment is saved correctly
        self.assertEqual(ticket.title, 'Attachment issue')
        self.assertIsNotNone(ticket.attachment)

    def test_ticket_ordering(self):
        # Create two tickets to test ordering by 'created_at'
        ticket1 = SupportTicket.objects.create(
            user=self.user,
            title='First issue',
            issue_description='This is the first issue.',
            attachment=None
        )
        ticket2 = SupportTicket.objects.create(
            user=self.user,
            title='Second issue',
            issue_description='This is the second issue.',
            attachment=None
        )

        # Fetch tickets and ensure they are ordered by 'created_at' (ascending)
        tickets = SupportTicket.objects.all()
        self.assertEqual(tickets[0], ticket1)
        self.assertEqual(tickets[1], ticket2)

    def test_ticket_indexes(self):
        # Test that filtering on indexed fields works as expected
        SupportTicket.objects.create(
            user=self.user,
            title='Open issue',
            issue_description='This is an open issue.',
            status='open',
            priority='low',
            attachment=None
        )
        SupportTicket.objects.create(
            user=self.user,
            title='Closed issue',
            issue_description='This is a closed issue.',
            status='closed',
            priority='high',
            attachment=None
        )

        # Fetch tickets based on status and priority indexes
        open_tickets = SupportTicket.objects.filter(status='open')
        closed_tickets = SupportTicket.objects.filter(status='closed', priority='high')

        # Ensure the correct tickets are returned
        self.assertEqual(open_tickets.count(), 1)
        self.assertEqual(closed_tickets.count(), 1)


from django.test import TestCase
from apps.support_system.models import SupportTicketResponse


class SupportTicketResponseModelTest(TestCase):

    def setUp(self):
        # Ensure unique emails are used when creating users
        self.user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'testuser@example.com', 'password': 'password'}
        )
        self.support_user, created = User.objects.get_or_create(
            username='supportuser',
            defaults={'email': 'supportuser@example.com', 'password': 'password'}
        )

        # Create a support ticket
        self.ticket = SupportTicket.objects.create(
            user=self.user,
            title='App is crashing',
            issue_description='The app crashes every time I open it.',
            status='open',
            priority='high'
        )

    def test_support_ticket_response_creation(self):
        # Create a response to the support ticket
        response = SupportTicketResponse.objects.create(
            ticket=self.ticket,
            user=self.support_user,
            response="We're investigating the issue."
        )

        # Ensure the response is created successfully
        self.assertEqual(response.ticket, self.ticket)
        self.assertEqual(response.user, self.support_user)
        self.assertEqual(response.response, "We're investigating the issue.")

        # Check that the created_at timestamp is set
        self.assertIsNotNone(response.created_at)

    def test_response_ordering(self):
        # Create two responses to the same support ticket to test ordering
        response1 = SupportTicketResponse.objects.create(
            ticket=self.ticket,
            user=self.support_user,
            response="First response."
        )
        response2 = SupportTicketResponse.objects.create(
            ticket=self.ticket,
            user=self.support_user,
            response="Second response."
        )

        # Ensure responses are ordered by 'created_at'
        responses = SupportTicketResponse.objects.filter(ticket=self.ticket).order_by('created_at')
        self.assertEqual(responses[0], response1)
        self.assertEqual(responses[1], response2)

    def test_response_indexes(self):
        # Test that filtering on indexed fields works as expected
        response = SupportTicketResponse.objects.create(
            ticket=self.ticket,
            user=self.support_user,
            response="Index testing response."
        )

        # Ensure we can filter by ticket and creation date
        filtered_by_ticket = SupportTicketResponse.objects.filter(ticket=self.ticket)
        self.assertEqual(filtered_by_ticket.count(), 1)
        self.assertEqual(filtered_by_ticket.first(), response)

        # Ensure we can filter by user and creation date
        filtered_by_user = SupportTicketResponse.objects.filter(user=self.support_user)
        self.assertEqual(filtered_by_user.count(), 1)
        self.assertEqual(filtered_by_user.first(), response)

    def test_response_str_representation(self):
        # Test the string representation of the SupportTicketResponse model
        response = SupportTicketResponse.objects.create(
            ticket=self.ticket,
            user=self.support_user,
            response="This is a response."
        )

        # Ensure the string representation includes the ticket title, username, and timestamp
        expected_str = f'{self.ticket.title} - {self.support_user.username} - {response.created_at.strftime("%Y%m%d%H:%M")}'
        self.assertEqual(str(response), expected_str)
