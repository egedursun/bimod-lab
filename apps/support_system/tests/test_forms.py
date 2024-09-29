from apps.support_system.forms.support_ticket_forms import SupportTicketForm


#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: test_forms.py
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

def test_init_support_system_test_forms():
    assert True


from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

User = get_user_model()


class SupportTicketFormTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user, created = User.objects.get_or_create(username='testuser', email='testuser@example.com',
                                                        password='password')

    def test_support_ticket_form_valid_data(self):
        # Test the form with valid data
        form_data = {
            'title': 'App Issue',
            'issue_description': 'The app crashes on startup.',
            'priority': 'high'
        }
        form = SupportTicketForm(data=form_data)

        # Ensure the form is valid
        self.assertTrue(form.is_valid())

        # Save the form and ensure the ticket is created
        ticket = form.save(commit=False)
        ticket.user = self.user  # Assign the user since it's not part of the form
        ticket.save()

        # Verify the ticket is created with the correct data
        self.assertEqual(ticket.title, 'App Issue')
        self.assertEqual(ticket.issue_description, 'The app crashes on startup.')
        self.assertEqual(ticket.priority, 'high')

    def test_support_ticket_form_with_attachment(self):
        # Test the form with an attachment
        file_data = SimpleUploadedFile("testfile.txt", b"File content")
        form_data = {
            'title': 'App Issue with Attachment',
            'issue_description': 'The app has issues with attachments.',
            'priority': 'medium',
        }
        form_files = {'attachment': file_data}
        form = SupportTicketForm(data=form_data, files=form_files)

        # Ensure the form is valid
        self.assertTrue(form.is_valid())

        # Save the form and ensure the ticket is created
        ticket = form.save(commit=False)
        ticket.user = self.user  # Assign the user
        ticket.save()

        # Verify the ticket is created with the attachment
        self.assertEqual(ticket.title, 'App Issue with Attachment')
        self.assertEqual(ticket.issue_description, 'The app has issues with attachments.')
        self.assertEqual(ticket.priority, 'medium')
        self.assertIsNotNone(ticket.attachment)
        self.assertTrue(ticket.attachment.name.startswith('tickets/attachments/'))

    def test_support_ticket_form_missing_required_fields(self):
        # Test the form with missing required fields (e.g., missing title)
        form_data = {
            'issue_description': 'Missing title.',
            'priority': 'low'
        }
        form = SupportTicketForm(data=form_data)

        # Ensure the form is invalid
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_support_ticket_form_invalid_priority(self):
        # Test the form with an invalid priority choice
        form_data = {
            'title': 'App Issue',
            'issue_description': 'The app has an issue with priority.',
            'priority': 'invalid_priority'  # Invalid choice
        }
        form = SupportTicketForm(data=form_data)

        # Ensure the form is invalid
        self.assertFalse(form.is_valid())
        self.assertIn('priority', form.errors)
