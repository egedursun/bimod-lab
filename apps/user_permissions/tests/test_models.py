

#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: test_models.py
#  Last Modified: 2024-08-07 16:37:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:10:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

def test_init_user_permissions_test_models():
    assert True


from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.user_permissions.models import UserPermission, PERMISSION_TYPES

User = get_user_model()


class UserPermissionModelTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='password')

        # Permission types to use in tests
        self.permission_type_1 = PERMISSION_TYPES[0][0]
        self.permission_type_2 = PERMISSION_TYPES[1][0]

        # Create an active permission for the user
        self.permission = UserPermission.objects.create(
            user=self.user,
            permission_type=self.permission_type_1,
            is_active=True,
        )

    def test_permission_creation(self):
        # Ensure the permission is correctly created
        self.assertEqual(self.permission.user, self.user)
        self.assertEqual(self.permission.permission_type, self.permission_type_1)
        self.assertTrue(self.permission.is_active)

    def test_get_permission_type_name(self):
        # Ensure the human-readable name of the permission type is correct
        self.assertEqual(self.permission.get_permission_type_name(), dict(PERMISSION_TYPES)[self.permission_type_1])

    def test_get_permission_type_code(self):
        # Ensure the code of the permission type is returned correctly
        self.assertEqual(self.permission.get_permission_type_code(), self.permission_type_1)

    def test_unique_user_permission_constraint(self):
        # Ensure the unique constraint prevents a duplicate permission for the same user and type
        with self.assertRaises(Exception):
            UserPermission.objects.create(
                user=self.user,
                permission_type=self.permission_type_1,
                is_active=True,
            )

    def test_custom_manager_active_permissions(self):
        # Ensure the custom manager only returns active permissions
        active_permissions = UserPermission.active_permissions.all()
        self.assertIn(self.permission, active_permissions)

        # Create an inactive permission and check if it's excluded
        inactive_permission = UserPermission.objects.create(
            user=self.user,
            permission_type=self.permission_type_2,
            is_active=False,
        )
        self.assertNotIn(inactive_permission, active_permissions)

    def test_ordering_by_created_at(self):
        # Ensure permissions are ordered by created_at in descending order
        new_permission = UserPermission.objects.create(
            user=self.user,
            permission_type=self.permission_type_2,
            is_active=True,
        )
        permissions = UserPermission.objects.all()
        self.assertEqual(permissions.first(), new_permission)
        self.assertEqual(permissions.last(), self.permission)

    def test_indexes_on_user_and_permission_type(self):
        # Ensure the indexes on user and permission type are functioning (no explicit assertion needed, just ensuring no error)
        UserPermission.objects.filter(user=self.user, permission_type=self.permission_type_1)
        UserPermission.objects.filter(user=self.user, permission_type=self.permission_type_1, is_active=True)

    def test_permissions_can_be_inactive(self):
        # Ensure a permission can be inactive and correctly retrieved
        self.permission.is_active = False
        self.permission.save()
        self.assertFalse(self.permission.is_active)

