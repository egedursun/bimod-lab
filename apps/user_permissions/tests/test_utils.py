#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: test_utils.py
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
from unittest import TestCase

from apps.user_permissions.utils import PermissionNames, PERMISSION_TYPES, get_permissions_grouped


def test_init_user_permissions_test_utils():
    assert True


class PermissionNamesTest(TestCase):

    def test_permission_constants_exist(self):
        # Verify that key constants exist in PermissionNames
        self.assertEqual(PermissionNames.ADD_LLM_CORES, 'add_llm_cores')
        self.assertEqual(PermissionNames.ADD_ORGANIZATIONS, 'add_organizations')
        self.assertEqual(PermissionNames.LIST_TRANSACTIONS, 'list_transactions')
        self.assertEqual(PermissionNames.ADD_USERS, 'add_users')
        self.assertEqual(PermissionNames.ADD_ASSISTANTS, 'add_assistants')
        self.assertEqual(PermissionNames.CAN_GENERATE_IMAGES, 'can_generate_images')

    def test_permission_types_integrity(self):
        # Verify that constants from PermissionNames are present in PERMISSION_TYPES
        permission_types_dict = dict(PERMISSION_TYPES)

        # Check that some key permissions from PermissionNames exist in PERMISSION_TYPES
        self.assertIn(PermissionNames.ADD_LLM_CORES, permission_types_dict)
        self.assertIn(PermissionNames.ADD_ORGANIZATIONS, permission_types_dict)
        self.assertIn(PermissionNames.LIST_TRANSACTIONS, permission_types_dict)
        self.assertIn(PermissionNames.ADD_USERS, permission_types_dict)
        self.assertIn(PermissionNames.ADD_ASSISTANTS, permission_types_dict)
        self.assertIn(PermissionNames.CAN_GENERATE_IMAGES, permission_types_dict)


class GetPermissionsGroupedTest(TestCase):

    def test_get_permissions_grouped_structure(self):
        # Test that the function returns a dictionary and contains expected groups
        permissions_grouped = get_permissions_grouped()

        # Verify that the main keys are present
        self.assertIn("Organization Permissions", permissions_grouped)
        self.assertIn("LLM Core Permissions", permissions_grouped)
        self.assertIn("Fine-Tuning Model Permissions", permissions_grouped)
        self.assertIn("User Permissions", permissions_grouped)
        self.assertIn("Assistant Permissions", permissions_grouped)
        self.assertIn("Memory Permissions", permissions_grouped)
        self.assertIn("Orchestration Permissions", permissions_grouped)

    def test_get_permissions_grouped_permissions(self):
        # Test that the expected permissions are within their respective groups
        permissions_grouped = get_permissions_grouped()

        # Check that specific permissions are correctly grouped
        organization_permissions = permissions_grouped["Organization Permissions"]
        self.assertIn(('add_organizations', 'Add Organizations'), organization_permissions)
        self.assertIn(('list_organizations', 'List Organizations'), organization_permissions)

        llm_permissions = permissions_grouped["LLM Core Permissions"]
        self.assertIn(('add_llm_cores', 'Add LLM Cores'), llm_permissions)
        self.assertIn(('list_llm_cores', 'List LLM Cores'), llm_permissions)

        assistant_permissions = permissions_grouped["Assistant Permissions"]
        self.assertIn(('add_assistants', 'Add Assistants'), assistant_permissions)
        self.assertIn(('delete_assistants', 'Delete Assistants'), assistant_permissions)

