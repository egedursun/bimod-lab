#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: test_utils.py
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

def test_init_support_system_test_utils():
    assert True


from django.test import TestCase
from apps.support_system.utils import TICKET_STATUSES, PRIORITY_CHOICES


class ConstantUtilsTest(TestCase):

    def test_ticket_statuses_structure(self):
        # Ensure TICKET_STATUSES is a list of tuples
        self.assertIsInstance(TICKET_STATUSES, list)
        for status in TICKET_STATUSES:
            self.assertIsInstance(status, tuple)
            self.assertEqual(len(status), 2)  # Ensure each tuple has 2 elements (key, value)

    def test_ticket_statuses_unique_keys(self):
        # Ensure all keys in TICKET_STATUSES are unique
        keys = [status[0] for status in TICKET_STATUSES]
        self.assertEqual(len(keys), len(set(keys)), "Duplicate keys found in TICKET_STATUSES")

    def test_ticket_statuses_expected_values(self):
        # Ensure expected statuses exist in TICKET_STATUSES
        self.assertIn(('open', 'Open'), TICKET_STATUSES)
        self.assertIn(('in_progress', 'In Progress'), TICKET_STATUSES)
        self.assertIn(('closed', 'Closed'), TICKET_STATUSES)
        self.assertIn(('resolved', 'Resolved'), TICKET_STATUSES)

    def test_priority_choices_structure(self):
        # Ensure PRIORITY_CHOICES is a list of tuples
        self.assertIsInstance(PRIORITY_CHOICES, list)
        for priority in PRIORITY_CHOICES:
            self.assertIsInstance(priority, tuple)
            self.assertEqual(len(priority), 2)  # Ensure each tuple has 2 elements (key, value)

    def test_priority_choices_unique_keys(self):
        # Ensure all keys in PRIORITY_CHOICES are unique
        keys = [priority[0] for priority in PRIORITY_CHOICES]
        self.assertEqual(len(keys), len(set(keys)), "Duplicate keys found in PRIORITY_CHOICES")

    def test_priority_choices_expected_values(self):
        # Ensure expected priorities exist in PRIORITY_CHOICES
        self.assertIn(('recommendation', 'Recommendation'), PRIORITY_CHOICES)
        self.assertIn(('low', 'Low'), PRIORITY_CHOICES)
        self.assertIn(('medium', 'Medium'), PRIORITY_CHOICES)
        self.assertIn(('high', 'High'), PRIORITY_CHOICES)
        self.assertIn(('critical', 'Critical'), PRIORITY_CHOICES)
