#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: test_forms.py
#  Last Modified: 2024-08-07 16:37:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:10:00
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.
from apps.user_management.forms import UserStatusForm


def test_init_user_management_test_forms():
    assert True


from django.test import TestCase
from auth.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class UserStatusFormTest(TestCase):

    def setUp(self):
        # Create a user and their profile for testing
        self.user = User.objects.get_or_create(username='testuser')[0]
        self.profile = Profile.objects.get_or_create(user=self.user)[0]

    def test_form_renders_correctly(self):
        # Test that the form renders correctly with the initial data
        form = UserStatusForm(instance=self.profile)
        self.assertIn('class="form-check-input"', form.as_p())

    def test_form_valid_data(self):
        # Test that the form validates and saves data correctly
        form_data = {'is_active': False}
        form = UserStatusForm(data=form_data, instance=self.profile)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Save the form and check that the profile is updated
        form.save()
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.is_active)

    def test_form_with_initial_value(self):
        # Test that the form loads with the correct initial value
        form = UserStatusForm(instance=self.profile)

        # Check that the form reflects the initial value of `is_active`
        self.assertTrue(form.initial['is_active'])
